"use client"

import React, { useEffect, useState, useRef  } from 'react';
import { ProfileService } from '../../service/profiles';
import { userContext, useUser } from '../../context/user';
//import DatasetFilter from '../../components/DatasetFilter';
import Datasets from '../../data/datasets';
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
  
  const loadSrcPoints = async () => {
    if ( !dataset || !dataset.src_typename )
      return
    try {
      const response = await ProfileService.getDataset( dataset.src_typename, document.cookie )
      if ( response && response.ok && response.data && response.data.features ){
        dataset.points = response.data;
        setDataset(dataset)
        setSrcPoints(dataset.points)
        setFilteredPoints(dataset.points)
      }
      toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Source data has been loaded.'});
    } catch (e) {
      console.log(e);
      toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Data not available.'});
    }
    setLoading(false)     
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

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    setLoading(true)
    try {
      const response = ProfileService.getDataset( document.cookie, id, 'datasets'  );
      if ( response && response.ok && response.data )
        setDataset (response.data);    
    } catch (error) {
      console.log(error);
    }
    setLoading(false) 
  },[user]);  // eslint-disable-line

  useEffect(() => {
    loadSrcPoints()
  },[dataset]);  // eslint-disable-line

  useEffect(() => {
    const fetchMap = async () => {
      if ( dataset ) {
        const _mapData = {
          points: dataset.points,
          label: 'Filtered ' + dataset.source,
        };
        if ( dataset.filter && dataset.filter.aoi )
          _mapData.aoi = dataset.filter.aoi;
        setMapData(_mapData);
      }  
    }
    if ( dataset.points )
      fetchMap();
  }, [dataset]); // eslint-disable-line
//<DatasetFilter dataset={dataset} setDataset={setDataset} />
  

return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.CREATED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Configuring New Points Soil Dataset</h5>      
      </>
    )}
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.PREPROCESSED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Validating Points Soil Dataset</h5>
      </>
    )}  
    { dataset && dataset.status === ProfileService.DATASET_STATUSES.PUBLISHED && (
      <>
      <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Published Points Soil Dataset</h5>
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

