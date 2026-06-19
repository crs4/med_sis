"use client"

import { point, union, area, clone, bbox, bboxPolygon, featureCollection, booleanIntersects, booleanPointInPolygon } from '@turf/turf';
//import { booleanPointInPolygon } from "@turf/boolean-point-in-polygon";
//booleanIntersects
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
import { ProfileService } from '../service/profiles';
import TaxonomyService from '../service/taxonomies';
import BaseDatasets from '../data/basedatasets';
import dynamic from "next/dynamic";
import Loading from './Loading';

const AoiSelectionMap = dynamic(() => import("./map/AoiSelectionMap"), { ssr:false })

const PointsFilterMap = dynamic(() => import("./map/PointsFilterMap"), { ssr:false })

export default function ConfigureDatasetPoint( { dataset, setDataset })  {
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
  const srcDatasetsList = BaseDatasets.sections
  const [selectedSource, setSelectedSource] = useState(null)
  

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
  
  // FILTERED points
  const [fPoints, setFPoints] = useState(null);

  
  // FILTER project
  const [projects, setProjects] = useState([]); 
  const [selectedProject, setSelectedProject] = useState(null)

  // FILTER survey method
  const [surMethods, setSurMethods] = useState([]);
  const [selectedSurMethod, setSelectedSurMethod] = useState(null)
  const [infoSMethods, setInfoSMethods] = useState(null);

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
  const setAoi = (_area) => {
    workDataset.filter.aoi = _area;
    setWorkDataset(workDataset)
    filtering()
    setSelectedArea(_area)
  }

  // This sets the dataset's source points (initialization) 
  const setPoints = (points) => {
    workDataset.points = points;
    setFPoints(points)
    workDataset.filter.points = points;
    setWorkDataset(workDataset)
  }
  
  // This sets the name of dataset 
  const setName = (name) => {
    workDataset.name = name;
    setWorkDataset(workDataset);
  }  

  // This sets the filter for depth 
  const setDepth = (depth) => {
    workDataset.filter.depth = depth;
    setWorkDataset(workDataset);
  }

  // This sets the period filter ( to  date ) 
  const setTo = (date) => {
    const d = new Date(date)
    workDataset.filter.to = d.toString();
    setWorkDataset(workDataset);
  }
  
  // This sets the period filter ( from  date )
  const setFrom = (date) => {
    const d = new Date(date)
    workDataset.filter.from = d.toString();
    setWorkDataset(workDataset);
  }
  
  // This sets a geonode dataset as source points dataset
  const setSource = async (sourceDS) => {
    if ( sourceDS === null ) {
      workDataset.source = null;
      workDataset.src_typename = null;
      workDataset.points = null;
      workDataset.filter.points = null;
    }
    else {
      workDataset.source = sourceDS.name;
      workDataset.src_typename = sourceDS.typename;
      if (sourceDS.typename) 
        await loadPoints(sourceDS.typename)
    }
    setSelectedSource(sourceDS)
    setWorkDataset(workDataset)
    await saveWorkDataset() 
  };
  
  // This extracts data to filter the source points dataset
  const extractData = async (points) => {
    /* FILTER FIELDS
      point_type, 
      project, 
      date, 
      survey_m_id, 
    */
    let prjs = ["All projects"]
    let sms = ["All methods"]
    let ts = ["All types"]
    if (!points)
      return;
    /// read projects, survey and laboratory methods
    for ( let i = 0; i < points.features.length; i += 1 ){
      const props = points.features[i].properties
      try {
        if ( props.project && prjs.indexOf(props.project) === -1 )
          prjs.push(props.project)
        if ( props.survey_m_id && sms.indexOf(props.survey_m_id) === -1 )
          sms.push( props.survey_m_id )
        if ( props.point_type && ts.indexOf(props.point_type) === -1 )
          ts.push( props.point_type )
        if ( props.date ) {
          const d = new Date(props.date)
          if ( workDataset.filter.from === null || new Date(workDataset.filter.from) > d ) {
            setFrom(d)
          }
          if ( workDataset.filter.to === null || new Date(workDataset.filter.to) < d ) {
            setTo(d)
          }  
        }
      }
      catch (e) {
        console.log(e) 
      } 
    }
    setProjects(prjs);
    setSurMethods(sms);
    setTypes(ts)  
  }

  // This reset the source points dataset
  const resetPoints = () => {
    setPoints (null);
    setProjects([{ descr: "All projects"}]);
    setSurMethods([{ descr: "All methods"}]);
    setTypes([{ descr: "All types"}]);
  }

  // This loads and sets the source points from a catalogue dataset
  const loadPoints = async (typename) => {
    if ( !workDataset )
      return
    try {
      const token = user.userData.access_token;
      setIsWorking(true);
      const response = await ProfileService.getDataset( typename, null, token )
      setIsWorking(false);
      if ( response && response.ok && response.data && response.data.features ){
        const points = response.data; 
        setPoints (points);
        await extractData (points);
        filtering();
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
  const filtering = () => {
    //return []
    let filtered = [] 
    if ( workDataset && workDataset.filter && workDataset.points && workDataset.points.features )
    { 
      for ( let l=0; l < workDataset.points.features.length; l += 1){
        let ok = false;
        let pt = workDataset.points.features[l];
        let props = pt.properties;
        // AOI filter   
        if ( workDataset.filter.aoi ){
          for ( let x=0; x < workDataset.filter.aoi.features.length; x += 1)
            if ( booleanPointInPolygon( pt, workDataset.filter.aoi.features[x] ) )
              ok = true;
        }
        if ( ok && props ){
          if (
            ( workDataset.filter.from && 
              ( new Date (workDataset.filter.from)) > new Date( props.date ) )  ||
            ( workDataset.filter.to && 
              ( new Date (workDataset.filter.to)) < new Date( props.date ) ) ) 
            { ok = false }
        }
        if ( ok && props && workDataset.filter.depth ){
          
          if ( ( workDataset.filter.depth === ProfileService.FILTER_DEPTH.DEPTH0_20 ) && ( props.upper > 20 ))
            ok = false
          else if ( 
            ( workDataset.filter.depth === ProfileService.FILTER_DEPTH.DEPTH20_50 ) &&
            ( props.upper === null || props.upper > 50 ||
              ( props.lower != null && props.upper > props.lower ) ||
              ( props.lower != null && props.lower < 20 ) 
            )
          )
          { ok = false }
        }      
        if ( ok && props && workDataset.filter.project &&  
          workDataset.filter.project !== props.project &&
          workDataset.filter.project !== "All projects" 
        )
        { console.log('prj'); ok = false }
        if ( ok && props && workDataset.filter.type && 
          workDataset.filter.type !== props.type_id &&
          workDataset.filter.type !== "All types" )
        { console.log('type'); ok = false }
        if ( ok && props && workDataset.filter.surMethod && 
          workDataset.filter.surMethod !== props.survey_m_id &&
          workDataset.filter.surMethod !== "All methods" )
        { console.log('method'); ok = false }
        if ( ok )
          filtered.push(pt)    
      }
      workDataset.filter.points = featureCollection(filtered);
      setFPoints(workDataset.filter.points)
      setWorkDataset(workDataset) 
    }
    return workDataset.filter.points
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
        setSelectedSource(null)
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
    const result = await saveWorkDataset()
    if ( result && to ) 
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

  // This loads the dataset sources list for a page  
  const loadAreasDatasets = async  ( page ) => { 
    try {
      setAreasDatasets(null);
      setIsWorking(true)
      const respAreas = await ProfileService.getDatasetsByCategory('boundaries', page, document.cookie);
      setIsWorking(false)
      if ( respAreas && respAreas.ok && respAreas.data ) {
        setAreasDatasets(respAreas.data)
        if (respAreas.data.total)
          setTotalAreas(respAreas.data.total)
      }     
    } catch (error) {
      console.log(error)
      setIsWorking(false) 
    } 
     
  }

  // This loads the taxonomy for the Point Soil Data Types needed by filters   
  const loadPointSoilDataTypes = async  ( ) => {
    try {
      setAreasDatasets(null);
      const respAreas = await TaxonomyService.listValues(  document.cookie);
      if ( respAreas && respAreas.ok && respAreas.data ) {
        setAreasDatasets(respAreas.data)
        if (respAreas.data.total)
          setTotalAreas(respAreas.data.total)
      }     
    } catch (error) {
      console.log(error) 
    }  
  }

  // This manages change page in boundaries dataset list  
  const onAreasPageChange = (event) => {
    setAreasPage(event.first);
    loadAreasDatasets(event.first)
  };
  
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
          setAoi(result)
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

  // This sets the survey method filter
  const setFilterSurMethod = (value) => {
    setSelectedSurMethod(value);
    workDataset.filter.surMethod = value
  };
  
  // This sets the project name filter
  const setFilterProject = (value) => {
    setSelectedProject(value);
    workDataset.filter.project = value
  };

  // This sets the points soil data type filter
  const setFilterType = (value) => {
    setSelectedType(value);
    workDataset.filter.type = value
  };

  // This initializes the laboratory method filter
  const initializeData = async () => {
    try { 
      if (workDataset.points) {
        await extractData(workDataset.points)
        filtering();
      };
      if ( workDataset.filter && workDataset.filter.aoi )
        setSelectedArea(workDataset.filter.aoi)
      const response = await TaxonomyService.listValues(document.cookie, 'POINT_DATA_TYPES')
      if ( response && response.ok && response.data )
          setInfoTypes(response.data);
      const response2 = await TaxonomyService.listValues(document.cookie, 'SURVEY_METHODS')
      if ( response2 && response2.ok && response2.data )  
          setInfoSMethods(response2.data)
      setSelectedType ( workDataset.filter.type )
      setSelectedSurMethod( workDataset.filter.surMethod )
    } catch (error) {
      console.log(error)
    }  
  }

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    if ( workDataset && workDataset.points )
      initializeData()
    loadAreasDatasets(1)
  }, [user, dataset]); // eslint-disable-line

  const aoiSourceTypes = [
    { key: 'custom', name: 'Custom Polygon' },
    { key: 'dataset', name: 'Catalogue dataset'}
  ]
  
  return (
    <div className="layout-dashboard">
    <Toast ref={toast} />
      {(!workDataset || !workDataset.filter) && (
      <span className="font-bold text-red-800">Error: dataset or filter not initialized </span>
      )} 
      { workDataset && workDataset.filter  && (
      <>
      <Steps model={items} activeIndex={activeIndex} readOnly className="mb-4" />
        { activeIndex === 0  && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          <div className="flex flex-column w-full m-2 align-items-center justify-content-center">
            <Fieldset className="w-full" legend={t('NAME')}>
              <InputText className="w-full" value={workDataset.name} onChange={(e) => setName(e.target.value)} />
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
                  onClick={() => { setSource (null) }}
                />
                <h5 className="font-bold text-800">Selected source: <span className="font-bold text-cyan-800">{workDataset.source}</span></h5>   
                <h5 className="font-bold text-800">Points: <span className="font-bold text-cyan-800">
                { workDataset.points && ( workDataset.points.features ? workDataset.points.features.length : 0 )}
                { !workDataset.points && ( 0 )}  
                </span></h5> 
              </div>
              )}
              </>
            )}
            { workDataset.source === null && (
              <div className="card flex flex-column gap-3 align-items-center mt-3">
              { isWorking && (
                <Loading title="Loading indicators"/>
              )}
              { !isWorking && srcDatasetsList && (
                <>
                  <h6 className="md:w-30rem surface-200 font-bold text-cyan-800 p-3 shadow-2">Available Sources</h6>
                  <Dropdown value={selectedSource} onChange={(e) => setSource(e.value)} options={srcDatasetsList} optionLabel="name" 
                    placeholder="Select a section" className="w-full md:w-30rem font-bold text-cyan-800" checkmark={true}  highlightOnSelect={false} />
                </>
              )}
              { !isWorking && ( !srcDatasetsList?.datasets || srcDatasetsList.datasets?.length === 0) && (
                <span classname="font-bold text-cyan-800">{t('EMPTY')}</span>
              )}
              </div>
            )}
            </Fieldset>
            <div class="flex justify-content-center w-full m-3">
              <Button
                label={t("SAVE_CONTINUE")}
                icon='pi pi-save'
                type='button'
                disabled={ isWorking || !workDataset || !workDataset.points }
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
                  <ListBox value={areasDataset} disabled={isWorking} onChange={(e) => setAreasDataset(e.value) } options={areasDatasets.datasets} 
                        optionLabel="name" className="md:w-30rem font-bold text-cyan-800" listStyle={{ maxHeight: '250px' }} />
                  <Paginator first={areasPage} rows={10} totalRecords={totalAreas} onPageChange={onAreasPageChange} 
                        template={{ layout: 'PrevPageLink CurrentPageReport NextPageLink' }} />
                  <Button
                    label={t('ADD_TO_MAP')}
                    icon='pi pi-map'
                    type='button'
                    disabled={ isWorking || !areasDataset || !areasDataset.alternate }
                    onClick={() => { setAreasTypeName(areasDataset.alternate); }}
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
        {( !fPoints || !workDataset.filter.aoi ) && (
          <span className="font-bold text-red-800">Error: no filtered points or Aoi not initialized </span>
        )}
        { fPoints && workDataset.filter.aoi && ( 
          <>
          <h5 className="font-bold text-cyan-800"> 
            { fPoints.features ? fPoints.features.length : 0 } Filtered Points</h5> 
          <PointsFilterMap points={fPoints} area={workDataset.filter.aoi} />
          <div class="flex justify-content-center w-full m-3">
            <Button
              label={t('APPLY_FILTER')}
              icon='pi pi-wrench'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { filtering() }}
            /> 
          </div>
          <Fieldset className="w-full m-2" legend={t('PERIOD')}>
            <h5 className="font-bold text-cyan-800">Select a period or None for all periods</h5>
            <div className="flex flex-row gap-2 font-bold text-cyan-800 w-full align-items-center mt-3">
              <span className="flex w-3 m-2 justify-content-end">{t('FROM_DATE')}</span><Calendar value={ new Date(workDataset.filter.from) } onChange={ (e) => setFrom(e.value) } showIcon />
            </div>  
            <div className="flex flex-row gap-2 font-bold text-cyan-800 w-full mt-3">
              <span className="flex w-3 m-2 justify-content-end">{t('TO_DATE')}</span><Calendar value={ new Date(workDataset.filter.to) } onChange={(e) => setTo(e.value)} showIcon />
            </div>  
          </Fieldset>
          <Fieldset className="w-full m-2" legend={t('DEPTH')}>
            <div className="flex flex-row gap-3">
              <RadioButton inputId="none" name="depth" value="none" onChange={(e) => setDepth(null) } checked={ workDataset.filter.depth === null} />
              <label htmlFor="none" className="ml-2">All depths</label>
              <RadioButton inputId="DEPTH0_20" name="depth" value="DEPTH0_20" onChange={(e) => setDepth("DEPTH0_20") } checked={ workDataset.filter.depth === 'DEPTH0_20'} />
              <label htmlFor="DEPTH0_20" className="ml-2">Upper: 0 cm; Lower: 20 cm</label>
              <RadioButton inputId="DEPTH20_50" name="depth" value="DEPTH20_50" onChange={(e) => setDepth("DEPTH20_50") } checked={ workDataset.filter.depth === 'DEPTH20_50'} />
              <label htmlFor="DEPTH20_50" className="ml-2">Upper: 20 cm; Lower: 50 cm</label>
            </div>
          </Fieldset>
          <Fieldset className="w-full m-2" legend={t('TYPE')}>
            <div className="flex flex-column gap-3">
              <h5 className="font-bold text-cyan-800">Select a point soil data type or All types</h5>
              <Dropdown value={selectedType} onChange={(e) => setFilterType(e.value)} options={types} 
                placeholder="select a type" className="md:w-30rem font-bold text-cyan-800" />
              {( selectedType && (
                <h5 className="font-bold text-cyan-800" >{ GetInfo( selectedType, infoTypes ) }</h5>
              ))}
            </div>
          </Fieldset> 
          <Fieldset className="w-full m-2" legend={t('SURMETHOD')}>
            <div className="flex flex-column gap-3">
              <h5 className="font-bold text-cyan-800">Select a survey method or All methods</h5>
              <Dropdown value={selectedSurMethod} onChange={(e) => { setFilterSurMethod(e.value) } } 
                options={surMethods} placeholder="select a survey method" className="md:w-30rem font-bold text-cyan-800" />
              {( selectedSurMethod && (
                <h5 className="font-bold text-cyan-800" >{ GetInfo( selectedSurMethod, infoSMethods ) }</h5>
              ))}
            </div> 
          </Fieldset>
          <Fieldset className="w-full m-2" legend={t('PROJECT')}>
            <div className="flex flex-column gap-3">
              <h5 className="font-bold text-cyan-800">Select a project or All projects</h5>
              <Dropdown value={selectedProject} onChange={(e) => setFilterProject(e.value)}  
                options={projects} placeholder="select a project" className="md:w-30rem font-bold text-cyan-800" />
            </div>
          </Fieldset>
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
