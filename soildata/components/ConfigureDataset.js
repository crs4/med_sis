"use client"

import { point, union, area, clone, bbox, bboxPolygon, feature, featureCollection, booleanIntersects, booleanPointInPolygon } from '@turf/turf';
import React, { useState, useEffect, useRef } from 'react';

import { Button } from 'primereact/button';
import { Paginator } from 'primereact/paginator';
import { Calendar } from 'primereact/calendar';
import { Checkbox } from 'primereact/checkbox';
import { RadioButton } from 'primereact/radiobutton';
import { Steps } from 'primereact/steps';
import { FileUpload } from 'primereact/fileupload';
import { Fieldset } from 'primereact/fieldset';
import { InputText } from 'primereact/inputtext';
import { ListBox } from 'primereact/listbox';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import { InputTextarea } from "primereact/inputtextarea";

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../context/user';
import ProfileService from '../service/profiles';
import TaxonomyService from '../service/taxonomies';
import BaseDatasets from '../data/basedatasets';
import dynamic from "next/dynamic";
import Loading from './Loading';

const AoiSelectionMap = dynamic(() => import("./map/AoiSelectionMap"), { ssr:false })

const PointsFilterMap = dynamic(() => import("./map/PointsFilterMap"), { ssr:false })

export default function ConfigureDataset( { isIndicators, dataset, setDataset } )  {
  const t = useTranslations('default');
  const user = useUser();
  const router = useRouter();
  const toast = useRef(null);
  // it manages configuration steps
  const [activeIndex, setActiveIndex] = useState(0);
  // working state 
  const [isWorking, setIsWorking] = useState(false);
  // working dataset
  const [workDataset, setWorkDataset] = useState(dataset)
  // SOURCES
  const srcDatasetsList = isIndicators ? 
      (dataset.context === ProfileService.DATASET_CONTEXT.AOI_SOIL_INDICATOR) ? BaseDatasets.aoiSoilIndicators : BaseDatasets.indicators
      :
      BaseDatasets.sections
  const [selectedSource, setSelectedSource] = useState(null);
  
  // MAP Points
  const [mapPoints, setMapPoints] = useState(null)

  // AOI FILTER
  // boundary datasets list (paginated)
  const [areasDatasets, setAreasDatasets] = useState(null);
  // number of boundaries dataset
  const [totalAreas, setTotalAreas] = useState(0);
  // areas typename
  const [areasTypeName, setAreasTypeName] = useState(null);
  // area
  const [selectedArea, setSelectedArea] = useState(null);
  // boundaries dataset selected 
  const [areasDataset, setAreasDataset] = useState(null);
  // areas paginator
  const [areasPage, setAreasPage] = useState(1);
  // selected A0i source type 
  const [aoiType, setAoiType] = useState(null); 
  // custom AOI file
  const aoiFileRef = useRef(null);
  const [aoiFileId, setAoiFileId] = useState(null);
  
  // FILTERED and AGREGATED points
  const [fPoints, setFPoints] = useState(null);

  // FILTER period
  const [selectedFrom, setSelectedFrom] = useState(null); 
  const [selectedTo, setSelectedTo] = useState(null); 
  
  // FILTER project
  const [projects, setProjects] = useState([]); 
  const [selectedProject, setSelectedProject] = useState(null)
   
  // FILTER laboratory method
  const [methods, setMethods] = useState([]);
  const [selectedMethod, setSelectedMethod] = useState(null)
  const [infoMethods, setInfoMethods] = useState(null);

  // FILTER survey method
  const [surMethods, setSurMethods] = useState([]);
  const [selectedSurMethod, setSelectedSurMethod] = useState(null)
  const [infoSMethods, setInfoSMethods] = useState(null);

  // FILTER point's type
  const [selectedDepth, setSelectedDepth] = useState(dataset.filter.depth);

  // FILTER point's type
  const [types, setTypes] = useState([]);
  const [selectedType, setSelectedType] = useState(null)
  const [infoTypes, setInfoTypes] = useState(null);

  const formatDate = (value) => {
    const date = new Date(value).toJSON()
    date = date.substring(0,10)
    return date
  };

  /* This reads the taxonomy's description  */
  const GetInfo = ( id, list) => {
    const info = ""
    if ( list && id )
      try {
        const e = list.filter( (i) => i.id === id )
        if ( e && e[0] )
          if ( e[0].descr )
            info = e[0].descr
          else info = "No description"      
      } catch (error) {
        console.log(error)
      }
    return info  
  }

  // This sets the Area of Interest filter 
  const setAoi = async (_area) => {
    if ( !_area || !bbox(_area) )
      _area = null
    workDataset.filter.aoi = _area;
    setWorkDataset(await filtering(workDataset))
    setSelectedArea(_area)
    if ( _area )
        toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Area of Interest selected.'});
    else toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Wrong Area of Interest selected.'});
  }

  // This sets the dataset's source points (initialization) 
  const setPoints = (points) => {
    workDataset.points = points;
    workDataset.filter.points = points;
    workDataset.k_params = {
      ...workDataset.k_params,
      epsg:  null,
      points:  null
    }
    workDataset.k_data = null;
    setWorkDataset(workDataset)
  }

  // This sets the filter for depth 
  const setDepth = (depth) => {
    workDataset.filter.depth = depth;
    setWorkDataset(workDataset);
  }

  // This sets the period filter ( to  date ) 
  const setTo = (date) => {
    if ( ( new Date(workDataset.filter.from) > date ) ){
      workDataset.filter.to = workDataset.filter.from;
      setSelectedTo(new Date(workDataset.filter.from))
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Wrong date.'});
    }  
    else {
      workDataset.filter.to = date.toJSON();
      setSelectedTo(date)
      setWorkDataset(workDataset);
      toast.current.show({ severity: 'success', summary: 'Done!', detail: 'End period selected.'});
    }
  }
  
  // This sets the period filter ( from  date )
  const setFrom = (date) => {
    if ( (new Date(workDataset.filter.to) < date ) ){
      workDataset.filter.from = workDataset.filter.to;
      setSelectedFrom(new Date(workDataset.filter.to))
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Wrong date.'});
    }  
    else {
      workDataset.filter.from = date.toJSON();
      setSelectedFrom(date)
      setWorkDataset(workDataset);
      toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Start period selected.'});
    }
  }
  
  // This sets a geonode dataset as source points dataset
  const setSource = async (sourceDS) => {
    workDataset.source = null; 
    workDataset.points = null;
    workDataset.filter.points = null;
    workDataset.k_params = {
      ...workDataset.k_params,
      epsg:  null,
      points:  null
    }
    workDataset.k_data = null;
    if ( sourceDS === null ) 
      workDataset.src_typename = null;
    else {
      workDataset.source = sourceDS.name;
      if (sourceDS.typename){ 
        workDataset.src_typename = 'geonode:' + sourceDS.typename;
        if ( workDataset.context === ProfileService.DATASET_CONTEXT.SOIL_INDICATOR )
          await loadPoints(sourceDS.typename)
        else 
          await loadIndicatorPoints(sourceDS.name,sourceDS.typename)    
      }
    }
    setWorkDataset(workDataset)
    saveWorkDataset()
    setSelectedSource(sourceDS)
  };
  
  // This extracts data to filter the source points dataset
  const extractData = async (points) => {
    let prjs = ["All projects"]
    let sms = ["All methods"]
    let lms = ["All methods"]
    let ts = ["All types"]
    let tax = null
    let _from = null;
    let _to = null;
    if (!points)
      return;
    /// read projects, survey and laboratory methods
    for ( let i=0; i< points.features.length; i+= 1 ){
      const props = points.features[i].properties
      try {
        if ( isIndicators && props.method ) {
          if ( props.method.indexOf(':') > 0 ) 
          // unique value if set
            tax = props.method.substring(0,props.method.indexOf(':'))
          lms.push(props.method)
        }
        if ( props.project && prjs.indexOf(props.project) === -1 )
          prjs.push(props.project)
        if ( props.survey_m_id && sms.indexOf(props.survey_m_id) === -1 )
          sms.push( props.survey_m_id )
        if ( props.point_type && ts.indexOf(props.point_type) === -1 )
          ts.push( props.point_type )
        if ( props.date ) {
          const d = new Date(props.date)
          if ( _from === null || _from > d )
            _from = d;
          if ( _to === null || _to  < d )
            _to = d;
        }
      }
      catch (e) {
        console.log(e)
        console.log('Errors in feature ' + i) 
      } 
    }
    if ( tax ) {
      const response = await TaxonomyService.listValues(document.cookie, tax)
      if ( response && response.ok && response.data )
        setInfoMethods(response.data)
    }
    setSelectedFrom(_from)
    setSelectedTo(_to)
    setProjects(prjs);
    setMethods(lms);
    setSurMethods(sms);
    setTypes(ts)  
  }

  // This reset the source points dataset
  const resetPoints = () => {
    setPoints (null);
    setProjects([{ descr: "All projects"}]);
    setMethods([{ descr: "All methods"}]);
    setSurMethods([{ descr: "All methods"}]);
    setTypes([{ descr: "All types"}]);
  }

  // It aggregates points to manage points with same position
  const aggregatePoints = async (_points) => {
    try {
      // first step creates an aggragated index using poition 
      const aggregateIndex = {}
      if ( !_points || !_points.features )
        return
      _points.features.forEach( ft => {
        if ( ft.geometry.coordinates ){
          const key = ft.geometry.coordinates[0] + '_' + ft.geometry.coordinates[1] ;
          if ( ft.properties ) {
            if ( !aggregateIndex[key] )
              aggregateIndex[key] = { geometry: ft.geometry, ids: [], values: [], lat : ft.geometry.coordinates[1], lon : ft.geometry.coordinates[0] }
            // read the feature id
            aggregateIndex[key].ids.push(ft.properties.id)
            // for soil indicators the value is the field "value"
            // for point soil data sections the value is the field "date"
            if ( ft.properties.value )
              aggregateIndex[key].values.push(" value"+ft.properties.value)
            else aggregateIndex[key].values.push(" date" + ft.properties.date)
          }   
        }  
      });
      const aFeatures = [];
      /// second step generates features to display in map with a popup
      Object.keys(aggregateIndex).forEach ((d) => {
        let panel = '<div class="flex flex-column justify-content-center text-cyan-500 font-bold">';
        const pdata = aggregateIndex[d];
        if ( pdata && pdata.geometry ) {
          const ft = feature (pdata.geometry)
          panel += '<div class="justify-content-center text-blue-500 font-bold">Aggregation of ' + pdata.ids.length + ' Points '
          panel += '<div>Latitude ' + pdata.lat + '</div>';
          panel += '<div>Longitude ' + pdata.lon + '</div>';
          panel += '<div>Values: '
          for ( let i = 0; i < pdata.ids.length; i+=1 ) {
            panel += '<div>' + pdata.ids[i]  ;
            if ( pdata.values.length > i )
              panel += '; ' + pdata.values[i]
            panel += '</div>'
          }  
          panel += '</div>'  
          ft.properties = { popup: panel } 
          aFeatures.push(ft)
        }
      });
      return featureCollection(aFeatures) 
    } catch (error) {
      console.log(error)  
    }
    return null
  }

  // get the mediana of a set of values of a numeric attribute in the points features properties 
  const getMediana = ( pts, element ) => {
    const array = []
    if ( pts ){
      pts.forEach ((ft) => {
        if ( !isNaN( parseFloat( ft.properties[element] ) ) )                
          array.push( parseFloat( ft.properties[element] ) )
      })
      if (array.length === 0) return null;
      const ordered = [...array].sort((a, b) => a - b);
      const middle = Math.floor(ordered.length / 2);
      // if the ordered size is an odd number return the central value
      if (ordered.length % 2 !== 0) 
        return ordered[middle];
      // if the odered size is an even number calculates the mediana using the media of the 2 central values 
      return (ordered[middle - 1] + ordered[middle]) / 2;
    } 
    return null 
  }

  // Enrichment factor calculation (!!!after AOI filter)
  const elaborateEF = ( points, elementA, elementB ) => {
    const efPoints = []
    if ( points && points.length ){
      const medianaA = getMediana( points, elementA)
      const medianaB = getMediana( points, elementB)
      
      if ( medianaA && medianaB ) {
        points.forEach ((ft) => {
          if ( !isNaN( parseFloat(ft.properties[elementA]) ) && !isNan( parseFloat(ft.properties[elementB]) ) ){ 
            ft.properties.value = ( parseFloat(ft.properties[elementA]) / parseFloat(ft.properties[elementB]) ) / ( medianaA / medianaB )                  
            efPoints.push(ft)
          }
        })
      }
    }
    return efPoints;          
  }
      
  // This loads and sets the source points from a catalogue dataset
  const loadIndicatorPoints = async (indicator, typename) => {
    try {
      const token = user.userData.access_token;
      setIsWorking(true);
      const response = await ProfileService.getDataset( 'geonode:' + typename, null, token )
      setIsWorking(false);
      if ( response && response.ok && response.data && response.data.features ){
        const labdata_points = response.data;
        const new_points = []
        /////// filter feature properties  
        const elemA = null, elemB = null
        labdata_points.features.forEach ( (ft) =>  {
          if ( ft.properties )  {
            /// set base attributes
            const new_props = {
              id: ft.properties.id,
              point_id: ft.properties.point_id,
              point_type: ft.properties.point_type,
              project:ft.properties.project,
              date: ft.properties.date,
              survey_m_id: ft.properties.survey_m_id,
              l_number: ft.properties.l_number,
              horizon: ft.properties.horizon,
              upper: ft.properties.upper,
              lower: ft.properties.lower,
            }
            switch (indicator) {
              case 'Enrichment factor - Pb' :
                new_props.pb = ft.properties.pb                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_pb_id
                elemA = 'pb'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Hg" :
                new_props.hg = ft.properties.hg                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_hg_id
                elemA = 'hg'
                elemB = 'zn'
                new_points.push(ft)
                break;
              case "Enrichment factor - Cd" :
                new_props.cd = ft.properties.cd                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_cd_id
                elemA = 'cd'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Ni" :
                new_props.ni = ft.properties.ni                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_ni_id;
                elemA = 'ni'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Cu" :
                new_props.cu = ft.properties.cu                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_cu_id
                elemA = 'cu'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Sb" :
                new_props.sb = ft.properties.sb                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_sb_id
                elemA = 'sb'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Mn" :
                new_props.mn = ft.properties.mn                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_mn_id
                elemA = 'mn'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Cr" :
                new_props.cr = ft.properties.cr                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_cr_id
                elemA = 'cr'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Co" :
                new_props.co = ft.properties.co                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_co_id
                elemA = 'co'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - V" :
                new_props.v = ft.properties.v                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_v_id
                elemA = 'v'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - As" :
                new_props.as_value = ft.properties.as_value                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_as_id
                elemA = 'as_value'
                elemB = 'zn'
                new_points.push(ft)
              break;
              case "Enrichment factor - Zn" :
                new_props.cu = ft.properties.cu                
                new_props.zn = ft.properties.zn
                new_props.method = ft.properties.met_zn_id
                elemA = 'zn'
                elemB = 'cu'
                new_points.push(ft)
              break;
            }  
            ft.properties = new_props
          }  
        })
        if ( elemA && elemB )
          new_points = elaborateEF(new_points, elemA, elemB )
        else new_points = []
        setPoints (featureCollection(new_points));
        await extractData (featureCollection(new_points));
        setWorkDataset(await filtering(workDataset));
        toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Source points has been loaded and evaluated.'});
      }
      else {
        resetPoints()
        toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Source points not available.'}); 
      }
    } catch (e) {
      resetPoints()
      console.log(e);
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'System Error, Errors loading source points.'});
    } 
  }

  // This loads and sets the source points from a catalogue dataset
  const loadPoints = async (typename) => {
    try {
      const token = user.userData.access_token;
      setIsWorking(true);
      const response = await ProfileService.getDataset( 'geonode:' + typename, null, token )
      setIsWorking(false);
      if ( response && response.ok && response.data && response.data.features ){
        const points = response.data; 
        setPoints (points);
        await extractData (points);
        setWorkDataset(await filtering(workDataset));
        toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Source points has been loaded.'});
      }
      else {
        resetPoints()
        toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Source points not available.'}); 
      }
    } catch (e) {
      resetPoints()
      console.log(e);
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'System Error, Errors loading source points.'});
      setIsWorking(false);
    }  
  }
 
  // This performs filtering using the Filter object
  const filtering = async ( _workDataset) => {
    let filtered = []
    try {
      for ( let l=0; l < _workDataset.points.features.length; l += 1){
        let ok = false;
        let pt = _workDataset.points.features[l];
        let props = pt.properties;
        // AOI filter   
        if ( _workDataset.filter.aoi ){
          for ( let x=0; x < _workDataset.filter.aoi.features.length; x += 1)
            if ( booleanPointInPolygon( pt, _workDataset.filter.aoi.features[x] ) )
              ok = true;
        }
        if ( ok && props ){
          // period filter
          if (
            ( _workDataset.filter.from && 
              ( new Date (_workDataset.filter.from)) >= new Date( props.date ) )  ||
            ( _workDataset.filter.to && 
              ( new Date (_workDataset.filter.to)) <= new Date( props.date ) ) ) 
          { 
            ok = false
          }
          
          // depth filter
          if ( _workDataset.filter.depth )
            if ( ( _workDataset.filter.depth === ProfileService.FILTER_DEPTH.DEPTH0_20 ) && ( props.upper > 20 ))
              ok = false
            else if ( ( _workDataset.filter.depth === ProfileService.FILTER_DEPTH.DEPTH20_50 ) &&
                      ( props.upper === null || props.upper > 50 ||
                        ( props.lower != null && props.upper > props.lower ) ||
                        ( props.lower != null && props.lower < 20 ) ) )
          { 
            ok = false
          }
          // project filter
          if ( _workDataset.filter.project &&  
               _workDataset.filter.project !== props.project &&
               _workDataset.filter.project !== "All projects" )
          { 
            ok = false
          }
          // point's type filter
          if ( _workDataset.filter.type && 
              _workDataset.filter.type !== props.type &&
              _workDataset.filter.type !== "All types" )
          { 
            ok = false
          }
          // measure method filter
          if ( isIndicators && _workDataset.filter.method && 
              _workDataset.filter.method !== props.method &&
              _workDataset.filter.method !== "All methods" )
          { 
            ok = false
          }
          
          // measure method filter
          if ( _workDataset.filter.surMethod && 
              _workDataset.filter.surMethod !== props.survey_m_id &&
              _workDataset.filter.surMethod !== "All methods" )
          { 
            ok = false
          }   
        }
        if (ok)
          filtered.push(pt)    
      }
      _workDataset.filter.points = featureCollection(filtered);
      const aggregatedPts = await aggregatePoints (_workDataset.filter.points)
      setMapPoints( aggregatedPts )
    } 
    catch (error) {
      console.log(error)
      _workDataset.filter.points = null
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors filtering points' , life: 3000});  
    } 
    return _workDataset
  };
  
  // This saves the dataset on backoffice db
  const saveWorkDataset = async () => {
    try {
      // save needs at least points  
      if ( !workDataset || !workDataset.id || !workDataset.name === "" )
        return;
      // reset post configuration parameters 
      setIsWorking(true)
      const response = await ProfileService.update( document.cookie, workDataset.id, workDataset, 'datasets'  );
      setIsWorking(false)
      if ( response && response.ok ) { 
        toast.current.show({severity: 'success', summary: 'Success!', detail: 'Dataset configuration has been saved' , life: 3000});
        const newData = response.data;
        setWorkDataset(newData)
        setDataset(newData)
        return true; 
      } 
      else toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset configuration' , life: 3000});
    } catch (error) {
      console.log(error)
      setIsWorking(false)
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset' , life: 3000}); 
    }
    return false;
  } 

  // this saves the dataset and go to the next step
  const saveAndContinue = async (to) => {
    if ( !workDataset.points || !workDataset.points.features || !workDataset.points.features.length  )
      return
    saveWorkDataset()
    setActiveIndex(to);
  }

  // Go to Validate page
  const finalizeDataset = async () => {
    workDataset.status = ProfileService.DATASET_STATUSES.CONFIGURED
    setWorkDataset(workDataset)
    await saveWorkDataset()
  } 
  
  // Configuration Steps
  const items = [
    { label: t('DS_DEFINITON'), command: (_e) => {setActiveIndex(0);} },
    { label: t('DS_AOI'), command: (_e) => {setActiveIndex(1);}},
    { label: t('DS_FILTERS'), command: (_e) => {setActiveIndex(2);} }, 
  ];

  let StepHeaders = ['Source', 'Area of Interest', 'Filters'];

  // This loads the boundaries datasets list  
  const loadAreasDatasets = async  ( ) => { 
    try {
      setAreasDatasets(null);
      setIsWorking(true)
      const respAreas = await ProfileService.getDatasetsByCategory('boundaries', document.cookie);
      setIsWorking(false)
      if ( respAreas && respAreas.ok && respAreas.data ) {
        setAreasDatasets(respAreas.data)
        if ( respAreas.data.total )
          setTotalAreas(respAreas.data.total)
      }     
    } catch (error) {
      console.log(error)
      setIsWorking(false) 
    }   
  }
  
  // This uploads a geoJSON file to set the AOI filter 
  const uploadRoiFile = async ({files}) => {
    try {
      // validate geometry first feature
      // Add bbox, area to new geojson
      const [file] = files;
      if ( file ) 
      {
        const readFilePromise = (aoiFile) => new Promise((resolve, reject) => {
          const readFile = new FileReader();
          readFile.onload = (event) =>  { 
            const contents = event.target.result;
            try { 
            /// only one feature!!!
              const geojson = JSON.parse(contents.replaceAll('/n',''));
              let ftCl = null
              let oneFeature = null;
              // verify data
              if ( geojson && area( geojson ) ) {
                if ( geojson.type === 'Feature' ) 
                  ftCl = featureCollection([geojson])
                else if ( geojson.features.length > 2)  
                  ftCl = featureCollection([ union( geojson )]) 
                else  
                  ftCl = geojson
              }
              else {
                reject('wrong json file');
              }
              ftCl.bbox = bbox(ftCl);
              resolve(ftCl);
            } catch (error) {
              reject('errors reading json file');
            }
          };
          readFile.onerror = (error) => {
            reject(error);
          };
          readFile.readAsText(aoiFile);
        });     
        const result = await readFilePromise(file)
        if ( result ) {   
          await setAoi(result)
          toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Your area of interest has been uploaded.'});
          return;
        }
        else toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Errors uploading file.'});
      }
    } catch (error) {
      console.log(error)
    }
    toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Errors uploading file'}); 
  };

  // This initializes the laboratory method filter
  const initializeData = async () => {
    try { 
      if (workDataset.points) {
        await extractData(workDataset.points)
        setWorkDataset(await filtering(workDataset));
      };
      if ( workDataset.filter && workDataset.filter.aoi )
        setSelectedArea(workDataset.filter.aoi)
      // This loads the taxonomy for the Point Soil Data Types needed by filters   
      const response = await TaxonomyService.listValues(document.cookie, 'POINT_DATA_TYPES')
      if ( response && response.ok && response.data )
          setInfoTypes(response.data);
      // This loads the taxonomy for the survey methods needed by filters   
      const response2 = await TaxonomyService.listValues(document.cookie, 'SURVEY_METHODS')
      if ( response2 && response2.ok && response2.data )  
          setInfoSMethods(response2.data)
      setSelectedFrom (new Date(workDataset.filter.from))
      setSelectedTo (new Date(workDataset.filter.to))
      setSelectedDepth (workDataset.filter.depth)
      setSelectedMethod(workDataset.filter.method)
      setSelectedType(workDataset.filter.type)
      setSelectedSurMethod(workDataset.filter.surMethod)
      setSelectedProject(workDataset.filter.project)
    } catch (error) {
      console.log(error)
    }  
  }

  const addAreasToMap  = (typename) => {
    setAreasTypeName(typename);
    toast.current.show({ severity: 'info', summary: 'Info', detail: 'Loading areas'}); 
  }

  const refreshMap = async () => { 
    setWorkDataset(await filtering(workDataset))  
  }

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    if ( workDataset && workDataset.points )
      initializeData()
    loadAreasDatasets()
  }, [user, dataset]); // eslint-disable-line
  
  const aoiSourceTypes = [
    { key: 'custom', name: 'Custom Polygon' },
    { key: 'dataset', name: 'Boundaries Catalogue dataset'}
  ]
  
  return (
    <div className="layout-dashboard">
    <Toast ref={toast} />
      {(!workDataset || !workDataset.filter) && (
      <span className="font-bold text-red-800"> Error: dataset or filter not initialized </span>
      )} 
      { workDataset && workDataset.filter  && (
      <>
      <Steps model={items} activeIndex={activeIndex} readOnly className="mb-4" />
        { activeIndex === 0  && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          <div className="flex flex-column w-full m-2 align-items-center justify-content-center">
            <Fieldset className="w-full" legend={t('NAME')}>
              <InputText className="w-full" value={workDataset.name} 
                onChange={(e) => setWorkDataset({ ...workDataset, name: e.target.value })} />
            </Fieldset>
            <Fieldset className="w-full" legend={t('DS_SOURCE')}>
            { workDataset && workDataset.source  && (
              <>
              { isWorking  && (
                <Loading title="loading point"/>
              )}
              { !isWorking && (

              <div className="flex flex-column gap-2 align-items-center  w-full">
                <Button
                  icon='pi pi-trash'
                  type='button'
                  disabled={ isWorking }
                  severity='danger'
                  onClick={() => { setSource (null); setWorkDataset({ ...workDataset, source: null }) }}
                />
                <h5 className="font-bold text-800">Selected source: <span className="font-bold text-cyan-800">{workDataset.source}</span></h5>   
                { workDataset.points && workDataset.points.features && (
                  <h5 className="font-bold text-800">Points: <span className="font-bold text-cyan-800">
                    { ( workDataset.points.features ? workDataset.points.features.length : 0 ) }
                  </span></h5>
                )}
                { !workDataset.points || !workDataset.points.features && ( 
                  <h5 classname="font-bold text-cyan-800">{t('EMPTY')}</h5>
                )}

                { selectedSource && selectedSource.abstract && (
                  <InputTextarea id="description" value={selectedSource.abstract} disabled rows={5} cols={30} />
                )}
              </div>
              )}
              </>
            )}
            { workDataset.source === null && (
              <div className="card flex flex-column gap-3 align-items-center mt-3">
              { isWorking && (
                <Loading title="Loading indicators"/>
              )}
              { !isWorking && srcDatasetsList && srcDatasetsList.length > 0 && (
                <>
                  <h6 className="md:w-30rem surface-200 font-bold text-cyan-800 p-3 shadow-2">Base Datasets Sources</h6>
                  <Dropdown value={selectedSource} 
                    onChange={(e) => { setSource(e.value); setWorkDataset({ ...workDataset, source: null }) }} 
                    options={srcDatasetsList} 
                    optionLabel="name" 
                    placeholder="Select a Source" 
                    filter filterDelay={400} 
                    className="w-full md:w-30rem font-bold text-cyan-800" />
                </>
              )}
              { !isWorking && ( !srcDatasetsList || srcDatasetsList.length === 0) && (
                <h5 classname="font-bold text-cyan-800">{t('EMPTY')}</h5>
              )}
              </div>
            )}
            </Fieldset>
            <div class="flex justify-content-center w-full m-3">
              <Button
                label={t("SAVE_CONTINUE")}
                icon='pi pi-save'
                type='button'
                disabled={ isWorking || !workDataset.points || !workDataset.points.features || !workDataset.points.features.length }
                className='mt-4 flex'
                onClick={() => { saveAndContinue(1) }} 
              />
            </div> 
          </div>
        </div>
        )}
        { activeIndex === 1 && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full justify-content-center">
          <Fieldset className="w-full justify-content-center" legend={t('DS_AOI_SELECTION')}>
            { !workDataset.filter.aoi && (
            <>  
            <div className="flex flex-wrap justify-content-center w-full gap-3">
              { aoiSourceTypes.map((aoiSourceType) => { return (
                <div key={aoiSourceType.key} className="flex align-items-center">
                  <RadioButton inputId={aoiSourceType.key} name="category" value={aoiSourceType} onChange={(e) => setAoiType(e.value)} checked={aoiType?.key === aoiSourceType.key} />
                  <label htmlFor={aoiSourceType.key} className="ml-2">{aoiSourceType.name}</label>
                </div>
              )})}
            </div>
            { aoiType?.key === "dataset" && (
              <div className="flex flex-column align-items-center justify-content-center w-full mt-3">
                { isWorking && (
                  <Loading title="Loading..."/>
                )}
                { !isWorking && areasDatasets && areasDatasets.datasets && areasDatasets.datasets.length && (
                  <>
                  <h6 className="surface-200 font-bold text-cyan-800 p-3 shadow-2">{t('DS_AREAS')}</h6>
                  <Dropdown value={areasDataset} disabled={isWorking} onChange={(e) => setAreasDataset(e.value)} options={areasDatasets.datasets}
                   optionLabel="name" placeholder="Select a dataset" filter filterDelay={400} className="w-full m-3 md:w-30rem font-bold text-cyan-800" />
                  <Button
                    label={t('ADD_TO_MAP')}
                    icon='pi pi-map'
                    type='button'
                    disabled={ isWorking || !areasDataset || !areasDataset.alternate }
                    onClick={() => {addAreasToMap(areasDataset.alternate); }}
                  />
                  </> 
                )}
                { ( !isWorking && ( !areasDatasets?.datasets || !areasDatasets.datasets?.length ) ) &&  (
                  <h6 className="font-bold text-cyan-800">No dataset available</h6>
                )}
              </div>
            )}  
            { aoiType?.key === "custom" && (
              <div className="flex flex-column">
                <span classname="font-bold text-cyan-800">Upload Custon Polygon:</span>
                <FileUpload 
                  disabled={aoiFileId !== null || isWorking}
                  id="file"
                  ref={aoiFileRef}
                  accept='.json, .geojson'
                  chooseLabel={t('CHOOSE_FILE')}
                  mode="basic"
                  multiple={false}
                  customUpload
                  auto
                  className='mb-4 mr-2 mt-4'
                  uploadHandler={uploadRoiFile}
                /> 
                {(aoiFileId !== null) && (
                <div class="flex flex-row mt-4 mb-4"> 
                  <Button
                      label={t('RESET')}
                      icon='pi pi-plus'
                      type='button'
                      disabled={ isWorking }
                      className='mr-2 mt-4 flex mr-4'
                      onClick={() => { resetFile(); }}
                  />
                  <Message classname="font-bold" severity="success" content={'File: ' + aoiFileId} /> 
                </div>
                )}  
              </div>     
            )}
            </>
            )}  
            { workDataset.filter.aoi && (
              <> 
              <div className="flex flex-column gap-2 align-items-center  w-full">
                <Button
                  icon='pi pi-trash'
                  type='button'
                  disabled={ isWorking }
                  severity='danger'
                  onClick={() => { setAoi (null) }}
                />
                <h5 className="font-bold text-800">{t('AOI_SELECTED')}</h5>
                { workDataset.filter.points && (
                  <h5 className="font-bold text-cyan-800">
                    { workDataset.filter.points.features ? workDataset.filter.points.features.length : 0 } Filtered Points: </h5>
                )} 
              </div>
              </>
            )}  
          </Fieldset>
          { workDataset && workDataset.points && (
          <AoiSelectionMap  token={user.userData.access_token} areasTypeName={areasTypeName} points={workDataset.points} area={selectedArea} setAoi={setAoi} />
          )} 
          <div class="flex justify-content-center w-full m-3">
            <Button
              label={t('BACK')}
              icon='pi pi-trash'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4 justify-content-start'
              onClick={() => { setActiveIndex(0); }}
            />
            <Button
              label={t("SAVE_CONTINUE")}
              icon='pi pi-save'
              type='button'
              disabled={ isWorking || !selectedArea }
              className='mt-4 flex justify-content-end'
              onClick={() => { saveAndContinue(2) }} 
            /> 
          </div>
        </div>
        )}
        { activeIndex === 2 && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full justify-content-center">
        {( !workDataset.filter.points || !workDataset.filter.aoi ) && (
          <span className="font-bold text-red-800">Error: no filtered points or Aoi not selected </span>
        )}
        { workDataset.filter.points && workDataset.filter.aoi && ( 
          <>
          <h5 className="font-bold text-cyan-800"> 
            { workDataset.filter.points.features ? workDataset.filter.points.features.length : 0 } Filtered Points</h5>
          <h5 className="font-bold text-cyan-800"> 
            { (mapPoints && mapPoints.features) ? mapPoints.features.length : 0 } Aggregated Points</h5> 
          <PointsFilterMap points={mapPoints} area={workDataset.filter.aoi} />
          <div class="flex justify-content-center w-full m-3">
            <Button
              label={t('APPLY_FILTER')}
              icon='pi pi-wrench'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => refreshMap() }
            /> 
          </div>
          <Fieldset className="w-full m-2" legend={t('PERIOD')}>
            <h5 className="font-bold text-cyan-800">Select a period or None for all periods</h5>
            <div className="flex flex-row gap-2 font-bold text-cyan-800 w-full align-items-center mt-3">
              <span className="flex w-3 m-2 justify-content-end">{t('FROM_DATE')}</span>
              <Calendar value={ selectedFrom } onChange={ (e) => setFrom(e.value) } showIcon />
            </div>  
            <div className="flex flex-row gap-2 font-bold text-cyan-800 w-full mt-3">
              <span className="flex w-3 m-2 justify-content-end">{t('TO_DATE')}</span>
              <Calendar value={ selectedTo } onChange={(e) => setTo(e.value)} showIcon />
            </div>  
          </Fieldset>
          <Fieldset className="w-full m-2" legend={t('DEPTH')}>  
            <div className="flex flex-row gap-3">
              <RadioButton inputId="none" name="depth" value="none" 
                onChange={ (e) => 
                  { setSelectedDepth(null);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , depth: null }})}} 
                checked={ workDataset.filter.depth === null} />
              <label htmlFor="none" className="ml-2">All depths</label>
              <RadioButton inputId="DEPTH0_20" name="depth" value="DEPTH0_20" 
                onChange={ (e) => 
                  { setSelectedDepth(ProfileService.FILTER_DEPTH.DEPTH0_20);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , depth: ProfileService.FILTER_DEPTH.DEPTH0_20 }})}} 
                checked={ selectedDepth === ProfileService.FILTER_DEPTH.DEPTH0_20} />
              <label htmlFor="DEPTH0_20" className="ml-2">Upper: 0 cm; Lower: 20 cm</label>
              <RadioButton inputId="DEPTH20_50" name="depth" value="DEPTH20_50" 
                onChange={ (e) => 
                  { setSelectedDepth(ProfileService.FILTER_DEPTH.DEPTH20_50);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , depth: ProfileService.FILTER_DEPTH.DEPTH20_50 }})}} 
                checked={ selectedDepth === ProfileService.FILTER_DEPTH.DEPTH20_50} />
              <label htmlFor="DEPTH20_50" className="ml-2">Upper: 20 cm; Lower: 50 cm</label>
            </div>
          </Fieldset>
          <Fieldset className="w-full m-2" legend={t('TYPE')}>
            <div className="flex flex-column gap-1">
              <h5 className="font-bold text-cyan-800">Select a point soil data type or All types</h5>
              <Dropdown value={selectedType} 
                onChange={ (e) => 
                  { setSelectedType(e.value);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , type: e.value }})}} 
                options={types} placeholder="select a type" className="md:w-30rem font-bold mt-1 text-cyan-800" />
              {( selectedType && (
                <h5 className="font-bold text-cyan-800" >{ GetInfo( selectedType, infoTypes ) }</h5>
              ))}
            </div>
          </Fieldset> 
          <Fieldset className="w-full m-2" legend={t('SURMETHOD')}>
            <div className="flex flex-column gap-1">
              <h5 className="font-bold text-cyan-800">Select a survey method or All methods</h5>
              <Dropdown value={selectedSurMethod} 
                onChange={ (e) => 
                  { setSelectedSurMethod(e.value);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , surMethod: e.value }})}} 
                options={surMethods} placeholder="select a survey method" className="md:w-30rem mt-1 font-bold text-cyan-800" />
              {( selectedSurMethod && (
                <h5 className="font-bold text-800" >{ GetInfo( selectedSurMethod, infoSMethods ) }</h5>
              ))}
            </div> 
          </Fieldset>
          <Fieldset className="w-full m-2" legend={t('PROJECT')}>
            <div className="flex flex-column gap-1">
              <h5 className="font-bold text-cyan-800">Select a project or All projects</h5>
              <Dropdown value={selectedProject} 
                onChange={ (e) => 
                  { setSelectedProject(e.value);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , project: e.value }})}} 
                options={projects} placeholder="select a project" className="md:w-30rem mt-1 font-bold text-cyan-800" />
            </div>
          </Fieldset>
          { isIndicators && (
          <Fieldset className="w-full m-2" legend={t('METHOD')}>
            <div className="flex flex-column gap-1">
              <h5 className="font-bold text-cyan-800">Select a laboratory method or All methods</h5>
              <Dropdown value={selectedMethod} 
                onChange={ (e) => 
                  { setSelectedMethod(e.value);
                    setWorkDataset({ ...workDataset, filter: { ...workDataset.filter , method: e.value }})}} 
                options={methods} placeholder="select a method" className="md:w-30rem mt-1 font-bold text-cyan-800" />
              {( selectedMethod && (
                <h5 className="font-bold text-cyan-800" >{ GetInfo( selectedMethod, infoMethods ) }</h5>
              ))}
            </div>
          </Fieldset>
          )}
          </>
        )}
          <div class="flex justify-content-center w-full m-3">
            <Button
              label={t('BACK')}
              icon='pi pi-trash'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4 justify-content-start'
              onClick={() => { setActiveIndex(1); }}
            />
            <Button
              label={t("SAVE_CONFIGURATION")}
              icon='pi pi-save'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex justify-content-end'
              onClick={() => { finalizeDataset() }} 
            /> 
          </div>
        </div>              
        )}
      </>
      )}  
    </div>
  )
}

export async function getStaticProps(context) {
  return {
    props: {       
      messages: (await import(`../translations/${context.locale}.json`)).default
    },
  }
}
