"use client"

import React, { useEffect, useState, useRef  } from 'react';
import { ProfileService } from '../../service/profiles';
import { userContext, useUser } from '../../context/user';
import ConfigureDataset from '../../components/ConfigureDataset';
import ValidateDataset from '../../components/ValidateDataset';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { Toast } from 'primereact/toast';
import { clone, featureCollection } from '@turf/turf';

/*
* This page allows different actions on new soil point datasets to publish on MED-SIS
* 1) View dataset configuration for published dataset.
* 2) Configure dataset for preprocessing: 
*  - Filters ( Area Of Interest, Depth, Project, Type, Project ),
*  - Interpolation parameters 
* 3) Validate preprocessed data 
*/ 
export default function Page()  {
  const t = useTranslations('default');
  const [dataset, setDataset] = useState(null);
  const [srcPoints, setSrcPoints] = useState(null);
  const [mapData, setMapData] = useState(null);
  const user = useUser();
  const router = useRouter();
  const toast = useRef(null);
  const [loading, setLoading] = useState(false);
  
  const id = router.query.id
  
 

  const updateDataset = async (updated) => {
    if ( updated )
      setDataset(updated)
  }

  const validate = () => {
    if ( dataset )
      try {
        dataset.status = ProfileService.DATASET_STATUSES.VALIDATED;
        const response = ProfileService.updateDataset( 'dataset', dataset, document.cookie );
        if ( response && response.ok ) {
          toast.current.show({severity:'success', summary: 'Success!', detail: 'Data has been updated' , life: 3000});
          setTimeout(() => {
            router.push('/dataset') 
          }, 3000);
        } 
        else toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Dataset not updated.'});   
      } catch (error) {
        console.log(error);
        toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Dataset not updated.'});
      }
  }

  const fetchDataset = async (id) => {
    setLoading(true)
    try {
      const response = await ProfileService.get( document.cookie, id, 'datasets'  );
      if ( response && response.ok && response.data )
        setDataset (response.data);    
    } catch (error) {
      console.log(error);
    }
    setLoading(false) 
  }

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    if (id)
      fetchDataset(id)
  },[user]);  // eslint-disable-line


  useEffect(() => {
    const fetchMap = async () => {
      if ( dataset ) {
        const _mapData = {
          areas : null,
          points: dataset.points,
          label: 'Filtered ' + dataset.source,
        };
        if ( dataset.filter && dataset.filter.aoi )
          _mapData.area = dataset.filter.aoi;
        setMapData(_mapData);
      }  
    }
    if ( dataset && dataset.points && dataset.points !== {}  )
      fetchMap();
  }, [dataset]); // eslint-disable-line
  

return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.CREATED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Configuring Dataset</h5>
      <ConfigureDataset dataset={dataset} setDataset={updateDataset} />     
      </>
    )}
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.PROCESSED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Validating Dataset</h5>
      <ValidateDataset dataset={dataset} /> 
      </>
    )}  
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.PUBLISHED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Published Dataset</h5>
       
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

