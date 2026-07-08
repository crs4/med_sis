"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { ProfileService } from '../../service/profiles';
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
    // fetch soil indicators and points sections lists 
    fetchData();
  },[user]);  // eslint-disable-line
  
  const fetchData = async  () => {
    try {  
      setIsWorking(true);
      const _idata = await ProfileService.list(document.cookie,'base-datasets');
      setIsWorking(false);
      if ( !_idata || !_idata.ok || !_idata.data || !Array.isArray(_idata.data) || _idata.data.length === 0 )
        toast.current.show({severity:'error', summary: 'No data!', detail: 'Base datasets descriptors not found' , life: 3000});
      else { 
        const _indicators = _idata.data.filter((d) => d.type !== 'points_soil_data');
        const _sections = _idata.data.filter((d) => d.type === 'points_soil_data');
        // sort by name
        setIndicators( _indicators.sort((a, b) => {
            const n1 = a.code.toUpperCase(); // ignore upper and lowercase
            const n2 = b.code.toUpperCase(); // ignore upper and lowercase
            if (n1 < n2) return -1;
            if (n1 > n2) return 1;
            return 0 
        }));
        setSections( _sections.sort((a, b) => {
            const n1 = a.code.toUpperCase(); // ignore upper and lowercase
            const n2 = b.code.toUpperCase(); // ignore upper and lowercase
            if (n1 < n2) return -1;
            if (n1 > n2) return 1;
            return 0 
        }));
        toast.current.show({severity:'success', summary: 'Done!', detail: "Base Datasets descriptors list has been loaded" , life: 3000});
      }
      setIsWorking(false);
    } catch (error) {
      console.log(error)  
    }   
  }

  const delay = (ms) => new Promise(res => setTimeout(res, ms));

  const updateState = async () => {
    fetchData();
  }

  const typeTemplate = (rowData) => {
    if ( rowData.type ) {
      if ( rowData.type === "soil_physical_health" )
        return <span className="font-bold text-orange-800">{t('PHYSICAL_HEALTH')}</span>
      if ( rowData.type === "soil_chemical_health" )
        return <span className="font-bold text-purple-800">{t('CHEMICAL_HEALTH')}</span>
      if ( rowData.type === "soil_biological_health" )
        return <span className="font-bold text-green-800">{t('BIOLOGICAL_HEALTH')}</span>
      else
        return <span className="font-bold text-cyan-800">{t('POINTS_SOIL_DATA')}</span>
    } 
  }

  const statusTemplate = (rowData) => {
    if ( rowData.status ) {
      if ( rowData.status === 'TO_CONFIGURE' )
        return <span className="font-bold text-cyan-800">{t(rowData.status)}</span>
      if ( rowData.status === 'CREATED' )
        return <span className="font-bold text-cyan-800">{t("WATING_ELABORATION")}</span>
      if ( rowData.status === 'IN_PROCESS' )
        return <span className="font-bold text-orange-800">{t(rowData.status)}</span>
      if ( rowData.status === 'PUBLISHED' )
        return <span className="font-bold text-green-800">{t(rowData.status)}</span>
      if ( rowData.status === 'ERRORS' )
        return <span className="font-bold text-red-800">{t(rowData.status)}</span>
    } 
  }

  const actionTemplate = (rowData) => (
    <> 
    { rowData && rowData.status === 'TO_CONFIGURE' && (
      <Button
        icon="pi pi-wrench"
        className="p-mb-2 p-mr-2 m-1"
        disabled={isWorking}
        label={t('CONFIGURE')}
        onClick={() => configure(rowData)}
      />
    )}
    { rowData && rowData.geonode_id && rowData.status === 'PUBLISHED' && (
      <>
      <a href={ '/catalogue/#/dataset/' + rowData.geonode_id } >
        <Button
          icon="pi pi-desktop"
          tooltip={t('GOTO_CATALOGUE')}
          tooltipOptions={{ position: 'top' }}
          disabled={isWorking}
          className="m-2"
        />
      </a> 
      { rowData && rowData.type !== 'points_soil_data' && (
      <Button 
        icon="pi pi-replay"
        tooltip={t('RECONFIGURE')}
        tooltipOptions={{ position: 'top' }}
        disabled={isWorking}
        className="m-2"
        onClick={() => configure(rowData, true)}
      />
      )}
      { rowData && rowData.type === 'points_soil_data' && (
      <Button 
        icon="pi pi-replay"
        tooltip={t('RECONFIGURE')}
        tooltipOptions={{ position: 'top' }}
        disabled={isWorking}
        className="m-2"
        onClick={() => configure(rowData, true)}
      />
      )}
      </>
    )}
    { rowData && rowData.status === 'ERRORS' && (
      <Button
        icon="pi pi-replay"
        className="p-mb-2 p-mr-2 m-1"
        disabled={isWorking}
        label={t('RECONFIGURE')}
        onClick={() => configure(rowData)}
      />
    )}
    </>  
  )

  const configure = async (ds, isIndicator) => {
    try {
      ds.status = "CREATED"
      const resp = await ProfileService.update ( document.cookie, ds.code, ds, 'base-datasets' )
      if ( !resp || resp.status < 200 || resp.status >= 300  )
        toast.current.show({severity:'error', summary: 'Errors!', detail: "Errors starting configuration for dataset " + ds.code , life: 3000}); 
      else {
        toast.current.show({severity:'success', summary: 'Done!', detail: "Configuration started for dataset " + ds.code , life: 3000});
        if ( isIndicator ) {
          setIndicators(indicators)  
        }
        else {
          setSections(sections)
        } 
        return ds;
      }
         
    } catch (e) {
      console.log(e)
      
    }
    return null
  }

  const configureAll = async () => {
    try {
      setIsWorking(true)
      for ( let i = 0; i < indicators.length; i += 1 ){
        await new Promise(resolve => setTimeout(resolve, 3000)); 
        await configure( indicators[i] , true );
      }  
      for ( let i = 0; i < sections.length; i += 1 ){
        await new Promise(resolve => setTimeout(resolve, 3000)); 
        await configure(sections[i], false );
      }
      setIsWorking(false) 
      fetchData ()   
    } catch (e) {
      setIsWorking(false) 
      console(e)
    } 
  }

  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <div className="flex flex-row-reverse w-full p-2">
      <Button 
        icon="pi pi-wrench"
        className="flex bg-primary font-bold border-round m-4"
        disabled={isWorking}
        onClick={() => configureAll()}
        label={t('CONFIGURE_ALL_LAYERS')}
      />
      <Button 
        icon="pi pi-replay"
        className="flex bg-primary font-bold border-round m-4"
        disabled={isWorking}
        onClick={() => updateState()}
        label={t('REFRESH_LIST')}
      />
    </div>
    {( isWorking ) && (
        <h5 className="font-bold text-cyan-800">The browser is working; do not leave the page. </h5>
    )}
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('SOIL_INDICATOR')} Base Datasets</h5>
    {( indicators ) && (
      <DataTable
        value={indicators}
        paginator
        className="p-datatable-gridlines  text-cyan-800"
        showGridlines
        rows={20}
        loading={isWorking}
        responsiveLayout="scroll"
      >
        <Column header="Name" field="name" sortable className="font-bold text-cyan-800" style={{ minWidth: '10rem' }} />
        <Column header="Abstract" field="abstract" style={{ minWidth: '20rem' }} />
        <Column header="Category" field="type" sortable body={typeTemplate} style={{ minWidth: '10rem' }}   />
        <Column header="Status" field="status" sortable body={statusTemplate} style={{ minWidth: '10rem' }}   />
        <Column header="Actions" body={actionTemplate} style={{ minWidth: '10rem' }}  />
    </DataTable>
    )}
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('POINT_SOIL_DATA_SECTION')} Base Datasets</h5>
    {( sections ) && (
      <DataTable
          value={sections}
          paginator
          className="p-datatable-gridlines font-bold text-cyan-800"
          showGridlines
          rows={20}
          loading={isWorking}
          responsiveLayout="scroll"
        >
          <Column header="Name" field="name" sortable style={{ minWidth: '10rem' }} />
          <Column header="Abstract" field="abstract" style={{ minWidth: '20rem' }} />
          <Column header="Category" field="type" body={typeTemplate} style={{ minWidth: '10rem' }}   />
          <Column header="Status" field="status" body={statusTemplate} sortable style={{ minWidth: '10rem' }}   />
          <Column header="Actions" body={actionTemplate} />
        </DataTable>
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

