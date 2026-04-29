"use client"

import { point, bbox, bboxPolygon, featureCollection } from '@turf/turf';
import React, { useState, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';

import { Paginator } from 'primereact/paginator';
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
import TaxonomyService from '../service/taxonomies';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../context/user';
import { ProfileService } from '../service/profiles';
import { InputTextarea } from "primereact/inputtextarea";
import dynamic from "next/dynamic";
import Loading from './Loading';

const AoiSelectionMap = dynamic(() => import("./AoiSelectionMap"), { ssr:false })

const initialFilter = {
  aoi : null,
  period : [null,null] ,
  depth: [0,null],
  project: null,
  type: null,
  method: null
};

export default function ConfigureDataset( { dataset })  {
  const t = useTranslations('default');
  const user = useUser();
  const router = useRouter();
  const toast = useRef(null);
  const [updatedDataset, setupdatedDataset] = useState(dataset);
  // it manages configuration steps
  const [activeIndex, setActiveIndex] = useState(0);
  // working state (loading, uploading)
  const [isWorking, setIsWorking] = useState(true);
  // DATASET NAME 
  const [datasetName, setDatasetName] = useState(null);
  
  // AOI FILTER
  // boundary datasets list (paginated)
  const [areasDatasets, setAreasDatasets] = useState(null);
  // boundaries dataset selected 
  const [areasDataset, setAreasDataset] = useState(null);
  // boundary datasets list page
  const [areasPage, setAreasPage] = useState(1);
  const [firstAreasPage, setFirstAreasPage] = useState(0);
  const [totalAreas, setTotalAreas] = useState(0);
  // selected A0i source type 
  const [selectedAoiSourceType, setSelectedAoiSourceType] = useState(null); 
  // custom AOI file
  const aoiFileRef = useRef(null);
  const [aoiFileId, setAoiFileId] = useState(null);
  
  // SOURCE
  // sources datasets to choose the points (paginated)
  const [srcDatasetsList, setSrcDatasetsList] = useState(null);
  // sources datasets list page
  const [srcDatasetsPage, setSrcDatasetsPage] = useState(1);
  // selected source dataset  
  const [selectedSource, setSelectedSource] = useState(null);
  // Paginator
  const [firstSourcesPage, setFirstSourcesPage] = useState(0);
  const [totalSources, setTotalSources] = useState(0);

  const [map, setMaps] = useState(null);
 
  // It sets the name of dataset 
  const setName = (name) => {
    setDatasetName(name)
    if ( updatedDataset ){
      updatedDataset.name = name;
      setUpdatedDataset(updatedDataset);
    }  
  }
  
  const loadSrcPoints  = async () => {
    if ( !selectedSource || !selectedSource.alternate || !updatedDataset )
      return
    setIsWorking(true);
    try {
      const response = await ProfileService.getDataset( selectedSource.alternate, document.cookie )
      if ( response && response.ok && response.data && response.data.features ){
        updatedDataset.points = response.data;
        updatedDataset.srcPoints = clone(response.data); 
        setUpdatedDataset(updatedDataset);
        toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Source points has been loaded.'});
      }
    } catch (e) {
      console.log(e);
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Data not available.'});
    }
    
    setIsWorking(false);     
  }

  // It sets the geonode Id of the source points 
  const setSource = async (source) => {
    if ( source  && updatedDataset )
    {
      updatedDataset.source = source.alternate;
      updatedDataset.points = null;
      updatedDataset.srcPoints = null;
      setupdatedDataset(updatedDataset);
      setSelectedSource(source)
    }  
  };

  // It sets the filtered points 
  const updatePoints = (points) => {
    if ( updatedDataset ){
      updatedDataset.points = points;
      setupdatedDataset(updatedDataset);
    }  
  };

  // It sets the aoi to filter points soil data
  const setArea = (area) => {
    if ( updatedDataset && updatedDataset.filter ){
      updatedDataset.filter.aoi = area;
      setupdatedDataset(updatedDataset);
    }  
  };

  const formatDate = (value) => {
    const date = new Date(value).toJSON()
    date = date.substring(0,10)
    return date
  };

  // Filtered Points Soil Data Map configuration
  const createPopupContent = (feature) => {
    try {
      if ( feature && feature.properties ){
        let panel = '<div class="flex flex-wrap  justify-content-center">';
        Object.keys(feature.properties).forEach(
          (field) => {
            panel += '<span class="text-cyan-500 align-items-center font-bold" >' + field + '</span>';
            panel += '<span>' + (feature.properties[field]) + '</span>';
          }
        );
        panel += '</div>'; 
      }
      return panel;
    } catch (e) {
      console(e)
    }
    return '<div><span class="font-bold">No data</span></div>';  
  } 
  
  const disableSave = () => {
    return ( !updatedDataset || !updatedDataset.name === "" || !updatedDataset.points || !updatedDataset.filter )
  }

  // Save the dataset and go to datasets list pages
  const saveDataset = async () => {
    try {
      // no data no party
      if ( !updatedDataset ||  !updatedDataset.name === "" || !updatedDataset.points || updatedDataset.points === {} || !updatedDataset.filter )
        return;
      // if the AOI isn't set use the bbox of the filtered points 
      if ( !updatedDataset.filter.aoi ) {
        updatedDataset.filter.aoi = turf.featureCollection([ turf.bboxPolygon(turf.bbox(updatedDataset.points)) ]);
      }  
      updatedDataset.k_variogram = null;
      updatedDataset.k_gn_raster = null;
      updatedDataset.k_data = null,
      updatedDataset.catalogue_id = null;
      updatedDataset.status = ProfileService.DATASET_STATUSES.CONFIGURED
      const response = await ProfileService.save(document.cookie, updatedDataset);
      if ( response && response.ok ) { 
        toast.current.show({severity: 'Success', summary: 'Success!', detail: 'Dataset has been configured' , life: 3000});
        setTimeout(() => {
          router.push('/datasets') 
        }, 3000);
      } 
      else toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset' , life: 3000});
    } catch (error) {
      console.log(error)
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset' , life: 3000}); 
    } 
  } 
  
  // Steps
  const items = [
    { label: t('DS_DEFINITON'), command: (_e) => {setActiveIndex(0);} },
    { label: t('DS_SOURCE') , command: (_e) => {setActiveIndex(1);}},
    { label: t('DS_AOI'), command: (_e) => {setActiveIndex(2);}},
    { label: t('DS_FILTERS'), command: (_e) => {setActiveIndex(3);} }, 
  ];

  let FiltersHeaders = ['Definition', 'Data Source', 'Area of Interest', 'Filters'];

  const backToAoi = () => {
    setFilter( {
      ...initialFilter,
      aoi: dataset.filter?.aoi
    });
    setActiveIndex(2);
    aoiFileRef.current?.clear();
  };
  
  const loadSources = async  ( page ) => {
    setIsWorking(true)
    try {
      setSrcDatasetsList(null);
      const keywords = ["physical_health","chemical_health","biological_health"]
      const respSources = await ProfileService.getDatasetsByKeyword(keywords, page, document.cookie);
      if ( respSources && respSources.ok && respSources.data ) {
        setSrcDatasetsList(respSources.data)
        if (respSources.data.total)
          setTotalSources(respSources.data.total)
      }
    } catch (error) {
      console.log(error)  
    }
    setIsWorking(false)   
  }

  const onSourcesPageChange = async  () => {
    setFirstSourcePage(event.first);
    loadSources(event.first)
  }
  
  const loadAreasDatasets = async  ( page ) => {
    setIsWorking(true)
    try {
      setAreasDatasets(null);
      const respAreas = await ProfileService.getDatasetsByCategory('boundaries', page, document.cookie);
      console.log(respAreas)
      if ( respAreas && respAreas.ok && respAreas.data ) {
        setAreasDatasets(respAreas.data)
        if (respAreas.data.total)
          setTotalAreas(respAreas.data.total)
      }   
      setIsWorking(false)
    } catch (error) {
      console.log(error) 
    }  
  }

  const onAreasPageChange = (event) => {
    setFirstAreasPage(event.first);
    loadAreasDatasets(event.first)
  };
  
  const goToSources = () => {
    setActiveIndex(1);
    if ( !selectedSource )
      loadSources(1)
  }

  const className1 = 'col-6 font-bold text-cyan-800 mt-1 mb-1';
  const className2 = 'col-6 text-green-800 mt-1 mb-1';
  
  const uploadRoiFile = async (file) => {
    try {
      // validate geometry first feature
      // Add bbox, area to new geojson
      if ( file ) 
      {
        const readFilePromise = (path) => new Promise((resolve, reject) => {
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
                else { 
                  geojson.features.forEach( (ft) => {
                    if ( area(ft) ) 
                      if ( oneFeature ) {
                        oneFeature = union( oneFeature, ft )
                      }  
                      else oneFeature = ft 
                  })
                  if ( oneFeature )
                    ftCl = featureCollection([oneFeature])
                }
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
          readFile.readAsText(file);
        });     
        const result = await readFilePromise(file)
        if ( result ) {    
          setArea(result)
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

  useEffect(() => {
    const fetchData = ( async() => {
      setIsWorking(true);
      setDatasetName(dataset?.name)
      await loadSources(1);
      await loadAreasDatasets(1);
      setIsWorking(false);   
    })
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    fetchData();
  }, [user]); // eslint-disable-line

  useEffect(() => {
    if ( firstSourcesPage )
      loadSources(firstSourcesPage)
  }, [firstSourcesPage]); // eslint-disable-line

  useEffect(() => {
    if ( firstAreasPage )
      loadAreasDatasets(firstAreasPage)
  }, [firstAreasPage]); // eslint-disable-line

  useEffect(() => {
    if ( areasDataset && areasDataset.alternate ) {
      // reset filtered point
      // reset filter AOI
      configureMap()
    }
  }, [areasDataset]); // eslint-disable-line
  
  const configureMap = async () => {
    if ( updatedDataset && updatedDataset.points && updatedDataset.filter && areasDataset?.alternate ) {
      const areasMap = {
        layers : {
          points: updatedDataset.points,
          areas: areasDataset.alternate,
          area: updatedDataset.filter.aoi,
        },
        label: 'Area of Interest Selection',
      };
      setMap(areasMap);
    }
    setMap(null);   
  }

  const aoiSourceTypes = [ 
    { key: 'none', name: 'None' },
    { key: 'custom', name: 'Custom Polygon' },
    { key: 'dataset', name: 'Catalogue dataset'}
  ]
  
  const value = "Esempio per l&apos;anstract del dato Esempio per l&apos;anstract del dato " + 
                " Esempio per l&apos;anstract del dato Esempio per l&apos;anstract del dato Esempio per l&apos;anstract del dato " +
                " Esempio per l&apos;anstract del dato Esempio per l&apos;anstract del dato Esempio per l&apos;anstract del dato "
  
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      { (!dataset || !dataset.filter) && (
        <span className="font-bold text-red-800">Error: dataset or filter not initialized </span>
      )} 
      { dataset && dataset.filter  && (
        <>
        <Steps model={items} activeIndex={activeIndex} readOnly className="mb-4" />
        { activeIndex === 0  && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          <div className="flex flex-row w-full m-2">
            <Fieldset className="w-6" legend={t('NAME')}>
              <InputText className="w-full" value={datasetName} onChange={(e) => setName(e.target.value)} />
            </Fieldset>
            <Fieldset className="w-6" legend={t('DATE')}>
              <div> { formatDate(dataset.date) } </div>
            </Fieldset>
          </div>
          <div className="flex flex-row w-full m-2">
            <Fieldset className="w-6" legend={t('USER_NAME')}>
              <div className={className2}> {dataset.user_name} </div>
            </Fieldset>
            <Fieldset className="w-6" legend={t('USER_EMAIL')}>
              <div className={className2}> {dataset.user_email} </div>
            </Fieldset>
          </div>
          <div class="flex justify-content-center w-full m-2">
            <Button
              label={t("DS_SOURCE")}
              icon='pi pi-arrow-right'
              type='button'
              loading={isWorking}
              disabled={ isWorking }
              className='mt-4 flex'
              onClick={() => { goToSources() }} 
            /> 
          </div>
        </div>
        )}
        { activeIndex === 1 && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          <Fieldset className="w-full" legend={t('DS_SOURCE')}>
            { selectedSource && (
              <div className="flex flex-column gap-2 align-items-center justify-items-center w-full">
                <Button
                  icon='pi pi-trash'
                  type='button'
                  disabled={ isWorking }
                  onClick={() => { setSelectedSource(null); }}
                />
                <h5 className="font-bold text-cyan-800">{selectedSource.name}:</h5>
                { selectedSource.abstract && (
                <InputTextarea id="description" value={selectedSource.abstract} disabled rows={5} cols={30} />
                )}
                { !selectedSource.abstract && (
                  <h6>No descriptions</h6>
                )}
                { selectedSource.alternate && updatedDataset && !updatedDataset?.points && (
                <Button
                  icon='pi pi-save'
                  label={t("LOAD_POINTS")}
                  type='button'
                  disabled={ isWorking }
                  onClick={() => {  loadSrcPoints(); }}
                />
                )}
              </div>
            )}
            { !selectedSource && (
              <div className="card flex flex-column gap-3 align-items-center">
              { isWorking && (
                <Loading title="Loading..."/>
              )}
              { !isWorking && srcDatasetsList && srcDatasetsList.datasets && (srcDatasetsList.datasets.length > 0) && (
                <>
                  <h6 className="w-full surface-200 font-bold text-cyan-800 p-3 shadow-2">Available Sources</h6>
                  <ListBox value={selectedSource} onChange={(e) => { setSource(e.value); } } options={srcDatasetsList.datasets} 
                    optionLabel="name" className="md:w-20rem font-bold text-cyan-800" listStyle={{ maxHeight: '250px' }} />
                  <Paginator first={firstSourcesPage} rows={10} totalRecords={totalSources} onPageChange={onSourcesPageChange} template={{ layout: 'PrevPageLink CurrentPageReport NextPageLink' }} />
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
              label={t('BACK')}
              icon='pi pi-trash'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => setActiveIndex(0) }
            />
            <Button
              label={t("DS_AOI")}
              icon='pi pi-save'
              type='button'
              loading={ isWorking }
              disabled={ isWorking || !updatedDataset.points }
              className='mt-4 flex'
              onClick={() => { setActiveIndex(2); }} 
            /> 
          </div>
        </div>
        )}
        { activeIndex === 2 && (
        <div className="card flex flex-column gap-3 text-cyan-800 w-full justify-content-center">
          { map && (
            <AoiSelectionMap map={map} setArea={setArea} />
          )}
          <Fieldset className="w-full justify-content-center" legend={t('DS_AREAS')}>
            { dataset.filter?.aoi && (
                <div className="flex flex-row w-full">
                  <Button
                    label={t('RESET')}
                    icon='pi pi-trash'
                    type='button'
                    disabled={ isWorking }
                    className='mt-4 flex mr-4'
                    onClick={() => { setArea(null); }}
                  />
                  <span className="font-bold text-cyan-800">Aoi already selected, read the map </span>  
                </div>
            )}
            { !dataset.filter?.aoi && (
            <>  
            <div className="flex flex-wrap justify-content-center w-full gap-3">
              { aoiSourceTypes.map((aoiSourceType) => { return (
                <div key={aoiSourceType.key} className="flex align-items-center">
                  <RadioButton inputId={aoiSourceType.key} name="category" value={aoiSourceType} onChange={(e) => setSelectedAoiSourceType(e.value)} checked={selectedAoiSourceType?.key === aoiSourceType.key} />
                  <label htmlFor={aoiSourceType.key} className="ml-2">{aoiSourceType.name}</label>
                </div>
              )} )}
            </div>
            { selectedAoiSourceType?.key === "dataset" && (
              <div className="flex flex-column align-items-center justify-content-center w-full m-3">
                <span className="font-bold text-cyan-800">List of datasets in the catalogue  with &quot;boundaries&quot; as metadata topic category </span>
                { isWorking && (
                  <Loading title="Loading..."/>
                )}
                { !isWorking && areasDatasets && areasDatasets.datasets && areasDatasets.datasets.length && (
                  <>
                  <h6 className="w-full surface-200 font-bold text-cyan-800 p-3 shadow-2">Available Sources</h6>
                  <ListBox value={areasDataset} onChange={(e) => setAreasDataset(e.value)} options={areasDatasets.datasets} 
                    optionLabel="name" className="md:w-20rem font-bold text-cyan-800" listStyle={{ maxHeight: '250px' }} />
                  <Paginator first={firstAreasPage} rows={10} totalRecords={totalAreas} onPageChange={onAreasPageChange} 
                    template={{ layout: 'PrevPageLink CurrentPageReport NextPageLink' }} />
                  </>
                )}
                { ( !isWorking && ( !areasDatasets?.datasets || !areasDatasets.datasets?.length ) ) &&  (
                  <h6 className="font-bold text-cyan-800">No dataset available</h6>
                )}
              </div>
            )}  
            { selectedAoiSourceType?.key === "custom" && (
              <div className="flex flex-column">
                <span classname="font-bold text-cyan-800">Upload Custon Polygon:</span>
                <FileUpload 
                  disabled={aoiFileId !== null || working}
                  id="file"
                  ref={aoiFileRef}
                  accept='.json, .geojson'
                  chooseLabel={t('CHOOSE_FILE')}
                  mode="basic"
                  multiple={false}
                  customUpload
                  auto
                  className='mb-4 mr-2 mt-4'
                  uploadHandler={(e) => loadFile(e.files)}
                /> 
                {(aoiFileId !== null) && (
                <div class="flex flex-row mt-4 mb-4"> 
                  <Button
                      label={t('RESET')}
                      icon='pi pi-plus'
                      type='button'
                      disabled={validating || uploading}
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
          </Fieldset>
          <div class="flex justify-content-center w-full m-3">
            <Button
              label={t('BACK')}
              icon='pi pi-trash'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { setActiveIndex(1); }}
            />
            <Button
              label={t("DS_FILTERS")}
              icon='pi pi-save'
              type='button'
              loading={isWorking}
              disabled={ isWorking || !dataset.points || ( selectedAoiSourceType !== "none" && !dataset.aoi ) }
              className='mt-4 flex'
              onClick={() => { setActiveIndex(3); }} 
            /> 
          </div>
        </div>
        )}
        { activeIndex === 3 & (
          <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          </div>
        )}
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
