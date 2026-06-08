"use client"

import { PTFService } from '../../service/ptf';
import { FilterMatchMode, FilterOperator } from 'primereact/api';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog } from 'primereact/confirmdialog'; 
import { Tag } from 'primereact/tag';
import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';
import {useTranslations} from 'next-intl';
import { Toast } from 'primereact/toast';
import { useUser } from '../../context/user';


export default function Page()  {
  const t = useTranslations('default');
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState('');   
  const [isWorking, setIsWorking] = useState(false);
  const [current, setCurrent] = useState(null);
  const [visibleDlg1, setVisibleDlg1] = useState(false);
  const [loading, setLoading] = useState(true);
  const [models, setModels] = useState(null);
  const router = useRouter();
  const toast = useRef(null);
  const user = useUser();
  const statuses = Object.keys(PTFService.STATUSES);
  
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    const fetchData = ( async() => {
      let _data = await PTFService.list(document.cookie)
      if ( !_data || _data.error )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading models' , life: 3000});
      else if ( !_data.data || !Array.isArray(_data.data) || _data.data.length === 0 ) 
        toast.current.show({severity:'warn', summary: 'No data!', detail: 'No models Found' , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The model list has been loaded' , life: 3000});
        setModels(mapModels(_data.data));
        initFilters();
      }
      setLoading(false); 
    })
    fetchData();
  },[user]);  // eslint-disable-line

  const goToModel = (id) => {
    router.push(`/hydroptf/${id}`);
  };

  const openCreate = () => {
    router.push(`/hydroptf/create`);
  };

  const removeModel = async (id) => {
    if ( !id || current )
      return;
    setIsWorking(true);
    setCurrent(id);
    setVisibleDlg1(true);
  };

  const performRemove = async () => {
    if ( !current )
      return;
    const res = await PTFService.remove(document.cookie,current);
    if ( res.status != 204 && res.status != 202 && res.status != 203 ) {
        toast.current.show({severity:'Error', summary: 'Error', detail:'Errors deleting HydroPTF model ' + current, life: 3000});
    }
    else  {
        setModels((omp) => (omp.filter((p) => p.id !== current)));
        toast.current.show({severity:'success', summary: 'Done!', detail:'HydroPTF Model ' + current +' has been deleted', life: 3000});
    } 
    initFilters();
    setCurrent(null);
    setIsWorking(false);
  };  

  const clearFilters = () => {
    initFilters();
  };

  const onGlobalFilterChange = (e) => {
    const value = e.target.value;
    let _filters = { ...filters };
    _filters['global'].value = value;
    setFilters(_filters);
    setGlobalFilterValue(value);
  };

  const renderHeader = () => {
    return (
        <div className="flex justify-content-between">
            <Button outlined icon="pi pi-filter-slash" label="Clear" onClick={clearFilters} />
            <span className="p-input-icon-left">
                <i className="pi pi-search" />
                <InputText value={globalFilterValue} onChange={onGlobalFilterChange} placeholder={t('SEARCH')} />
            </span>
        </div>
    );
  };

  const rejectDlg1 = () => {
    setCurrent(null);
    setIsWorking(false);
  };

  const formatDate = (value) => {
    return value.toLocaleDateString('en-US', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
  };

  const initFilters = () => {
    setFilters({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      id: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      title: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      editor: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      date: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      status: {
        operator: FilterOperator.OR,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
    });
    setGlobalFilterValue('');
  };
  
  const dateBodyTemplate = (rowData) => {
      return formatDate(rowData.date);
  };

  const dateFilterTemplate = (options) => {
      return <Calendar value={options.value} onChange={(e) => options.filterCallback(e.value, options.index)} dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" mask="99/99/9999" />;
  };

  const statusBodyTemplate = (rowData) => {/*
    if ( rowData.status === PTFService.STATUSES.IMPORT_SUCCESS )
      return ( <Tag icon="pi pi-check" severity="success" value="All saved"></Tag>)
    else if ( rowData.status === HYDROPTFService.STATUSES.IMPORT_WITH_ERROR )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="warning" value="Some Errors"></Tag>)
    else if ( rowData.status === HYDROPTFService.STATUSES.IN_PROCESS )
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Elaborating"></Tag>)
    else if ( rowData.status === HYDROPTFService.STATUSES.HYDROPTFED )
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Waiting"></Tag>)
    else if ( rowData.status === HYDROPTFService.STATUSES.CRITICAL_ERROR )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="Critical error"></Tag>)*/
  };

  const statusFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={statuses} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={statusItemTemplate} placeholder="Select a Status" className="p-column-filter" showClear />;
  };

  const statusItemTemplate = (option) => { /*
    if ( option === HYDROPTFService.STATUSES.IMPORT_SUCCESS )
      return ( <Tag severity="success" value="All saved"></Tag>)
    else if ( option === HYDROPTFService.STATUSES.IMPORT_WITH_ERROR )
      return ( <Tag severity="warning" value="Some Errors"></Tag>)
    else if ( option === HYDROPTFService.STATUSES.HYDROPTFED )
      return ( <Tag severity="info" value="Waiting"></Tag>)
    else if ( option === HYDROPTFService.STATUSES.IN_PROCESS )
      return ( <Tag severity="info" value="Elaborating"></Tag>)
    else if ( option === HYDROPTFService.STATUSES.CRITICAL_ERROR )
      return ( <Tag severity="danger" value="Critical error"></Tag>) */
  };

  

  const header = renderHeader();

  const mapModels = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        return d;
    });
  };

  const actionsTemplate = (rowData) => (
    <>
    { (rowData.status !== PTFService.STATUSES.IN_PROCESS &&
       rowData.status !== PTFService.STATUSES.UPLOADED
      ) && (
    <>     
    <Button
      icon="pi pi-times"
      className="p-button-danger p-mb-2 p-mr-2 m-1"
      label=""
      loading={loading}
      disabled={isWorking}
      tooltip={t('DELETE_HYDROPTFMODEL')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeModel(rowData.id) }
      aria-controls={visibleDlg1 ? 'dlg_remove' : null} 
      aria-expanded={visibleDlg1 ? true : false}
    />
    <Button
      icon="pi pi-folder-open"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('SHOW_MODEL')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToModel(rowData.id)}
      label=""
    />
    </>
    )}
    </> 
  );

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('HYDROPTF_LIST')}</h4>
      <div className="card text-cyan-800">
      { models && !loading && ( 
        <>
        <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlg1} onHide={() => setVisibleDlg1(false)} message="Are you sure you want to delete Hydro PTF model?" 
          header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg1} />
        <div className="flex flex-row-reverse w-full p-2">
          <Button 
            icon="pi pi-download"
            className="flex bg-primary font-bold border-round"
            disabled={isWorking}
            onClick={() => openCreate()}
            label={t('NEW_HYDROPTF')}
          />
        </div>
        <DataTable
          value={models}
          paginator
          dataKey="id"
          className="p-datatable-gridlines"
          globalFilterFields={['id', 'title', 'editor', 'type', 'status']}
          showGridlines
          rows={20}
          filters={filters}
          filterDisplay="menu"
          loading={loading}
          responsiveLayout="scroll"
          emptyMessage="No Hydro PTF models found."
          header={header}
        >
          <Column header="Identifier" field="id"  filter filterPlaceholder="Search by id" style={{ minWidth: '8rem' }} />
          <Column header="Name" field="title"  filter filterPlaceholder="Search by name" style={{ minWidth: '14rem' }} />
          <Column header="Editor" field="editor"  filter filterPlaceholder="Search by user" style={{ minWidth: '12rem' }} />
          <Column header="Date"  field="date" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
          <Column header="Type"  field="type" filterMenuStyle={{ width: '10rem' }} style={{ minWidth: '10rem' }} body={typeBodyTemplate} filter filterElement={typeFilterTemplate} />
          <Column header="Operation"  field="operation" filterMenuStyle={{ width: '12rem' }} style={{ minWidth: '14rem' }} body={operationBodyTemplate} filter filterElement={operationFilterTemplate} />
          <Column header="Status"  field="status" filterMenuStyle={{ width: '12rem' }} style={{ minWidth: '12rem' }} body={statusBodyTemplate} filter filterElement={statusFilterTemplate} />
          <Column header="Actions" body={actionsTemplate} style={{ minWidth: '10rem' }} />
        </DataTable>
        </>
      )}
      {(!models && !loading ) && (
          <h5 className="font-bold text-cyan-800">No Hydro PTF models found</h5>
      )}
      {(loading ) && (
          <h5 className="font-bold text-cyan-800">Loading Hydro PTF model info...</h5>
      )}
      </div>
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

