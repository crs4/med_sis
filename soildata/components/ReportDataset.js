"use client"

import { point, featureCollection, feature, toMercator } from '@turf/turf';
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

const PointsDatasetMap = dynamic(() => import("./map/PointsDatasetMap"), { ssr:false })

export default function ValidateDataset( { dataset, setDataset })  { 
  const models = [ 
    { name: 'linear', formula: 'a + b * x'}, 
    { name: 'power', formula: 'a + b * x^k'}, 
    { name: 'square', formula: 'a + b * sqrt(x)'}, 
    { name: 'logarithmic', formula: 'a + b * ln(1 + x)'}, 
    { name: 'gaussian', formula: 'n + (s-n) * (1 - exp(-(x/r)^2))'}
  ]
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  const [isWorking, setIsWorking] = useState(false);
  const [workDataset, setWorkDataset] = useState(dataset);
  const [variogram, setVariogram] = useState(null);
  const [kPoints, setKPoints] = useState(null);
  const [kriging, setKriging] = useState(null);
  const [maxDist, setMaxDist] = useState(0);
  const [nClasses, setNClasses] = useState(100); 
  const [nSkip, setNSkip] = useState(1); 
  const [model, setModel] = useState(models[0]);
  const [descriptors, setDescriptors] = useState([]);
  const [message, setMessage] = useState('');
  
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
      if ( len < 2 )
        _descriptors.push({ name: "Warning", value: "too few points to perform the interpolation" })
      else if ( len < 20 )
        _descriptors.push({ name: "Warning", value: "very few points to perform the interpolation" })   
    }
    else {
      _descriptors.push({ name: "Aggregated points", value: 0 })
      _descriptors.push({ name: "Warning", value: "too few points to perform the interpolation" })
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
 
  function initKriging (k) {
    setKriging(k);
    workDataset.kriging = k;
    setWorkDataset(workDataset); 
  }

  function evalDepth (ft, depth_class) {
    // 0 to 20 cm OR 20 to 50 cm
    if ( !ft || !ft.properties || ft.properties.upper === null || !depth_class  )
      return 0;
    const uA = depth_class === 'depth0-20' ? 0 : 20,
          lA = depth_class === 'depth0-20' ? 20 : 50,
          uB = ft.properties.upper,
          lB = ft.properties.lower? ft.properties.lower: lA,
          l = ( lA > lB ) ? lB : lA,
          u = ( uA > uB ) ? uA : uB,
          perc = 0;      
    if ( (l - u) > 0 )   
      perc = (l-u)/(lA-uA)
    return perc; 
  }
  
  // aggregation using sixth decimal place (1 meter) in latitude and longitude
  // convert in mercator (EPSG:900913) projection
  // add abbox in mercator
  const aggregateKPoints = async () => {
    const aggregateIndex = {}
    if ( !workDataset || !workDataset.filter.points || !workDataset.filter.points.features )
      return
    workDataset.filter.points.features.forEach( ft => {
      if ( ft.geometry.coordinates ){
        const key = truncate( ft.geometry.coordinates[0] ) + '_' + truncate ( ft.geometry.coordinates[1] );
        if ( !aggregateIndex[key] )
          aggregateIndex[key] = { values: [], percentages: [] }
        const p = evalDepth( ft, workDataset.filter.depth )
        if ( ft.properties && ft.properties.value && p > 0 ){
          aggregateIndex[key].pt = toMercator( point([ft.geometry.coordinates[0],ft.geometry.coordinates[1]]) )
          aggregateIndex[key].ptgeo = point([ft.geometry.coordinates[0],ft.geometry.coordinates[1]])
          aggregateIndex[key].values.push(ft.properties.value)
          aggregateIndex[key].lat = ft.geometry.coordinates[1]
          aggregateIndex[key].lon = ft.geometry.coordinates[0]
          aggregateIndex[key].percentages.push(p)
        } 
      }  
    });
    const kFeatures = [];
    const kGeoPts = [];
    Object.keys(aggregateIndex).forEach ((d) => {
      const data = aggregateIndex[d]
      if ( data && data.pt && data.values.length ) {
        let sum = 0 
        for ( let i = 0; i < data.values.length; i += 1 )
          sum += data.values[i] / data.percentages[i]
        data.pt.properties = { id: d, lat:data.lat, lon:data.lon, value : sum / data.values.length }
        data.ptgeo.properties = { id: d, lat:data.lat, lon:data.lon, value : sum / data.values.length }
        kFeatures.push(data.pt)
        kGeoPts.push(data.ptgeo)
      }
    });
    if ( kFeatures.length ) {
      workDataset.k_params.points = featureCollection(kFeatures);
      workDataset.k_data = featureCollection(kGeoPts)
    } 
    else {
      workDataset.k_params.points = null;
      workDataset.k_data = null;
    } 
    setKPoints(workDataset.k_data)
    setWorkDataset(workDataset);
    await saveWorkDataset();  
  };

  const openList = () => {
    router.push(`/datasets`);
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
    if ( !workDataset.kriging || !workDataset.k_params || !workDataset.k_params.points || workDataset.k_params.points.length < 3 ){
      toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Too few points to perform interpolation.'});
      return;
    }
    setWorkDataset(workDataset)
    await saveWorkDataset()
    openList()
  } 

  // Re-configure   --- to NULL
  const backToConfiguration = async () => {
    workDataset.status = ProfileService.DATASET_STATUSES.CREATED
    if ( workDataset.k_params && workDataset.k_params.points )
      workDataset.k_params.points = null;
    workDataset.k_data = null;
    workDataset.k_variogram = null;
    setWorkDataset(workDataset)
    await saveWorkDataset()
  }
  
  // Calculate variogram 
  const calculateVariogram = async () => {
    setMessage('');
    if ( !workDataset.k_params || !workDataset.k_params.points || workDataset.k_params.points.length < 3 ){
      toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Too few points to perform interpolation.'});
      return;
    }
    workDataset.k_params.nClasses = nClasses;
    workDataset.k_params.model = model.formula;
    workDataset.k_params.nSkip = nSkip;
    workDataset.k_params.maxDist = maxDist; /// float
    workDataset.k_variogram = null;
    setVariogram(null);
    setWorkDataset(workDataset);
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
          max: max,
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
    else { 
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Variogram not calculated, wrong parameters or system error (try later) '}); 
      setMessage('Variogram not calculated, wrong parameters (e.g maxDist too low ) or System error (try later)')
    }
  }

  // initialize parameters for kriging if present 
  const initializeData = async () => {
    if ( !dataset )
      return;
    workDataset = dataset;
    setKriging(dataset.kriging);
    if ( dataset.k_param && dataset.k_param.maxDist )  
      setMaxDist(dataset.k_param.maxDist)
    if ( dataset.k_param && dataset.k_param.nClasses )  
      setNClasses(dataset.k_param.nClasses)
    if ( dataset.k_param && dataset.k_param.nSkip )  
      setNSkip(dataset.k_param.nSkip)
    if ( dataset.k_param && dataset.k_param.model )  
      setModel(dataset.k_param.model)
    if ( dataset.filter.points && !dataset.k_data ) { 
      await aggregateKPoints(workDataset)
    }
    else {
      setKPoints(dataset.k_data)
    }
    setWorkDataset(workDataset);
    generateDescriptor()
  }

  //OK
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    if ( dataset ) 
      initializeData()   
  }, [user]); // eslint-disable-line

  useEffect(() => {
  }, []); // eslint-disable-line

/*
Mappa
kriging toogle
diagram
kriging parameters

maxDist -> -1.0  default
nClasses -> 100  default
nSkip = -> 1 default
model = -> linear : 'a + b * x' default

variance/distance
*/
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      { !workDataset && (
      <span className="font-bold text-red-800">Error: dataset not initialized </span>
      )} 
      { workDataset && (
      <>
      <div className="card flex flex-warp text-cyan-800 w-full align-items-center"> 
        <div className="flex text-cyan-800 md:w-5 sm:w-full">
          <PointsDatasetMap fPoints={workDataset.filter.points} area={workDataset.filter.aoi} kPoints={workDataset.k_data} />
        </div>
        <div className="flex flex-column gap-2 align-content-start text-cyan-800 md:w-6 sm:w-full m-2">
          <h5 className="flex justify-content-center w-full text-cyan-800"> New Dataset Descriptor</h5>
          <DataTable value={descriptors} tableStyle={{ minWidth: '40rem' }}>
            <Column field="name" header="" style={{ width: '25%' }}></Column>
            <Column field="value" header="" ></Column>
          </DataTable>
        </div>
      </div>  
      <div className="card flex flex-row text-cyan-800 w-full justify-content-center align-items-center"> 
          <h5 className="text-cyan-800"><Checkbox onChange={e => initKriging(e.checked)} className="mr-3" checked={kriging} /> Elaborate Kriging Interpolation</h5>
      </div>    
      { workDataset.kriging && (
      <div className="card flex flex-warp text-cyan-800 w-full justify-content-center align-items-center">
        <div className="flex flex-column gap-2 text-cyan-800 md:w-5 sm:w-full">
          <Card title={t('KRIGING_INTERPOLATION')} subTitle={t('KRIGING_INTERPOLATION_SUBTILE')} 
              className="flex flex-column justify-content-center w-full gap-3 text-cyan-800">
            <h5 className="mt-3">Model ( Default: linear &quot; a + x * b &quot;  )</h5> 
            <Dropdown value={model} onChange={(e) => setModel(e.value)} options={models} optionLabel="name" 
              placeholder="Select a model" className="w-full md:w-14rem" />
            { model && (
            <h6 className="mt-1 text-cyan-800">{ model.formula }</h6> 
            )}     
            <h5 className="mt-3">Initial Number of Distance Classes ( Minimum: 2, Default: 100 )</h5> 
            <InputNumber value={nClasses} onValueChange={(e) => setNClasses(e.value)} showButtons buttonLayout="horizontal" step={1}
                decrementButtonClassName="p-button-danger" decrementButtonIcon="pi pi-minus"
                incrementButtonClassName="p-button-success" incrementButtonIcon="pi pi-plus" 
                mode="decimal" min={0} max={200} maxFractionDigits={0} className="mt-1 mb-3"
            />
            <h5 className="mt-3">Maximum Distance	Floating point ( Minimum: 0, Default: 0.000000 )</h5> 
            <InputNumber value={maxDist} onValueChange={(e) => setMaxDist(e.value)} showButtons buttonLayout="horizontal" step={10}
                decrementButtonClassName="p-button-danger" decrementButtonIcon="pi pi-minus"
                incrementButtonClassName="p-button-success" incrementButtonIcon="pi pi-plus" 
                mode="decimal" min={0} maxFractionDigits={6} className="mt-1 mb-3"
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
      <div className="flex flex-roe justify-content-center w-full gap-3">
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
          label={t('GENERATE_DATASET')}
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
