"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';

import { ProfileService } from '../../service/profiles';
import { useUser } from '../../context/user';
import Loading from '../../components/Loading';

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

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const toast = useRef(null);
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState(''); 
  const [visibleRemoveDlg, setVisibleRemoveDlg] = useState(false);
  const [visibleCreateDlg, setVisibleCreateDlg] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isWorking, setIsWorking] = useState(false);
  const [dataset, setDataset] = useState(null);
  const [selected, setSelected] = useState(null);
  const [selectedSource, setSelectedSource] = useState(null);
   
  const [datasets, setDatasets] = useState([]); 
  
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

  const goToDataset = (id) => {
    router.push(`/dataset/${id}`);
  };

  const newDataset = () => {
    if ( !isWorking || loading ) {
      setSelected(null);
      const d = {
        date : Date.now(),
        name : 'user'+user.id+'-'+formatDate(new Date(Date.now())),
        user : user.id,
        points : null,
        user_email : user.email, 
        k_variogram : null,
        k_gn_raster : null,  // geonode id
        catalogue_id : null,  // geonode id
        source : null,
        src_typename : null,
        typename : null,
        filter : null,
        kriging : false,
        k_params : null,
        k_data : null,
        status : ProfileService.DATASET_STATUSES.CREATED
      }
      setDataset(d);
      setVisibleCreateDlg(true);  
    }
  };

  const cloneDataset = async (id) => {
    if ( !id )
      return;
    setIsWorking(true);
    try {
      setSelected(id)
      const response = await ProfileService.get( document.cookie, id, 'datasets' );
      if ( response && response.ok && response.data ) {
        let d = {
          ...response.data, 
          date : Date.now(),
          name : 'user'+user.id+'-'+formatDate(new Date(Date.now())),
          user : user.id,
          points : null,
          user_email : user.email, 
          k_variogram : null,
          k_gn_raster : null,  // geonode id
          catalogue_id : null,  // geonode id
          typename : null,
          k_data : null,
          status : ProfileService.DATASET_STATUSES.CREATED
        }
        setSelectedSource(d.source)
        setDataset(d);
        setVisibleCreateDlg(true);
      }  
      else toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading cloned dataset info' , life: 3000});
      
    } catch (error) {
      toast.current.show({severity:'error', summary: 'Error', detail:'Errors reading cloned dataset info', life: 3000});
    }
  };

  const performRemove = async () => {
    if ( !selected )
      return;
    try {
      const resp = await ProfileService.remove( document.cookie, selected, 'datasets');
      if ( resp.ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'dataset info ' + dataset.id + ' has been deleted', life: 3000});
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

  const performCreate = async () => {
    if ( !dataset )
      return;
    try {
      const response = await ProfileService.save( document.cookie, dataset, 'dataset' );
      if ( response.ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'dataset data ' + dataset.id + ' has been deleted', life: 3000});
        setIsWorking(false);
        setSelected(null);
        setDataset(null);
        fetchData()  
      }
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting data', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }   
  };
   
  const fetchData = async  () => {
    setLoading(true);
    const response = await ProfileService.list(document.cookie,'dataset');
    if ( !response || !response.ok )
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading datasets' , life: 3000});
    else if ( !response.data || !Array.isArray(response.data) || response.data.length === 0 ) 
      toast.current.show({severity:'warn', summary: 'No data!', detail: 'No Soil datasets Found' , life: 3000});
    else { 
      toast.current.show({severity:'success', summary: 'Success!', detail: 'The Soil datasets list has been loaded' , life: 3000});
    } 
    setDatasets(setDates(response.data));
    initFilters();
    setLoading(false); 
  }
    
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
  
  const rejectDlg = () => {
    setSelected(null);
    setDataset(null);
  };
  
  const setDates = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        return d;
    });
  };

  const formatDate = (value) => {
    return value.toLocaleDateString('en-US', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
    });
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
      }  
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
      tooltip={t('CLONE_REQUEST')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => cloneDataset(rowData)}
      aria-controls={visibleCreateDlg ? 'clone dataset' : null}
      aria-expanded={visibleCreateDlg ? true : false}
    />
    <Button icon="pi pi-times"
      className="p-button-danger mb-2 mr-2"
      label=""
      loading={isWorking}
      disabled={isWorking}
      tooltip={t('DELETE_PROFILE')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeDataset(rowData.id) }
      aria-controls={visibleRemoveDlg ? 'open dialog remove request' : null}
      aria-expanded={visibleRemoveDlg ? true : false}
    />
    </> 
  );
 
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    fetchData(); 
  },[user]);  // eslint-disable-line
  
  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2"> Custom Datasets List</h5>
    <div className="card flex w-full" >      
    {(loading) && (
      <Loading  title="Loading Requests" />
    )}
    {(!loading && !datasets) && (
      <h6 class="font-bold cyan-800">No Datasets Found</h6>
    )} 
    {(!loading && datasets) && (
      <>
      <div className="card flex flex-reverse w-full m-3"> 
        <Button icon="pi pi-plus" className="mr-2 mb-2" label="New Dataset" disabled={isWorking}
          tooltip={t('CREATE_DATASET')} tooltipOptions={{ position: 'top' }}
          onClick={() => newDataset()}
        />
      </div>
      <Dialog header="Create new dataset" visible={visibleCreateDlg} style={{ width: '50vw' }} 
        onHide={() => { rejectDlg();setVisibleCreateDlg(false);}}>
        { dataset && (  
          <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
            <div className="grid " >
              <div className={className1}> name: </div><div className={className2}> {dataset.name} </div>
              <div className={className1}> date: </div><div className={className2}> {formatDate(dataset.date)} </div>
              <div className={className1}> user: </div><div className={className2}> {dataset.user} </div>
              <div className={className1}> email: </div><div className={className2}> {dataset.user_email} </div>
            </div>
            <Fieldset legend="Select Points Source">
              { dataset.source && (
                <ListBox value={selectedSource} onChange={(e) => setSelectedSource(e.value)} options={datasetsSources} 
                  optionLabel="name" optionGroupChildren="items" className="w-full md:w-20rem" listStyle={{ maxHeight: '250px' }} />
              )}
            </Fieldset>
            <div class="flex flex-row mt-4 mb-4">
              <Button
                label={t('RESET')}
                icon='pi pi-trash'
                type='button'
                disabled={ isWorking }
                className='mt-4 flex mr-4'
                onClick={() => { resetData(); }}
              />
              <Button
                label={t('CREATE_DATASET')}
                icon='pi pi-save'
                type='button'
                loading={uploading}
                disabled={ isWorking || !selectedSource }
                className='mt-4 flex'
                onClick={() => { setIsWorking(true); performCreate(); }} 
              /> 
            </div>
          </div>
        )}
      </Dialog>    
      <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleRemoveDlg} onHide={() => setVisibleRemoveDlg(false)} 
          message="Are you sure you want to delete the Request? (Note: this don't remove datasets in the catalogue.)" 
          header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg} />
      
      <DataTable value={datasets} paginator dataKey="id" className="p-datatable-gridlines"
        globalFilterFields={['id','name','date','source','username','useremail']}
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
        <Column header="User" sortable field="username" filter filterPlaceholder="user name"/>
        <Column header="Email" sortable field="useremail" filter filterPlaceholder="user email"/>
      </DataTable>
      </>
    )}
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
