"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';

import { ProfileService } from '../../service/profiles';
import { useUser } from '../../context/user';
import Loading from '../../components/Loading';

import { FilterMatchMode, FilterOperator } from 'primereact/api';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { InputText } from 'primereact/inputtext';
import { Dialog } from 'primereact/dialog';
import { ConfirmDialog } from 'primereact/confirmdialog'
import { Fieldset } from 'primereact/fieldset'
import { ListBox } from 'primereact/listbox' 
import { Toast } from 'primereact/toast';
import { Tag } from 'primereact/tag';
   

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const toast = useRef(null);
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState(''); 
  const [visibleRemoveDlg, setVisibleRemoveDlg] = useState(false);
  const [visibleCloneDlg, setVisibleCloneDlg] = useState(false);
  const [visibleCreateDlg, setVisibleCreateDlg] = useState(false);
  const [isWorking, setIsWorking] = useState(false);
  const [selected, setSelected] = useState(null); 
  const [datasets, setDatasets] = useState([]); 

  const goToDataset = (id) => {
    router.push(`/datasets/${id}`);
  };

  const createDataset = async () => {
    if ( !isWorking ) {
      setSelected(null);
      setVisibleCreateDlg(true);
    }
  };

  const performCreate = async () => {
    setIsWorking(true)
    const dataset = {
        date : formatDate(Date.now()),
        name : user.userData.preferred_username+':'+formatDate(Date.now()),
        points : "{}",
        user_email : user.userData.email, 
        user_name : user.userData.preferred_username, 
        k_variogram : "{}",
        k_gn_raster : null,  // geonode id
        catalogue_id : null,  // geonode id
        source : null,
        src_typename : null,
        typename : null,
        filter : "{}",
        kriging : false,
        k_params : "{}",
        k_data : "{}",
        context : ProfileService.DATASET_CONTEXT.SOIL_INDICATOR,
        status : ProfileService.DATASET_STATUSES.CREATED
    }
    try {
      const response = await ProfileService.save( document.cookie, dataset, 'datasets' );
      if ( response.ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'dataset ' + response.data.id + ' has been created', life: 3000});
        setTimeout(() => {
          router.push('/datasets') 
        }, 3000); 
      }
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors creating dataset', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    } 
    setIsWorking(false);
    setSelected(null);
    initFilters();  
  };

  const cloneDataset = async (id) => {
    if ( !id || isWorking )
      return;
    const req = datasets.map( (e) => e.id === id )
    if ( req[0] ) {
      setSelected(id);
      setVisibleCloneDlg(true);
    }
    else toast.current.show({severity:'error', summary: 'Error', detail:'Errors dataset data not found', life: 3000}); 
  };

  const performClone = async () => {
    if ( !selected )
      return;
    setIsWorking(true);
    try {
      const response = await ProfileService.get( document.cookie, selected, 'datasets' );
      if ( response && response.ok && response.data ) {
        let dataset = {
          ...response.data, 
          date : formatDate(Date.now()),
          name : user.userData.preferred_username+':'+formatDate(Date.now()),
          user_name : user.userData.preferred_username,
          user_email : user.userData.email, 
          points : "{}",
          k_variogram : "{}",
          k_gn_raster : null,  // geonode id
          catalogue_id : null,  // geonode id
          typename : null,
          k_data : "{}",
          context : ProfileService.DATASET_CONTEXT.SOIL_INDICATOR,
          status : ProfileService.DATASET_STATUSES.CREATED
        }
        
        const response = await ProfileService.save( document.cookie, dataset, 'datasets' );
        if ( response.ok ) {
          toast.current.show({severity:'success', summary: 'Done!', detail:'dataset ' + response.data.id + ' has been created', life: 3000});
          setTimeout(() => {
            router.push('/datasets') 
          }, 3000); 
        }
        else 
          toast.current.show({severity:'error', summary: 'Error', detail:'Errors creating dataset', life: 3000});
      }
    } catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    } 
    setIsWorking(false);
    setSelected(null);
    initFilters();   
  };

  const removeDataset = async (id) => {
    if ( !id )
      return;
    const req = datasets.map( (e) => e.id === id )
    if ( req[0] ) {
      setSelected(id);
      setVisibleRemoveDlg(true);
    }
    else toast.current.show({severity:'error', summary: 'Error', detail:'Errors dataset data not found', life: 3000}); 
  };
  
  const performRemove = async () => {
    if ( !selected )
      return;
    setIsWorking(true);
    try {
      const resp = await ProfileService.remove( document.cookie, selected, 'datasets');
      if ( resp.ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'dataset info ' + selected + ' has been deleted', life: 3000});
        setDatasets(datasets.map( (e) => e.id !== selected ));
      }
      else toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting data', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    setIsWorking(false);
    setSelected(null);
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
        <Button outlined icon="pi pi-filter-slash" label="Clear" onClick={initFilters} />
          <span className="p-input-icon-left">
            <i className="pi pi-search" />
            <InputText value={globalFilterValue} onChange={onGlobalFilterChange} placeholder={t('SEARCH')} />
          </span>
        </div>
    );
  };

  const renderHeaderDlg = () => {
    return (
      <h5 className="w-7 surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2"> {t('CREATE_DATASET')}</h5>
    )
  };  
  
  const rejectDlg = () => {
    setSelected(null);
  };
  
  const setDates = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        return d;
    });
  }; 

  const formatDate = (value) => {
    const date = new Date(value).toJSON()
    date = date.substring(0,10)
    return date
  };
  
  const initFilters = () => { 
    setFilters({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      id: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      name: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      date: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      source: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      username: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      useremail: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
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

  const header = renderHeader();

  const headerDlg = renderHeaderDlg();

  const actionsTemplate = (rowData) => (  
    <>
    <Button icon="pi pi-folder-open"
      className="mr-2 mb-2"
      label=""
      tooltip={t('INSPECT_DATASET')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToDataset(rowData.id)}
      aria-controls={visibleCreateDlg ? 'Show the request data' : null}
      aria-expanded={visibleCreateDlg ? true : false}
    />
    <Button icon="pi pi-clone"
      className="mr-2 mb-2"
      label=""
      loading={isWorking}
      disabled={isWorking}
      tooltip={t('CLONE_DATASET')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => cloneDataset(rowData.id)}
    />
    <Button icon="pi pi-times"
      className="p-button-danger mb-2 mr-2"
      label=""
      loading={isWorking}
      disabled={isWorking}
      tooltip={t('DELETE_DATASET')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeDataset(rowData.id) }
      aria-controls={visibleRemoveDlg ? 'open dialog remove request' : null}
      aria-expanded={visibleRemoveDlg ? true : false}
    />
    </> 
  );
 
  const fetchData = async  () => {
    setIsWorking(true);
    const response = await ProfileService.list(document.cookie,'datasets');
    if ( !response || !response.ok )
      toast.current.show({severity:'error', summary: t('ERRORS'), detail:t('ERRORS_READING_DATASET') , life: 3000});
    else if ( !response.data || !Array.isArray(response.data) || response.data.length === 0 ) 
      toast.current.show({severity:'warn', summary: t('EMPTY'), detail:t('NO_DATASETS_FOUND') , life: 3000});
    else { 
      toast.current.show({severity:'success', summary: t('SUCCESS'), detail:t('DATASETS_LOADED') , life: 3000});
    } 
    setDatasets(setDates(response.data)); 
    initFilters();
    setIsWorking(false); 
  }
    
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    fetchData(); 
  },[user]);  // eslint-disable-line

  const statusBodyTemplate = (rowData) => {
    if ( rowData.status === ProfileService.DATASET_STATUSES.CREATED )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="To configure"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.CONFIGURED || 
              rowData.status === ProfileService.DATASET_STATUSES.VALIDATED || 
              rowData.status === ProfileService.DATASET_STATUSES.IN_PROCESS ) 
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Elaborating"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.PROCESSED )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="To evaluate"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.PUBLISHED )
      return ( <Tag icon="pi pi-check" severity="success" value="Published"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.ERRORS )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="Errors"></Tag>)
  };

  const className1 = 'col-6 font-bold text-cyan-800 mt-1 mb-1';
  const className2 = 'col-6 text-green-800 mt-1 mb-1';

  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2"> {t('DATASETS_LIST')}</h5>
    <div className="card text-cyan-800" >      
    {(isWorking) && (
      <Loading  title={t('LOADING')} />
    )} 
      <div className="card flex flex-reverse w-full m-3"> 
        <Button icon="pi pi-plus" className="mr-2 mb-2" label="New Dataset" disabled={isWorking}
          tooltip={t('CREATE_DATASET')} tooltipOptions={{ position: 'top' }}
          onClick={() => createDataset()}
        />
      </div>
      <ConfirmDialog id="dlg_create" group="declarative"  visible={visibleCreateDlg} onHide={() => setVisibleCreateDlg(false)} 
          message="Are you sure you want to create the new dataset?" 
          header="Confirmation" icon="pi pi-plus" accept={performCreate} reject={rejectDlg} />
      <ConfirmDialog id="dlg_create" group="declarative"  visible={visibleCloneDlg} onHide={() => setVisibleCloneDlg(false)} 
          message="Are you sure you want to create the cloned dataset?" 
          header="Confirmation" icon="pi pi-plus" accept={performClone} reject={rejectDlg} />
      <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleRemoveDlg} onHide={() => setVisibleRemoveDlg(false)} 
          message="Are you sure you want to delete the Dataset? (Note: this doesn't remove the dataset in the catalogue.)" 
          header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg} />
      
      <DataTable value={datasets} paginator dataKey="id" className="p-datatable-gridlines"
        globalFilterFields={['id','name','date','source','username','useremail','status']}
        showGridlines
        rows={20}
        filters={filters}
        filterDisplay="menu"
        responsiveLayout="scroll"
        emptyMessage="No customdatasets found."
        header={header}
      >
        <Column header="Actions" frozen body={actionsTemplate} style={{ minWidth: '8rem' }} />
        <Column header="Code" sortable field="id" filter filterPlaceholder="Search by id" />
        <Column header="Date" sortable field="date" dataType="date" body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
        <Column header="Name" sortable field="name" filter filterPlaceholder="text"/>
        <Column header="Source" sortable field="source" filter filterPlaceholder="text"/>
        <Column header="User" sortable field="user_name" filter filterPlaceholder="text"/>
        <Column header="Email" sortable field="user_email" filter filterPlaceholder="text"/>
        <Column header="Status" sortable field="status" filter filterPlaceholder="status"/>
      </DataTable>
    </div>
  </div>
  )
};

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}
