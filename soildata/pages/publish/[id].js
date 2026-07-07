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
  
  /* fetch dataset data */
  const fetchDataset = async (id) => {
    console.log('fetch')
    setLoading(true)
    try {
      const response = await ProfileService.get( document.cookie, id, 'datasets'  );
      if ( response && response.ok && response.data ){
        const ds = response.data
        setDataset (ds);
      }      
    } catch (error) {
      console.log(error);
      console.log('no data')
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

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    if (id)
      fetchDataset(id)
  },[user, id]);  // eslint-disable-line

return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <div className="card flex flex-reverse w-full m-4"> 
      <Button icon="pi pi-plus" className="mr-2 mb-2" label="List of Dataset" disabled={isWorking}
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
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Dataset Publishing Report</h5>
      </>
    )}  
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.ERRORS && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Errors generating dataset... </h5>   
      </>
    )} 
    { dataset && dataset.status !== ProfileService.DATASET_STATUSES.CREATED && 
      dataset.status !== ProfileService.DATASET_STATUSES.CONFIGURED &&
      dataset.status !== ProfileService.DATASET_STATUSES.ERRORS && 
      dataset.status !== ProfileService.DATASET_STATUSES.PUBLISHED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Dataset in elaboration... </h5>
      <div class="flex justify-content-center w-full m-3">
        <Button
          label={t("REFRESH")}
          icon='pi pi-save'
          type='button'
          disabled={ isWorking || !workDataset }
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
