"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { ProfileService } from '../../service/profiles';
import BaseDatasets from '../../data/basedatasets';
import { useUser } from '../../context/user';
import Loading from '../../components/Loading';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';

import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { Card } from 'primereact/card'; 
import { Toast } from 'primereact/toast';   

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const toast = useRef(null);
  const [isWorking, setIsWorking] = useState(false);
  const [indicators, setIndicators] = useState([]);
  const [sections, setSections] = useState([]);

  useEffect(() => {
    // only administrators and data managers
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    // fetch soil indicators and points soildata lists 
    const fetchData = async  () => {
      setIsWorking(true);
      const _idata = await ProfileService.list(document.cookie,'base-datasets');
      setIsWorking(false);   
      if ( !_idata || !_idata.ok || !_idata.data || !Array.isArray(_idata.data) || _idata.data.length === 0 )
        toast.current.show({severity:'error', summary: 'No data!', detail: 'Base datasets descriptors not found' , life: 3000});
      else { 
        const _indicators = _idata.data.filter((d) => d.type === 'SOIL_INDICATOR');
        const _sections = _idata.data.filter((d) => d.type === 'POINT_SOIL_DATA_SECTION');
        setIndicators(_indicators)
        setSections(_sections)
        toast.current.show({severity:'success', summary: 'Done!', detail: "Base Datasets descriptors list has been loaded" , life: 3000});
      }
      setIsWorking(false);   
    }
    fetchData();
  },[user]);  // eslint-disable-line
              
  const statusTemplate = (rowData) => (
    <>
    { !rowData.check  && (
    <Button
      icon="pi pi-times"
      className="p-mb-2 p-mr-2 m-1"
      severity="danger"
      label=""
      tooltip={t('DATASET_NOT_INITIALISED')}
      tooltipOptions={{ position: 'top' }}
    />
    )}
    { rowData.check  && (
    <Button
      icon="pi pi-check"
      className="p-mr-2 p-mb-2 m-1"
      severity="success"
      tooltip={t('DATASET_INITIALISED')}
      tooltipOptions={{ position: 'top' }}
      label=""
    />
    )}
    </> 
  );

  const updateLayers = async () => {
    setIsWorking(true)
    const resp = await ProfileService.doFetchBackOffice ( 'updatelayers', null, 'POST', {}, document.cookie)
    setIsWorking(false)
    console.log(resp)
    if ( !resp || resp.status < 200 || resp.status >= 300  ){
        toast.current.show({severity:'error', summary: 'Errors!', detail: "Errors configuring base datasets" , life: 3000}); 
    }
    else  toast.current.show({severity:'success', summary: 'Done!', detail: "base datasets configuration started it take about 10 minutes" , life: 3000});  
  }

  const header1 = (
    <div className="flex justify-content-center w-full">
        <h4 className="font-bold text-cyan-800 p-3 mb-3">{t('SOIL_INDICATORS')}</h4>   
    </div>
  )

  const header2 = (
    <div className="flex justify-content-center w-full">
        <h4 className="font-bold text-cyan-800 p-3 mb-3">{t('POINT_SOIL_DATA_SECTIONS')}</h4>   
    </div>
  )

  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <div className="flex flex-row-reverse w-full p-2">
      <Button 
        icon="pi pi-wrench"
        className="flex bg-primary font-bold border-round"
        disabled={isWorking}
        onClick={() => updateLayers()}
        label={t('UPDATE_LAYERS')}
      />
      <Button 
        icon="pi pi-wrench"
        className="flex bg-primary font-bold border-round"
        disabled={isWorking}
        onClick={() => updateLayers()}
        label={t('INITIALIZE_LAYERS')}
      />
    </div>
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Base datasets</h5>
    {( isWorking ) && (
        <h4 className="font-bold text-cyan-800">Loading Descriptors...</h4>
    )}
    { indicators && !isWorking && ( 
      <>
        <DataTable
          value={indicators}
          paginator
          dataKey="code"
          className="p-datatable-gridlines"
          showGridlines
          rows={20}
          loading={isWorking}
          responsiveLayout="scroll"
          emptyMessage="Soil Indicators not found"
          header={header1}
        >
          <Column header="Name" field="name" sortable style={{ minWidth: '10rem' }} />
          <Column header="Abstract" field="abstract" style={{ minWidth: '40rem' }} />
          <Column header="Type" field="type" sortable style={{ minWidth: '10rem' }}   />
          <Column header="keywords" field="keywords" sortable style={{ minWidth: '10rem' }}   />
          <Column header="Status" field="status" sortable style={{ minWidth: '10rem' }}   />
          <Column header="Actions" body={statusTemplate} />
        </DataTable>
      </>
    )}
    { sections && !isWorking && ( 
      <>
        <DataTable
          value={indicators}
          paginator
          dataKey="code"
          className="p-datatable-gridlines"
          showGridlines
          rows={20}
          loading={isWorking}
          responsiveLayout="scroll"
          emptyMessage="Soil Indicators not found"
          header={header1}
        >
          <Column header="Name" field="name" sortable style={{ minWidth: '10rem' }} />
          <Column header="Abstract" field="abstract" style={{ minWidth: '40rem' }} />
          <Column header="Type" field="type" sortable style={{ minWidth: '10rem' }}   />
          <Column header="keywords" field="keywords" sortable style={{ minWidth: '10rem' }}   />
          <Column header="Status" field="status" sortable style={{ minWidth: '10rem' }}   />
          <Column header="Actions" body={statusTemplate} />
        </DataTable>
      </>
    )}    
  </div>
  );
};

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}

