"use client"

import React, { useEffect, useState, useRef  } from 'react';
import { ProfileService } from '../../service/profiles';
import { userContext, useUser } from '../../context/user';
import ConfigureDataset from '../../components/ConfigureDataset';
import ValidateDataset from '../../components/ValidateDataset';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { Toast } from 'primereact/toast';
import { Button } from 'primereact/button';
import { clone, featureCollection } from '@turf/turf';

import { Card } from 'primereact/card';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Timeline } from 'primereact/timeline';
/*
* This page allows different actions on soilindicators base datasets 
* to publish new dataset on MED-SIS for End User
* 1) Select source dataset.
* 2) Filter source dataset to create new dataset.
* 3) optionally execute a Kriging Interpolation on the new dataset 
* 4) Publish the new datasets on catalogue. 
* Finally using Catalogue functionalities you can 
* - Edit new dataset metadata 
* - Manage permissions for the new dataset to permit access to the End User 
*/ 
export default function Page()  {
  const t = useTranslations('default');
  const user = useUser();
  const router = useRouter();
  const [dataset, setDataset] = useState(null); /* New dataset data */
  const id = router.query.id; /* Id of the new dataset */
  const toast = useRef(null);
  const [loading, setLoading] = useState(false);
  const [descriptors, setDescriptors] = useState([]);
  
  /* fetch dataset data */
  const fetchDataset = async (id) => {
    setLoading(true)
    try {
      const response = await ProfileService.get( document.cookie, id, 'datasets'  );
      if ( response && response.ok && response.data ){
        const ds = response.data
        generateDescriptor(ds)
        setDataset (ds);
      }      
    } catch (error) {
      console.log(error);
    }
    setLoading(false) 
  }

  const goToList = () => {
    router.push(`/publish/`);
  };

  const reload = () => {
    if (id)
      router.push(`/publish/${id}`);
  };

  function generateDescriptor ( _dataset) {
    if ( !_dataset )
      return null;

    const _descriptors = [
      { name: "Name", value: _dataset.name },
      { name: "Owner", value: _dataset.user_email },
      { name: "Date", value: _dataset.date },
      { name: "Source", value: _dataset.source },
    ]
    if ( _dataset.points)
      _descriptors.push({ name: "Source points", value: ( _dataset.points.features ? _dataset.points.features.length : 0 ) })
    if ( _dataset.filter.points)
      _descriptors.push({ name: "Filtered points", value: ( _dataset.filter.points.features ? _dataset.filter.points.features.length : 0 ) })
    else
      _descriptors.push({ name: "Filtered points", value: 0 })
    if ( _dataset.context !== ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA && _dataset.k_data ){
      const len = (_dataset.k_data.features ? _dataset.k_data.features.length : 0);
      _descriptors.push({ name: "Aggregated points", value: len })  
    }
    setDescriptors(_descriptors)
  }

  const customizedMarker = (item) => {
    console.log(item)
    return (
        <span className="flex w-2rem h-2rem align-items-center justify-content-center text-white border-circle z-1 shadow-1" 
          style={{ backgroundColor: item.ok? '#55EE55' : '#EE5555' }}>
            <i className={item.ok? 'pi pi-check' : 'pi pi-times' }></i>
        </span>
    );
  };

  const customizedContent = (item) => {
    return (
        <Card> <p> Stage:{item.stage}, {item.text}</p> </Card>
    );
  };

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    if (id && !dataset)
      fetchDataset(id)
  },[user, id]);  // eslint-disable-line

return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <div className="card flex flex-reverse w-full m-4"> 
      <Button icon="pi pi-plus" className="mr-2 mb-2" label="List of Dataset" disabled={loading}
        tooltip={t('DATASET_LIST')} tooltipOptions={{ position: 'top' }}
        onClick={() => goToList()}
      />
    </div>
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.CREATED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Configuring Dataset</h5>
      { dataset && (
        <ConfigureDataset 
          isIndicators={ !(dataset.context === ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA) }
          dataset={dataset} 
          setDataset={setDataset} />     
      )}
      </>
    )}
    { dataset && ( dataset.status === ProfileService.DATASET_STATUSES.CONFIGURED || dataset.status === ProfileService.DATASET_STATUSES.ERRORS ) && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Validating Dataset</h5>
      { dataset && (
        <ValidateDataset 
          isIndicators={ !(dataset.context === ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA) }
          dataset={dataset} 
          setDataset={setDataset} />     
      )}
      </>
    )}
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.PUBLISHED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Dataset Published</h5>
      <div className="flex flex-column gap-2 align-content-start text-cyan-800 md:w-6 sm:w-full m-2">
        <h5 className="flex justify-content-center w-full text-cyan-800">Reports </h5>
        <DataTable className="font-bold text-cyan-800"  value={descriptors} tableStyle={{ minWidth: '40rem' }}>
          <Column field="name" header="" style={{ width: '25%' }}></Column>
          <Column field="value" header=""  className="text-yellow-800" ></Column>
        </DataTable>
        <div className="flex flex-row gap-2">
          <div className="flex flex-column gap-2 min-w-max">
            <h5 className="flex justify-content-center w-full text-cyan-800">Elaboration flow</h5>
            <Timeline value={dataset.report?.msgs} align="alternate" className="customized-timeline" marker={customizedMarker} content={customizedContent} />
          </div>
          { dataset.report.style &&  (  
          <div flex flex-column gap-2> 
            <h5 className="flex justify-content-center w-full text-cyan-800">Proposed Raster Style:</h5>
            <div className="card flex flex-column gap-1 font-italic">
              { dataset.report.style }
              { dataset.report.style.split('\n').forEach ( (e) => ( <span>pippo</span> ) ) }
            </div>
          </div>
          )}  
        </div>
      </div>
      </>
    )}  
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.ERRORS && (
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Errors generating dataset... </h5>   
    )} 
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.IN_PROCESS && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Dataset in elaboration... </h5>
      <div class="flex justify-content-center w-full m-3">
        <Button
          label={t("REFRESH")}
          icon='pi pi-save'
          type='button'
          disabled={ loading || !dataset }
          className='mt-4 flex'
          onClick={() => { reload() }} 
        />
      </div>    
      </>
    )}  

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
