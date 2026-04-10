"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { ProfileService } from '../../service/profiles';
import { TaxonomyService } from '../../service/taxonomies';
import { userContext, useUser } from '../../context/user';
import Loading from '../../components/Loading';
import Datasets from '../../data/datasets';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic"

import { FileUpload } from 'primereact/fileupload';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { InputNumber } from 'primereact/inputnumber';
import { Fieldset } from 'primereact/fieldset';
import { Slider } from 'primereact/slider';
import { SelectButton } from 'primereact/selectbutton';
import { ListBox } from 'primereact/listbox'; 
import { Toast } from 'primereact/toast';
import { Steps } from 'primereact/steps';

import { clone, featureCollection } from '@turf/turf';

const MyMap = dynamic(() => import("../../components/CreatorPointsMap"), { ssr:false })

/*
* This page allows you to generate a new dataset by filtering
* soil point dataset published on MED-SIS .
* Filters:
* - Area Of Interest
* - Depth
* - Area
* - Project
* - Method
* - Type
* - 
*/ 
export default function Page()  {
  const t = useTranslations('default');
  const [activeIndex, setActiveIndex] = useState(0);
  const [mapData, setMapData] = useState(null);
  const [request, setRequest] = useState(null);
  
  const [dataset, setDataset] = useState(null);
  const [points, setPoints] = useState(null);
  
  // Geoserver layer source

  // AOI
  const [gnAreas, setGnDsAreas] = useState(null);
  const [areas, setAreas] = useState(null);
  const [aoiFileName, setAoiFileName] = useState(null);
  const [validating, setValidating] = useState(false);
  const aoiFileRef = useRef(null);
  // Depth
  const [upper, setUpper] = useState(null);
  const [lower, setLower] = useState(null);
  // Date
  const [from, setFrom] = useState(null);
  const [to, setTo] = useState(null);
  // Type
  const [types, setTypes] = useState(null);
  // Project
  const [projects, setProjects] = useState(null);
  
  const user = useUser();
  const router = useRouter();
  const toast = useRef(null);
  const [loading, setLoading] = useState(false);
  

  const stepItems = [
    {
      label: 'Define Source'
    },
    {
      label: 'Area of Interest'
    },
    {
      label: 'Filtering'
    },
    {
      label: 'Interpolation'
    },
    {
      label: 'Publishing'
    }
  ];

  const loadGeoJSON = async () => {
    if ( !request.source || !request.source.geoserver )
      return
    setLoading(true);
    // update data
    if ( !request.source.data )
    {
      let points = { 
        msg  : "Data not available",
        count: 0,
        name : request.source.geoserver,
        data : []
      }
      try {
        const response = await ProfileService.getDataset( request.source.geoserver, document.cookie )
        if ( !response || !response.ok || !response.data || !response.data.features )
        {
          points.count = response.data.features.length
          points.data = response.data
          points.msg = "Successfully loaded"
        }
        request.source = points;
        const response2 = await ProfileService.update( document.cookie, request.id, request, 'requests' )
        if ( !response2 || !response2.ok || !response2.data )
        {
          setRequest(response2.data)
        }
        toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Source data has been loaded.'});
      } catch (e) {
        console.log(e);
        toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Data not available.'});
      
      }
    }
    setLoading(false)     
  }
   
  const inRange = ( a, b ) => {
    let min = (a[0] < b[0]  ? a : b)
    let max = (min == a ? b : a)
    if ( min[1] < max[0] )
      return false;
    return true
  }

  const filterData = async () => {
    if ( !request || !request.source || !request.source.data )
      return
    let filtered = clone(featureCollection(request.source.data));
    if ( !filtered.features || !filtered.features.length || filtered.features.length === 0 )
      return null
    if ( request.aoi ) 
    {
      ffeatures = [];   
      for ( let i = 0; i < filtered.features; i += 1 )
        if ( turf.booleanContains( request.aoi, filtered.features[i]) ) 
          ffeatures.push(filtered.features[i])
    }
    else request.aoi = turf.envelope(filtered);
    filtered = featureCollection(ffeatures);
    if ( request.upper && request.lower ) 
    {
      ffeatures = [];
      for ( let i = 0; i < filtered.features; i += 1 )
      {
        let u = 0;
        let l = 10000; // 100m
        ft = filtered.features[i]
        if ( ft && ft.properties && ft.properties["upper"] )
          u = Number.parseInt(ft.properties["upper"])
        if ( ft && ft.properties && ft.properties["lower"]) 
          l = Number.parseInt(ft.properties["lower"])
        if ( inRange( [request.upper,request.lower], [u,l] ) )
          ffeatures.push(ft)
      } 
      filtered = featureCollection(ffeatures);
    }
    if ( request.filters.from ) {
      ffeatures = [];
      for ( let i = 0; i < filtered.features; i += 1 )
      {
        let ft = filtered.features[i];
        if ( ft && ft.properties && ft.properties["date"] &&
          period[0] <= ft.properties["date"] && 
          period[1] >= ft.properties["date"]
        )
          ffeatures.push(ft)
      } 
      filtered = featureCollection(ffeatures);
      /*
      <Calendar value={dates} onChange={(e) => setDates(e.value)} selectionMode="range" readOnlyInput hideOnRangeSelection />
      */
    }
    else if ( filtered && filtered.features) 
    { //cm
      const _from = new Date(0);
      const _to = new Date.now();
      for ( let i = 0; i < filtered.features.length ; i += 1 )
      { 
        let prop = filtered.features[i].properties
        if ( prop && prop["date"] && (!_from || _from > Date.parse(prop["date"])) )
          _from = Date.parse(prop["date"]);
        if ( prop && prop["date"] && (!_to || _to < Date.parse(prop["date"])) )
          _to = Date.parse(prop["date"]);
      }
      if ( !_from ) new Date(0);
      if ( !_to ) new Date.now();
      setPeriod([_from,_to]);
    }
    if ( project ) {
      /*
      <InputText value={value} onChange={(e) => setValue(e.target.value)} />
      */
      ffeatures = [];
      for ( let i = 0; i < filtered.features; i += 1 )
      {
        let ft = filtered.features[i];
        if ( ft && ft.properties && project === ft.properties["project"] )
          ffeatures.push(ft)
      } 
      filtered = featureCollection(ffeatures);
      /*
      <Calendar value={dates} onChange={(e) => setDates(e.value)} selectionMode="range" readOnlyInput hideOnRangeSelection />
      */
    }
    if ( type ) {
      /*
      <Dropdown value={selectedCity} onChange={(e) => setSelectedCity(e.value)} options={cities} optionLabel="name" 
    placeholder="Select a City" className="w-full md:w-14rem" />
      */
      ffeatures = [];
      for ( let i = 0; i < filtered.features; i += 1 )
      {
        let ft = filtered.features[i];
        if ( ft && ft.properties && type === ft.properties["type"] )
          ffeatures.push(ft)
      } 
      filtered = featureCollection(ffeatures);
    }
    if ( method ) {
      /*
      <Dropdown value={selectedCity} onChange={(e) => setSelectedCity(e.value)} options={cities} optionLabel="name" 
    placeholder="Select a City" className="w-full md:w-14rem" />
      */
      ffeatures = [];
      for ( let i = 0; i < filtered.features; i += 1 )
      {
        let ft = filtered.features[i];
        if ( ft && ft.properties && type === ft.properties["method"] )
          ffeatures.push(ft)
      } 
      filtered = featureCollection(ffeatures);
    }
    setFilteredPoints(filtered);
     
  };

  const download = () => {
    console.log('download')
  }

  const resetFilter = async () => {
    const fp = await JSON.parse( JSON.stringify(pointsGeoJSON.data))
    setFilteredPoints(fp);
    setActiveIndex(1);
  }

  const resetData = () => {
    setDataset(null);
    setPointsGeoJSON(null);
    setFilteredPoints(null);
  }

  const handleSelect = ( feature ) => {
    console.log(feature)
  }

  const publish = () => {
    console.log('publish')
  }

  const validateRoiFile = async (files) => {
    const geojson = null;
    try {
      // validate geometry first feature
      // Add bbox, area to new geojson
      if ( files && files[0] ) {
        const readFilePromise = (path) => new Promise((resolve, reject) => {
          const readFile = new FileReader();
          readFile.onload = (event) =>  { 
            const contents = event.target.result;
            let geojson = JSON.parse(contents.replaceAll('/n',''));
            geojson.bbox = bbox(geojson);
            geojson.area = area(geojson) / 10000;   // hectares
            resolve(JSON.stringify(geojson));
          };
          readFile.onerror = (error) => {
            reject(error);
          };
          readFile.readAsText(file);
        }); 
        setFileId(files[0].name)    
        geojson = await readFilePromise(files[0])
        if ( geojson ) {
          toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Your polygon has been uploaded.'});
          geojson.source = files[0].name
          setAoi(geojson);
          return
        } 
      }
    } catch (error) {
      console.log(error);
    }
    roiFileRef.current?.clear();
    setFileId( null )
    toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Errors reading file'});
  }; 
    
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    setLoading(true)
    try {
      const response = ProfileService.getDatasetsByCategory( 'boundaries', document.cookie );
      if ( response && response.ok && response.data && response.data.resources )
        setGnDsAreas (response.data.resources);    
    } catch (error) {
      setGnDsAreas ([]);
      console.log(error);
    }
    setLoading(false) 
  },[user]);  // eslint-disable-line

  useEffect(() => {
    loadGeoJSON()
  },[dataset]);  // eslint-disable-line

  useEffect(() => {
    if ( pointsGeoJSON ) 
      filterData();
  },[aoi, depth, period, project, type, method]);  // eslint-disable-line

  useEffect(() => {
    const fetchMap = async () => {
      if ( filteredPoints ) {
        const pointsData = {
          layer : {
            points: filteredPoints,
            style: { radius: 8, fillColor: 'rgb(8, 156, 197)', color: 'rgb(221, 33, 0)', weight: 3, opacity: 1, fillOpacity: 0.7, },
          },
          label: 'Filtered ' + pointsGeoJSON.source,
        };
        setMapData(pointsData);
      }  
    }
    if ( filteredPoints )
      fetchMap();
  }, [filteredPoints]); // eslint-disable-line

  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Creating a new dataset from soil data filtering</h5>
    <div className="card w-full">
      <Steps model={stepItems} activeIndex={activeIndex} onSelect={(e) => setActiveIndex(e.index)} readOnly={false} />
      <div className="w-full flex flex-column align-items-center m-3 gap-3">
      { activeIndex === 0 && (
        <>
        <h5 className="md:w-30rem font-bold text-cyan-800 p-3 m-3 justify-content-center shadow-2">
            Select the initial data
        </h5>
        { pointsGeoJSON && ( 
        <div className="card md:w-30rem flex flex-column gap-3 m-3 align-items-center">  
          <Button icon="pi pi-trash" onClick={resetData} severity="danger"/>
          <div className="md:w-30rem">
            <h5 className="font-bold text-green-600 m-2">
              <span className="font-bold text-gray-800">Selected: </span> 
              {pointsGeoJSON.name} 
            </h5>
            <h5 className="font-bold text-green-600 m-2">
              <span className="font-bold text-gray-800">Status: </span>
              {pointsGeoJSON.msg}
            </h5>
            <h5 className="font-bold text-green-600 m-2">
              <span className="font-bold text-gray-800">Points: </span>
              {pointsGeoJSON.count}
            </h5>
          </div>
        </div>
        )}
        { loading && (
            <Loading  title="Loading ..." />
        )}
        { !loading && !pointsGeoJSON && (
        <div className="flex flex-column gap-3 align-items-center">
          <SelectButton value={dataType} onChange={(e) => setDataType(e.value)} options={dataOptions} />
          <div className="xl:flex xl:justify-content-center">  
            { dataType === 'Soil Indicator' && (
            <ListBox value={dataset} onChange={(e) => setDataset(e.value)} disabled={loading} options={Datasets["indicators"]} optionLabel="name" 
              className="w-full md:w-30rem" listStyle={{ maxHeight: '250px' }} />
            )} 
            { dataType === 'Point Soil Data'  && (
            <ListBox value={dataset} onChange={(e) => setDataset(e.value)} disabled={loading} options={Datasets["sections"]} optionLabel="name" 
              className="w-full md:w-30rem" listStyle={{ maxHeight: '250px' }} />
            )}
              
          </div>
        </div>  
        )}
        <Button icon="pi pi-arrow-right" iconPos="right" label="Next" disabled={!(pointsGeoJSON?.count)} onClick={() => resetFilter()} severity="success" raised />
        </>
      )}  
      { activeIndex === 1 && mapData && (
      <>
      <h5 className="w-full font-bold text-cyan-800 p-3 m-3 justify-content-center shadow-2">
          Data filtering 
      </h5>
      <div id="mymap" className="w-full card m-3">
        <h6 class="font-bold surface-200 text-green-500">{ mapData ? mapData.label : 'Filtered data' }</h6>
        <MyMap data={mapData} setSelected={handleSelect} />
      </div>
      <div className="m-3">
        <Fieldset classname="flex flex-column" legend="Area Of Interest">
        { !aoi && ( 
          <>
          { !dsAreas && gnDsAreas && gnDsAreas.length  && (
          <>
          <Dropdown id="gndataset" classname="md:w-30rem" optionLabel="name" value={dsAreas} options={gnDsAreas} onChange={(e) => setDsAreas(e.value)} placeholder="Select a Dataset"/>
          <label htmlFor="gndataset">Select a dataset then a polygon in the map</label>
          </>
          )}
          <div classname="flex flex-row mt-4">
            <FileUpload 
                disabled={fileId !== null || validating}
                id="file"
                ref={roiFileRef}
                accept='.json, .geojson'
                chooseLabel={t('CUSTOM_POLYGON')}
                mode="basic"
                multiple={false}
                customUpload
                auto
                className='mb-4 mr-2 mt-4'
                uploadHandler={(e) => validateRoiFile(e.files)}
              /> 
          </div>
          </>
        )} 
        { !aoi && dsAreas && ( 
          <div className="card md:w-30rem flex flex-column gap-3 m-3 align-items-center">  
            <Button icon="pi pi-trash" onClick={resetData} severity="danger"/>
            <h5 classname="font-bold text-cyan-800">Dataset Selected: <span  classname="text-green-600">{ dsAreas }</span></h5>
            <h6 classname="font-italic">!Select a polygon in the map</h6>
          </div>
        )} 
        { aoi && ( 
          <div className="card md:w-30rem flex flex-column gap-3 m-3 align-items-center">  
            <Button icon="pi pi-trash" onClick={resetData} severity="danger"/>
            <h5 classname="font-bold text-cyan-800">Aoi Selected: <span  classname="text-green-600">{ aoi.source }</span></h5>
          </div>
        )}
        </Fieldset>
        <Fieldset legend="Depth">
        <div className="grid m-2">
          <div classname="col-6">
            <h5 className="font-bold text-cyan-800">Upper: {depth[0]}</h5>
            <h5 className="font-bold text-cyan-800">Lower: {depth[1]}</h5>
          </div>
          <div classname="col-6 flex flex-column align-item-center">
            <div className="font-bold text-blue-800">0 cm</div>
            <Slider max={maxDepth} value={depth} onChange={(e) => setDepth(e.value)} orientation="vertical" className="h-14rem" range />
            <div className="font-bold text-blue-800">100 cm</div>
            <span className="p-float-label">
              <InputNumber id="maxdepth" maxFractionDigits='0' value={maxDepth} onValueChange={(e) => setMaxDepth(e.value)} />
              <label htmlFor="maxdepth">Max Depth (default 100)</label>
            </span>
          </div>
        </div>
        </Fieldset>
      </div>
      <div className="flex flex-row gap-3 align-items-center">
        <Button icon="pi pi-arrow-circle-left" label="Previous" onClick={() => resetData() } severity="success" raised />
        <Button icon="pi pi-arrow-circle-right" iconPos="right" label="Next" disabled={!filteredPoints} onClick={ () => setActiveIndex(2)} severity="success" raised />
      </div>
      </>
      )}
      {(activeIndex === 2) && (
      <>
      {(filteredPoints) && (
        <span class="font-bold text-cyan-800">ok dataset filtered</span>
      )}
      {(!filteredPoints) && (
        <span class="font-bold text-cyan-800">first filter the data</span>
      )}
        <Button icon="pi pi-arrow-circle-left" label="Previous" disabled={!dataset} onClick={() => setActiveIndex(2)} severity="success" raised />
        <Button icon="pi pi-download" label="Download" disabled={!filteredPoints} onClick={() => download()} severity="success" raised />
        <Button icon="pi pi-map" label="Publish" disabled={!filteredPoints} onClick={() => publish() } severity="success" raised />
      </>
      )}
      </div>
    </div>
  </div>
  );
};

export async function getStaticPaths() {
  return {
    paths: [],
    fallback: 'blocking',
  }
}

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
    },
  }
}



