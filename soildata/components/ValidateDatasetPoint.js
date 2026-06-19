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

import ProfileService from '../service/profiles';
import TaxonomyService from '../service/taxonomies';
import dynamic from 'next/dynamic'

const PointsFilterMap = dynamic(() => import("./map/PointsFilterMap"), { ssr:false })

export default function ValidateDatasetPoint( { dataset, setDataset })  { 
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  const [isWorking, setIsWorking] = useState(false);
  const [workDataset, setWorkDataset] = useState(dataset);
  const [descriptors, setDescriptors] = useState([]);
  
  function generateDescriptors (_workDataset) {
    const _descriptors = [
      { name: "Name", value: _workDataset.name },
      { name: "Owner", value: _workDataset.user_email },
      { name: "Date", value: _workDataset.date },
      { name: "Source", value: _workDataset.source },
    ]
    if ( _workDataset.points)
      _descriptors.push({ name: "Source points", value: ( _workDataset.points.features ? _workDataset.points.features.length : 0 ) })
    else
      _descriptors.push({ name: "Source points", value: 0 })
    if ( _workDataset.filter.points)
      _descriptors.push({ name: "Filtered points", value: ( _workDataset.filter.points.features ? _workDataset.filter.points.features.length : 0 ) })
    else
      _descriptors.push({ name: "Filtered points", value: 0 })
    setDescriptors(_descriptors);
  }

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
        return true; 
      } 
      else toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset configuration' , life: 3000});
    } catch (error) {
      console.log(error)
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving dataset' , life: 3000}); 
    }
    setIsWorking(false) 
    return false;
  } 

  // publish new dataset
  const finalizeDataset = async () => {
    /* publish in the catalogue */ 
    workDataset.status = ProfileService.DATASET_STATUSES.VALIDATED
    setWorkDataset(workDataset)
    await saveWorkDataset()
    openList()
  } 

  // Re-configure
  const backToConfiguration = async () => {
    workDataset.status = ProfileService.DATASET_STATUSES.CREATED
    setWorkDataset(workDataset)
    await saveWorkDataset()
  }

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    if ( dataset ) {
      const _workDataset = dataset;
      setWorkDataset(_workDataset);
      generateDescriptors(_workDataset)
    }
  }, [user]); // eslint-disable-line

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
          <PointsFilterMap points={workDataset.filter.points} area={workDataset.filter.aoi}  />
        </div>
        <div className="flex flex-column gap-2 text-cyan-800 md:w-6 sm:w-full m-2">
          <h5 className="flex justify-content-center w-full text-cyan-800"> New Dataset Descriptor</h5>
          <DataTable value={descriptors} tableStyle={{ minWidth: '40rem' }}>
            <Column field="name" header="" style={{ width: '25%' }}></Column>
            <Column field="value" header="" ></Column>
          </DataTable>
        </div>
      </div>  
      
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
