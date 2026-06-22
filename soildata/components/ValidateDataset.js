"use client"

import { point, featureCollection, feature, toMercator, bbox, bboxPolygon, clone, toWgs84 } from '@turf/turf';
import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';

import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import { Checkbox } from 'primereact/checkbox';
import { InputNumber } from 'primereact/inputnumber';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import { Chart } from 'primereact/chart';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

import { useUser } from '../context/user';
import VariogramGraph from './Variogram';

import ProfileService from '../service/profiles';
import TaxonomyService from '../service/taxonomies';
import dynamic from 'next/dynamic'

const PointsFilterMap = dynamic(() => import("./map/PointsFilterMap"), { ssr:false })

export default function ValidateDataset( { dataset, setDataset })  { 
  const models = [ 
    { name: 'Linear', formula: 'a + b * x'}, 
    { name: 'Power', formula: 'a + b * x^k'}, 
    { name: 'Square', formula: 'a + b * sqrt(x)'}, 
    { name: 'Logarithmic', formula: 'a + b * ln(1 + x)'}
  ]
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  const [isWorking, setIsWorking] = useState(false);
  // dataset work object
  const [workDataset, setWorkDataset] = useState(dataset);
  // semi variogram result data 
  const [variogram, setVariogram] = useState(null);
  // variogram points in simple mercator projection
  const [mapPoints, setMapPoints] = useState([])
  const [noOutliers, setNoOutliers] = useState(false)
  const [kriging, setKriging] = useState(null);
  const [maxDist, setMaxDist] = useState(-1.00000);
  const [nClasses, setNClasses] = useState(100); 
  const [nSkip, setNSkip] = useState(1); 
  const [model, setModel] = useState(models[0]);
  const [descriptors, setDescriptors] = useState([]);
  const [message, setMessage] = useState('');
  const [visibleFiltered, setVisibleFiltered] = useState(false)
  const [visibleAggregated, setVisibleAggregated] = useState(false)

  function generateDescriptor () {
    const _descriptors = [
      { name: "Name", value: workDataset.name },
      { name: "Owner", value: workDataset.user_email },
      { name: "Date", value: workDataset.date },
      { name: "Source", value: workDataset.source },
    ]
    if ( workDataset.points)
      _descriptors.push({ name: "Source points", value: ( workDataset.points.features ? workDataset.points.features.length : 0 ) })
    else
      _descriptors.push({ name: "Source points", value: 0 })
    if ( workDataset.filter.points)
      _descriptors.push({ name: "Filtered points", value: ( workDataset.filter.points.features ? workDataset.filter.points.features.length : 0 ) })
    else
      _descriptors.push({ name: "Filtered points", value: 0 })
    if ( workDataset.k_data ){
      const len = (workDataset.k_data.features ? workDataset.k_data.features.length : 0);
      _descriptors.push({ name: "Aggregated points", value: len })  
    }
    else {
      _descriptors.push({ name: "Aggregated points", value: 0 })
    }
    setDescriptors(_descriptors)
  }

  function truncate (num) {
    let nums = num.toString(),
        decPos = nums.indexOf('.');
    if ( decPos === -1 )
      nums += '.000000'
    else nums += '000000' 
    let substrLength = decPos == -1 ? nums.length : 1 + decPos + 6,
        trimmedResult = nums.substr(0, substrLength),
        finalResult = isNaN(trimmedResult) ? 0 : trimmedResult;
    return finalResult;
  }

  function evalDepth (ft, depth_class) {
    // 0 to 20 cm OR 20 to 50 cm
    if ( !ft || !ft.properties || ft.properties.upper === null || !depth_class  )
      return 0;
    const uA = depth_class === ProfileService.FILTER_DEPTH.DEPTH0_20 ? 0 : 20,
          lA = depth_class === ProfileService.FILTER_DEPTH.DEPTH0_20 ? 20 : 50,
          uB = ft.properties.upper,
          lB = ft.properties.lower !== null ? ft.properties.lower: lA,
          l = ( lA > lB ) ? lB : lA,
          u = ( uA > uB ) ? uA : uB,
          perc = 0; 
    
    if ( (l - u) > 0 )   
      perc = (l-u)/(lA-uA)
    return perc; 
  }
  
  // The median absolute deviation (MAD) is used to identify outliers.
  function findOutliers( points ) {
    try {  
      if ( !points || !points.features )
        return []
      let array = [];
      const median = null
      points.features.forEach( ft => {
        if ( ft.properties && ft.properties.value && !isNaN( parseFloat( ft.properties.value ) ) )                
          array.push( parseFloat( ft.properties.value ) )
      })
      let ordered = [...array].sort((a, b) => a - b);
      let middle = Math.floor(ordered.length / 2);
      if ( middle > 0 ) 
      // if the ordered size is an odd number return the central value
        median = (ordered.length % 2 !== 0) ? ordered[middle] : (ordered[middle - 1] + ordered[middle]) / 2;
      if ( median ) {
        array = array.map( (elem) => ( median - elem  > 0 ) ? ( median - elem )  : ( elem - median ) )
        ordered = [...array].sort((a, b) => a - b);
        middle = Math.floor(ordered.length / 2);
        let mad = null;
        // if the ordered size is an odd number return the central value
        if ( middle > 0 ) 
          mad = (ordered.length % 2 !== 0) ? ordered[middle] : (ordered[middle - 1] + ordered[middle]) / 2;
        points.features.forEach( ft => {
          if ( ft.properties && ft.properties.value && !isNaN( parseFloat( ft.properties.value ) ) ) {
            const v = parseFloat( ft.properties.value )
            if ( mad != null && ( ( v - median > 0 ) ? ( v - median ) : ( median - v ) ) > 5*mad )
              ft.properties.outlier = true
            else ft.properties.outlier = false                
          }  
        })
      }
    } catch (error) {
      console.log(error)  
    }  
    return points
  }

  // points aggregation using sixth decimal place (1 meter) in latitude and longitude
  // variogram data is in simple mercator instead UTM to speed validation
  const aggregatePoints = async () => {
    const aggregateIndex = {}
    if ( !workDataset || !workDataset.filter.points || !workDataset.filter.points.features )
      return
    let epsg_utm_code = null
    workDataset.filter.points.features.forEach( ft => {
      if ( ft.geometry.coordinates ){
        const key = truncate( ft.geometry.coordinates[0] ) + '_' + truncate ( ft.geometry.coordinates[1] );
        if ( !epsg_utm_code )
          epsg_utm_code = getUTM_EPSG_CODE(ft.geometry.coordinates[1], ft.geometry.coordinates[0])
        const p = evalDepth( ft, workDataset.filter.depth )
        if ( ft.properties && ft.properties.value && p > 0 ){
          if ( !aggregateIndex[key] )
          aggregateIndex[key] = { points: [], values: [], percentages: [] }
          // geo point for interpolation (UTM)
          aggregateIndex[key].pt = point([ft.geometry.coordinates[0],ft.geometry.coordinates[1]])
          // latitude
          aggregateIndex[key].lat = truncate( ft.geometry.coordinates[1] )
          // longitude
          aggregateIndex[key].lon = truncate( ft.geometry.coordinates[0] )
          // list of point values ​​and their relative depth intersection percentage
          aggregateIndex[key].points.push(ft.properties.id)
          aggregateIndex[key].values.push(ft.properties.value)
          aggregateIndex[key].percentages.push(p)
        } 
      }  
    });
    /// aggregated points for kriging interpolation
    const kPts = [];
    const popups = {};
    Object.keys(aggregateIndex).forEach ((d) => {
      try {
        const data = aggregateIndex[d]
        const kPt = data.pt
        let sum = 0 
        for ( let i = 0; i < data.values.length; i += 1 )
          sum += data.values[i] * data.percentages[i]
        let panel = '<div class="flex flex-column justify-content-center text-cyan-500 font-bold">';
        panel += '<div class="justify-content-center text-blue-500 font-bold">' + data.points.length + ' aggregated Points '
        panel += '<div>Latitude ' + data.lat + '</div>';
        panel += '<div>Longitude ' + data.lon + '</div>';
        panel += '<div>Value ' + (sum / data.values.length) + '</div>';
        panel += '<div>[Point id :  value * depth percentage ] '
        for ( let i = 0; i < data.points.length; i+=1 ) 
          panel += '<div>' + data.points[i] + ': ' + data.values[i] + ' * ' + data.percentages[i] + '</div>'
        panel += '</div>'
        kPt.properties = { id: d, lat: data.lat, lon: data.lon, value: sum / data.values.length }
        kPts.push(kPt)
        popups[d] = panel
      } catch (error) {
        console.log(error)
      }
    })
    if ( kPts.length > 0 ){
      workDataset.k_data = findOutliers(featureCollection(kPts))
      workDataset.k_params.epsg = epsg_utm_code;
      const vPts = []
      const mPts = []
      workDataset.k_data.features.forEach ( (ft) => {
        if ( !workDataset.k_params.outlier )
          vPts.push( toMercator(ft) )
        const mPt = clone(ft)
        mPt.properties.popup = popups[mPt.properties.id]
        mPts.push(mPt)
      })
      workDataset.k_params.points = featureCollection(vPts)
      setMapPoints(featureCollection(mPts))
    } 
    else {
      workDataset.k_params.epsg = null
      workDataset.k_data = null;
      workDataset.k_params.points = null;
      setMapPoints(null);
    } 
    setWorkDataset(workDataset);
    await saveWorkDataset();  
  };

  const openList = () => {
    router.push(`/publish`);
  };

  // This saves the dataset on backoffice db
  const saveWorkDataset = async () => {
    setIsWorking(true)
    try {
      // save needs at least points  
      if ( !workDataset || !workDataset.id  )
        return;
      // reset post configuration parameters 
      const response = await ProfileService.update( document.cookie, workDataset.id, workDataset, 'datasets'  );
      if ( response && response.ok ) { 
        toast.current.show({severity: 'success', summary: 'Success!', detail: 'New Dataset has been saved' , life: 3000});
        const newData = response.data;
        setWorkDataset(newData)
        setDataset(newData)
      } 
      else toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset configuration' , life: 3000});
    } catch (error) {
      console.log(error)
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset' , life: 3000}); 
    }
    setIsWorking(false) 
  } 

  // elaborate and/or publish  new dataset 
  const finalizeDataset = async () => {
    /* publish in the catalogue */ 
    workDataset.status = ProfileService.DATASET_STATUSES.VALIDATED
    if ( workDataset.kriging && ( !workDataset.k_params || !workDataset.k_data || !workDataset.k_data.features || workDataset.k_data.features.length < 3 )){
      toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Too few points to perform interpolation.'});
      return;
    }
    //if kriging is True generates points in WGS84 to interpolate
    if ( workDataset.kriging ) {
      if ( workDataset.k_params.noOutliers ){
        const kPoints = [];
        workDataset.k_data.features.forEach( (ft) => {  
          if ( !ft.properties.outlier )
            kPoints.push(ft) 
        })
        workDataset.k_params.points = featureCollection(kPoints)
      }  
      else workDataset.k_params.points = workDataset.k_data
      console.log(workDataset.k_params.points)
    }
    setWorkDataset(workDataset)
    await saveWorkDataset()
    openList()
  } 

  // Re-configure   --- to NULL
  const backToConfiguration = async () => {
    workDataset.status = ProfileService.DATASET_STATUSES.CREATED
    if ( workDataset.k_params && workDataset.k_params.points ){
      workDataset.k_params.epsg = null;
      workDataset.k_params.points = null;
    }
    workDataset.k_data = null;
    workDataset.k_variogram = null;
    setWorkDataset(workDataset)
    await saveWorkDataset()
  }
    
  // Calculate variogram 
  const calculateVariogram = async () => {
    try {
      setMessage('');
      const bounds = featureCollection([bboxPolygon(bbox(workDataset.filter.aoi)) ]);
      workDataset.k_params.bbox = bounds;
      workDataset.k_params.nClasses = nClasses;
      workDataset.k_params.model = model.formula;
      workDataset.k_params.nSkip = nSkip;
      workDataset.k_params.maxDist = maxDist;
      workDataset.k_params.noOutliers = noOutliers;
      workDataset.k_variogram = null;
      const vPts = []
      workDataset.k_data.features.forEach ( (ft) => {
        if ( !noOutliers || !ft.properties.outlier )
          vPts.push( toMercator(ft) )
      })
      workDataset.k_params.points = featureCollection(vPts)
      setWorkDataset(workDataset);
      setVariogram(null);
      if ( !workDataset.k_params.points || !workDataset.k_params.points.features || workDataset.k_params.points.features.length < 3 )
        setMessage('Too few points to interpolate.');
      else {
        const response = await ProfileService.calculateVariogram(document.cookie, workDataset.id, workDataset.k_params);  
        if ( response && response.ok && response.data ) {
          let var_pts = []
          let mod_pts = []
          let max = 0
          let mind = null
          let maxd = 0 
          if ( response.data.variogram ) {
            let array = response.data.variogram.split('\n')
            let matrix = array.map( (e) => e.split(',') )
            matrix = matrix.slice(1);
            matrix.forEach( (e) => {
              if ( e && e.length === 6 && e[1] && e[3] && e[5]  ){
                var_pts.push({ x: e[1] , y: e[3] })
                mod_pts.push({ x: e[1] , y: e[5] })
                if ( e[3] > max ) max =  Math.round(e[3])
                if ( e[5] > max ) max =  Math.round(e[5])
                if ( mind === null || e[1] < mind  )
                  mind = Math.floor(e[1])
                if ( e[1] > maxd ) maxd = Math.round(e[1])            
              } 
            })
            workDataset.k_variogram = {
              var_pts: var_pts,
              mod_pts: mod_pts,
              max: max + 10,
              mind: mind,
              maxd: maxd,
              model: model.formula
            }
            setWorkDataset(workDataset)
            await saveWorkDataset()
            setVariogram(workDataset.k_variogram)
            toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Variogram has been created.'});
          } 
        } 
        else setMessage('Variogram not calculated, wrong parameters (e.g maxDist too low ) or System error (try later)')
      }
    } catch (error) {
      setMessage('Variogram not calculated System error (try later)')     
    }    
  }

  // retrive the UTM EPSG Code needed in kriging interpolation
  const getUTM_EPSG_CODE = (latitude, longitude) => {
    // Ensure longitude is within valid -180 to 180 range
    const lon = parseFloat(longitude);
    const lat = parseFloat(latitude);

    // Calculate zone number
    let zoneNumber = Math.floor((lon + 180) / 6) + 1;

    // Handle special case for Norway/Svalbard exception
    if (lat >= 56.0 && lat < 64.0 && lon >= 3.0 && lon < 12.0) {
        zoneNumber = 32;
    }
    // Handle special cases for Svalbard exceptions
    if (lat >= 72.0 && lat < 84.0) {
        if (lon >= 0.0 && lon < 9.0) zoneNumber = 31;
        else if (lon >= 9.0 && lon < 21.0) zoneNumber = 33;
        else if (lon >= 21.0 && lon < 33.0) zoneNumber = 35;
        else if (lon >= 33.0 && lon < 42.0) zoneNumber = 37;
    }

    const utm_emisphere = lat >= 0 ? 'EPSG:326' : 'EPSG:327';
    return `${utm_emisphere}${zoneNumber}`
  }
    
  const headerTemplate1 = () => {
      return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }} >List of filtered points values</h4>
  };
  
  const headerTemplate2 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}> List of aggregated points values</h4>
  };
  
  const getPtsValues = (fromFilter) => {
    try {
      const pts = []
      let features = workDataset.filter.points.features 
      if ( !fromFilter )
        features = workDataset.k_data.features
      features.forEach((ft) => {
        let upper = fromFilter ? ft.properties.upper : ( workDataset.filter.depth === ProfileService.FILTER_DEPTH.DEPTH0_20 ) ? 0 : 20 ;
        let lower = fromFilter ? ft.properties.lower : ( workDataset.filter.depth === ProfileService.FILTER_DEPTH.DEPTH0_20 ) ? 20 : 50 ;
        pts.push( { code: ft.properties.id, value: ft.properties.value, upper: upper + " cm", lower: lower + " cm" } )
      });
      return pts; 
    } catch (error) {
      console.log(error)
    }
    return [];
  }

  const getOutliers = () => {
    let ol = 0;
    if ( workDataset.k_data && workDataset.k_data.features )
      workDataset.k_data.features.forEach ( (ft) => { 
        if ( ft.properties && ft.properties.outlier )
          ol += 1;
      } )
    return ol;
  }

  // initialize parameters for kriging if present 
  const initializeData = async () => {
    if ( !dataset )
      return;
    setKriging(dataset.kriging);
    if ( dataset.k_params ) {
      if ( dataset.k_params.maxDist )  
        setMaxDist(dataset.k_params.maxDist)
      if ( dataset.k_params.nClasses )  
        setNClasses(dataset.k_params.nClasses)
      if ( dataset.k_params.nSkip )  
        setNSkip(dataset.k_params.nSkip)
      if ( dataset.k_params.model )  
        models.forEach( (m) =>  { if ( m.formula === dataset.k_params.model ) setModel(m) } )
      if ( dataset.k_params.noOutliers )  
        setNoOutliers(dataset.k_params.noOutliers)
    }
    setWorkDataset(dataset);
    await aggregatePoints()
    generateDescriptor()
  }

  //OK
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    if ( dataset ) 
      initializeData()   
  }, [user]); // eslint-disable-line

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      { !workDataset && (
      <span className="font-bold text-red-800">Error: dataset not initialized </span>
      )} 
      { workDataset && (
      <>
      <Dialog  header={headerTemplate1} visible={visibleFiltered} style={{ width: '50vw' }}
        onHide={() => {if (!visibleFiltered) return; setVisibleFiltered(false); }} className="surface-200">
      {( workDataset.filter.points && workDataset.filter.points.features && workDataset.filter.points.features.length > 0 ) && (
        <div className="card flex flex-column gap-2 text-cyan-800 w-full align-items-center">      
        <h5 className="font-bold text-cyan-800 mt-1 mb-1">{t('VALUES')}:</h5>
        <DataTable value={getPtsValues(true)} className="text-cyan-800 ml-5 mt-1" tableStyle={{ minWidth: '30rem' }} >
          <Column field="code" sortable header={(<span className='text-xl font-bold'>{t('CODE')}</span>)} headerClassName="w-10rem"></Column>
          <Column field="value" sortable header={(<span className='text-xl font-bold'>{t('VALUE')}</span>)}></Column>
          <Column field="upper" sortable header={(<span className='text-xl font-bold'>{t('UPPER')}</span>)}></Column>
          <Column field="lower" sortable header={(<span className='text-xl font-bold'>{t('LOWER')}</span>)}></Column>
        </DataTable>
        </div>
        )} 
        {( workDataset.k_data && workDataset.k_data.length > 0 ) && (
        <h5 className="col-12 font-bold text-cyan-800 mt-1 mb-1">No filtered points found</h5>          
        )}
      </Dialog>        
      <Dialog  header={headerTemplate2} visible={visibleAggregated} style={{ width: '50vw' }} 
        onHide={() => {if (!visibleAggregated) return; setVisibleAggregated(false); }} className="surface-200">
          {( workDataset.k_data && workDataset.k_data.features && workDataset.k_data.features.length > 0 ) && (
          <div className="card flex flex-column text-cyan-800 w-full align-items-center">      
          <h5 className="font-bold text-cyan-800 mt-1 mb-1">{t('VALUES')}:</h5>
          <DataTable value={getPtsValues(false)} className="text-cyan-800 ml-5 col-12 mt-1" tableStyle={{ minWidth: '30rem' }} >
            <Column field="code" sortable header={(<span className='text-xl font-bold'>{t('CODE')}</span>)} headerClassName="w-10rem"></Column>
            <Column field="value" sortable header={(<span className='text-xl font-bold'>{t('VALUE')}</span>)}></Column>
            <Column field="upper" sortable header={(<span className='text-xl font-bold'>{t('UPPER')}</span>)}></Column>
            <Column field="lower" sortable header={(<span className='text-xl font-bold'>{t('LOWER')}</span>)}></Column>
          </DataTable>
          </div>
          )} 
          {( !workDataset.k_data || workDataset.k_data.length === 0 ) && (
          <h5 className="col-12 font-bold text-cyan-800 mt-1 mb-1">Aggregated points not found</h5>          
          )}
      </Dialog>
      <div className="card flex flex-warp text-cyan-800 w-full align-items-center">
        <div className="flex flex-column text-cyan-800 md:w-6 sm:w-full">
          <h5 className="flex justify-content-center w-full text-cyan-800">Aggregated Filtered Points Map</h5> 
          <PointsFilterMap points={mapPoints} area={workDataset.filter.aoi}  />
        </div>
        <div className="flex flex-column gap-2 align-content-start text-cyan-800 md:w-6 sm:w-full m-2">
          <h5 className="flex justify-content-center w-full text-cyan-800">Summary of the new Dataset </h5>
          <DataTable className="font-bold text-cyan-800"  value={descriptors} tableStyle={{ minWidth: '40rem' }}>
            <Column field="name" header="" style={{ width: '25%' }}></Column>
            <Column field="value" header=""  className="text-yellow-800" ></Column>
          </DataTable>
          <div className="card flex flex-column gap-2 font-bold w-full"> 
            { getOutliers() > 0 && (
              <Message severity="error" text={"Warning! Found " + getOutliers() + " outliers in values"} />
            )}
            { getOutliers() === 0 && (
              <Message severity="success" text="Good! Found 0 outlier in values" />
            )} 
            { workDataset.k_data && workDataset.k_data.features && workDataset.k_data.features.length < 20 && (
              <Message severity="warn" text="Warning! The dataset has too few points for interpolation." />
            )}
            { !workDataset.k_data || !workDataset.k_data.features || workDataset.k_data.features.length === 0 && (
              <Message severity="error" text="Warning! The dataset has no points for interpolation." />
            )} 
              <div className="flex flex-row gap-3 w-full justify-content-center align-items-center"> 
              <Button
                className="button"
                loading={isWorking}
                disabled={isWorking}
                label={t('SHOW_FILTERED')}
                icon="pi pi-wrench"
                onClick={() => { setVisibleFiltered(true); }}
              />
              <Button
                className="button"
                loading={isWorking}
                disabled={isWorking}
                label={t('SHOW_AGGREGATED')}
                icon="pi pi-wrench"
                onClick={() => { setVisibleAggregated(true); }}
              />
            </div>
          </div>
        </div>
      </div>       
      <div className="card flex flex-row text-cyan-800 w-full justify-content-center align-items-center"> 
          <h5 className="text-cyan-800">
            <Checkbox 
                onChange={ (e) => { setKriging(e.checked); setWorkDataset({ ...workDataset, kriging: e.checked })}} 
                className="mr-3" checked={kriging} /> 
              Elaborate Kriging Interpolation
          </h5>
      </div> 

      { workDataset.kriging && (
      <div className="card flex flex-warp text-cyan-800 w-full justify-content-center align-items-center">
        <div className="flex flex-column gap-2 text-cyan-800 md:w-5 sm:w-full">
          <Card title={t('KRIGING_INTERPOLATION')} subTitle={t('KRIGING_INTERPOLATION_SUBTILE')} 
              className="flex flex-column justify-content-center w-full gap-3 text-cyan-800">
            
            { getOutliers() > 0 && (
            <>
            <h5 className="mt-3 text-cyan-800">
            <Checkbox 
              onChange={ (e) => { 
                setNoOutliers(e.checked); 
                setWorkDataset({ ...workDataset, k_param: { ...workDataset.k_params , noOutliers: e.checked }})
              }}  
              className="mr-3" checked={noOutliers} /> 
              Do not use outliers
            </h5>
            <div className="mt-1 text-red-800">
            <span> The presence of outliers generates out of scale predictions by skewing parameter estimates and 
              altering the underlying data distribution. Outliers can result from data entry errors, but they can 
              also be genuine data points that </span>
            <span className="font-bold"> WARRANT MORE INVESTIGATION.</span>
            </div>
            </>
            )} 
            <h5 className="mt-3">Model ( Default: linear &quot; a + x * b &quot;  )</h5> 
            <Dropdown value={model} onChange={(e) => setModel(e.value)} options={models} optionLabel="name" 
              placeholder="Select a model" className="w-full md:w-14rem" />
            { model && (
            <h6 className="mt-1 text-cyan-800">{ model.formula }</h6> 
            )}     
            <h5 className="mt-3">Initial Number of Distance Classes ( Minimum: 2, Default: 100 )</h5> 
            <InputNumber value={nClasses} onValueChange={(e) => setNClasses(e.value)} showButtons buttonLayout="horizontal" step={10}
                decrementButtonClassName="p-button-danger" decrementButtonIcon="pi pi-minus"
                incrementButtonClassName="p-button-success" incrementButtonIcon="pi pi-plus" 
                mode="decimal" min={0} max={200} maxFractionDigits={0} className="mt-1 mb-3"
            />
            <h5 className="mt-3">Maximum Distance	Floating point ( Default: -1.000000, not used )</h5> 
            <InputNumber value={maxDist} onValueChange={(e) => setMaxDist(e.value)} showButtons buttonLayout="horizontal" step={1}
                decrementButtonClassName="p-button-danger" decrementButtonIcon="pi pi-minus"
                incrementButtonClassName="p-button-success" incrementButtonIcon="pi pi-plus" 
                mode="decimal" min={-1.000000} maxFractionDigits={6} className="mt-1 mb-3"
            />
            <h5 className="mt-3">Skip Number ( Minimum: 1, Default: 1 )</h5> 
            <InputNumber value={nSkip} onValueChange={(e) => setNSkip(e.value)} showButtons buttonLayout="horizontal" step={1}
                decrementButtonClassName="p-button-danger" decrementButtonIcon="pi pi-minus"
                incrementButtonClassName="p-button-success" incrementButtonIcon="pi pi-plus" 
                mode="decimal" min={1}  maxFractionDigits={0} className="mt-1 mb-3"
            />
            <div className="flex w-full justify-content-center mt-4 mb-6">
              <Button
                className="button"
                loading={isWorking}
                disabled={isWorking}
                label={t('CALCULATE_VARIOGRAM')}
                icon="pi pi-wrench"
                onClick={() => { calculateVariogram(); }}
              />
            </div>
          </Card>
        </div>    
        <div className="flex md:w-6 sm:w-full">
          { variogram && (
            <VariogramGraph data={variogram} />
          )}  
          { !variogram && message && (
            <div className="flex flex-column align-content-center m-2">
              <h5 className="flex justify-content-center w-full text-cyan-800">{message}</h5>
            </div>
          )}  
        </div>
      </div>
      )}
      <div className="flex flex-row justify-content-center w-full gap-3">
        <Button
          className="button"
          loading={isWorking}
          disabled={isWorking}
          type="submit"
          label={t('BACK_CONFIGURATION')}
          icon="pi pi-trash"
          onClick={() => { backToConfiguration(); }}
        />
        <Button
          className="button"
          loading={isWorking}
          disabled={isWorking}
          type="submit"
          label={t('GENERATE_DATASETS')}
          icon="pi pi-save"
          onClick={() => { finalizeDataset(); }}
        />
      </div>
      </>
      )}
    </div>  
  );
}

export async function getStaticProps(context) {
  return {
    props: {       
      messages: (await import(`../translations/${context.locale}.json`)).default
    },
  }
}


/*
{
  "category": "location"
}
*/