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
import { Dropdown } from 'primereact/dropdown';
import { RadioButton } from 'primereact/radiobutton';
 
export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const toast = useRef(null);
  /* Table of datasets filters  */
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState(''); 
  /* List of datasets */
  const [datasets, setDatasets] = useState([]);  
  /* Selected dataset */
  const [selected, setSelected] = useState(null);
  /* soilContext of the new dataset */ 
  // -ProfileService.DATASET_CONTEXT.SOIL_INDICATOR
  // -ProfileService.DATASET_CONTEXT.AOI_SOIL_INDICATOR
  // -ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA 
  const [soilContext, setSoilContext] = useState(null);
  
  const [visibleRemoveDlg, setVisibleRemoveDlg] = useState(false);
  const [visibleCloneDlg, setVisibleCloneDlg] = useState(false);
  const [visibleCreateDlg, setVisibleCreateDlg] = useState(false);
  const [isWorking, setIsWorking] = useState(false);
  
  const goToDataset = (id) => {
    router.push(`/publish/${id}`);
  };

  

  const formatDate = (value) => {
    const date = new Date(value).toJSON()
    if (date)
      return date.substring(0,10)
    else return ""
  };

  /* Initial configuration of new datasets */
  const initialDatasetConf = () => {
    const nowd = formatDate(Date.now())
    return {
      date : nowd,
      name : user.userData.preferred_username+':'+nowd,
      points : null, // source points soil data
      user_email : user.userData.email, 
      user_name : user.userData.preferred_username, 
      source : null, // source dataset title
      src_typename : null, // source dataset typename (catalogue layer name )
      filter : {
        aoi : null, // area of interest in geoJSON
        from : null , // period filter: from date
        to : null , // period filter: to date  
        depth: null, // depth filter: value  in [null,'0to20cm','20to50cm'] 
        project: null, // project name filter: string
        type: null, // point soil data type filter:  (taxonomy)
        method: null, // laboratory method filter:  (taxonomy)
        surMethod: null, // survey method filter:  (taxonomy)
        points: null // filtered points in geoJSON
      }, 
      kriging : false, // kriging interpolation toggle
      k_variogram : null, // variogram geoJSON object
      k_params : {},
      report : {},
      k_data : null, // aggregated points
      status : ProfileService.DATASET_STATUSES.CREATED,
      context : ProfileService.DATASET_CONTEXT.SOIL_INDICATOR
    }
  };
  
  /* This start creating a new dataset */
  const createDataset = async () => {
    if ( !isWorking ) {
      setSelected(null);
      setVisibleCreateDlg(true);
    }
  };

  /* This creates a new dataset */ 
  const performCreate = async () => {
    setVisibleCreateDlg(false);
    setIsWorking(true)
    try {
      const dataset = initialDatasetConf()
      dataset.context = soilContext
      const response = await ProfileService.save( document.cookie, dataset, 'datasets' );
      if ( response.ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'dataset ' + response.data.id + ' has been created', life: 3000});
        fetchData() 
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

  /* This start cloning dataset */
  const cloneDataset = async (id) => {
    if ( !id || isWorking )
      return;
    const req = datasets.filter( (e) => e.id === id )
    if ( req[0] ) {
      setSelected(id);
      setVisibleCloneDlg(true);
    }
    else toast.current.show({severity:'error', summary: 'Error', detail:'Errors dataset data not found', life: 3000}); 
  };

  /* This clones a dataset */
  const performClone = async () => {
    if ( !selected )
      return;
    setIsWorking(true);
    try {
      const response = await ProfileService.get( document.cookie, selected, 'datasets' );
      if ( response && response.ok && response.data ) {
        const nowd = formatDate(Date.now())
        // old field not modified:
        //   source, src_typename : the source dataset
        //   filter : point filters  
        //   kriging, k_params : kriging configuration
        //   context : the context of dataset 
        //            - Point soil data section
        //            - Soil indicator
        //            - Aoi soil indicator
        let dataset = {
          ...response.data, 
          date : nowd,
          name : user.userData.preferred_username+':'+nowd,
          user_name : user.userData.preferred_username,
          user_email : user.userData.email, 
          points : null, // original geo points not filtered, reload
          k_variogram : null, // semi-variogram data
          k_data : null, // aggregated geo filtered points
          report : null,  // final publication report with geonode ids
          status : ProfileService.DATASET_STATUSES.CREATED
        }
        
        const response = await ProfileService.save( document.cookie, dataset, 'datasets' );
        if ( response.ok ) {
          toast.current.show({severity:'success', summary: 'Done!', detail:'dataset ' + response.data.id + ' has been created', life: 3000});
          fetchData()
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

  /* This start deleting a dataset */ 
  const removeDataset = async (id) => {
    if ( !id )
      return;
    const req = datasets.filter( (e) => e.id === id )
    if ( req[0] ) {
      setSelected(id);
      setVisibleRemoveDlg(true);
    }
    else toast.current.show({severity:'error', summary: 'Error', detail:'Errors dataset data not found', life: 3000}); 
  };
  
  /* This delete a dataset  */
  const performRemove = async () => {
    if ( !selected )
      return;
    setIsWorking(true);
    try {
      const resp = await ProfileService.remove( document.cookie, selected, 'datasets');
      if ( resp.ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'dataset info ' + selected + ' has been deleted', life: 3000});
        setDatasets(datasets.filter( (e) => e.id !== selected  ));
      }
      else toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting data', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    setSelected(null);
    initFilters(); 
    setIsWorking(false);
  };

  const onGlobalFilterChange = (e) => {
    const value = e.target.value;
    let _filters = { ...filters };
    _filters['global'].value = value;
    setFilters(_filters);
    setGlobalFilterValue(value);
  };
  
  const header = () => {
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
  };
  
  const setDates = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        return d;
    });
  }; 
  
  const initFilters = () => { 
    setFilters({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      id: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      context: {
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
  
  const headerDlg = () => {
    return (
      <h5 className="w-7 surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2"> {t('CREATE_DATASET')}</h5>
    )
  }; 
  
  const actionsTemplate = (rowData) => (  
    <>
    <Button icon="pi pi-folder-open"
      className="mr-2 mb-2"
      label=""
      disabled={isWorking}
      tooltip={t('INSPECT_DATASET')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToDataset(rowData.id)}
      aria-controls={visibleCreateDlg ? 'Show the request data' : null}
      aria-expanded={visibleCreateDlg ? true : false}
    />
    <Button icon="pi pi-clone"
      className="mr-2 mb-2"
      label=""
      disabled={isWorking}
      tooltip={t('CLONE_DATASET')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => cloneDataset(rowData.id)}
    />
    <Button icon="pi pi-times"
      className="p-button-danger mb-2 mr-2"
      label=""
      disabled={isWorking}
      tooltip={t('DELETE_DATASET')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeDataset(rowData.id) }
      aria-controls={visibleRemoveDlg ? 'open dialog remove request' : null}
      aria-expanded={visibleRemoveDlg ? true : false}
    />
    </> 
  );
  
  const contextBodyTemplate = (rowData) => {
    if ( rowData.context === ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="Point Soil Data Section"></Tag>)
    else if ( rowData.context === ProfileService.DATASET_CONTEXT.SOIL_INDICATOR )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="Soil Indicator"></Tag>)
    else if ( rowData.context === ProfileService.DATASET_CONTEXT.AOI_SOIL_INDICATOR )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="Area Soil Indicator"></Tag>)
    else return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="No context error"></Tag>)
  };

  const contextFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={Object.keys(ProfileService.DATASET_CONTEXT)} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={contextItemTemplate} placeholder="Select a dataset context" className="p-column-filter" showClear />;
  };
  
  const contextItemTemplate = (option) => {
    return <Tag icon="pi pi-caret-right" severity="info" value= {( option == ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA ) ? "Point Soil Data section" : (( option == ProfileService.DATASET_CONTEXT.SOIL_INDICATOR ) ? "Soil indicator" : "Area Soil Indicator" ) }></Tag>;
  };
  
  const statusBodyTemplate = (rowData) => {
    if ( rowData.status === ProfileService.DATASET_STATUSES.CREATED )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="To configure"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.CONFIGURED )
      return ( <Tag icon="pi pi-caret-right" severity="info" value="To validate"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.VALIDATED || 
              rowData.status === ProfileService.DATASET_STATUSES.IN_PROCESS ) 
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Elaborating"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.PUBLISHED )
      return ( <Tag icon="pi pi-check" severity="success" value="Published"></Tag>)
    else if ( rowData.status === ProfileService.DATASET_STATUSES.ERRORS )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="Errors"></Tag>)
    else return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="No Status error"></Tag>)
  };
  
  const className1 = 'col-6 font-bold text-cyan-800 mt-1 mb-1';
  const className2 = 'col-6 text-green-800 mt-1 mb-1';
  
  const headerTemplate = () => {
    return  <h5 className="font-bold shadow-1 p-3 bg-cyan-700 text-white" style={{ width: '90%' }}>Choose the context of the new Dataset </h5>
  };
  
  const fetchData = async  () => {
    setIsWorking(true);
    const response = await ProfileService.list(document.cookie,`datasets`);
    if ( !response || !response.ok )
      toast.current.show({severity:'error', summary: t('ERRORS'), detail:t('ERRORS_READING_DATASET') , life: 3000});
    else if ( !response.data || !Array.isArray(response.data) || response.data.length === 0 ) 
      toast.current.show({severity:'warn', summary: t('EMPTY'), detail:t('NO_DATASETS_FOUND') , life: 3000});
    else {
      toast.current.show({severity:'success', summary: t('SUCCESS'), detail:t('DATASETS_LOADED') , life: 3000});
      setDatasets(setDates(response.data));
    }
    initFilters();
    setIsWorking(false); 
  }
    
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    fetchData(); 
  },[user]);  // eslint-disable-line

  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2"> {t('DATASETS_LIST')}</h5>
    <div className="card text-cyan-800" >      
    {(isWorking) && (
      <Loading  title={t('LOADING')} />
    )} 
      <div className="card flex flex-reverse w-full m-4"> 
        <Button icon="pi pi-plus" className="mr-2 mb-2" label="New Dataset" disabled={isWorking}
          tooltip={t('DATASETS_LIST')} tooltipOptions={{ position: 'top' }}
          onClick={() => goToList()}
        />
      </div>
      <Dialog header={headerTemplate} visible={visibleCreateDlg} style={{ width: '50vw' }} onHide={() => setVisibleCreateDlg(false)} >
        <div className="m-4 font-bold text-cyan-800">
          <h5>You must choose the context of the new dataset</h5>
          <div className="flex flex-column gap-3">
            <div>
              <RadioButton inputId="sections" name="context" value="sections" onChange={(e) => setSoilContext(ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA) } checked={ soilContext === ProfileService.DATASET_CONTEXT.POINTS_SOIL_DATA} />
              <label htmlFor="sections" className="ml-2">Point Soil Data Sections</label>
            </div>
            <div>
              <RadioButton inputId="indicators" name="context" value="indicators" onChange={(e) => setSoilContext(ProfileService.DATASET_CONTEXT.SOIL_INDICATOR) } checked={ soilContext === ProfileService.DATASET_CONTEXT.SOIL_INDICATOR} />
              <label htmlFor="indicators" className="ml-2">Soil Indicators</label>
            </div>
            <div>
              <RadioButton inputId="indicators" name="context" value="indicators" onChange={(e) => setSoilContext(ProfileService.DATASET_CONTEXT.AOI_SOIL_INDICATOR) } checked={ soilContext === ProfileService.DATASET_CONTEXT.AOI_SOIL_INDICATOR} />
              <label htmlFor="indicators" className="ml-2">Soil indicators evaluated in an area</label>
            </div>
          </div>
          <div class="flex flex-row justify-content-center w-full m-3">
            <Button
              label={t('CANCEL')}
              icon='pi pi-trash'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { setVisibleCreateDlg(false) }}
            />
            <Button
              label={t('CREATE_DATASET')}
              icon='pi pi-wrench'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { performCreate() }}
            /> 
          </div>
        </div>    
      </Dialog>

      <ConfirmDialog id="dlg_create" group="declarative"  visible={visibleCloneDlg} onHide={() => setVisibleCloneDlg(false)} 
          message="Are you sure you want to create the cloned dataset?" 
          header="Confirmation" icon="pi pi-plus" accept={performClone} reject={rejectDlg} />
      <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleRemoveDlg} onHide={() => setVisibleRemoveDlg(false)} 
          message="Are you sure you want to delete the Dataset? (Note: this doesn't remove the dataset in the catalogue.)" 
          header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg} />
      
      <DataTable value={datasets} paginator dataKey="id" className="p-datatable-gridlines"
        globalFilterFields={['id','name','date','context','source','username','useremail','status']}
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
        <Column header="Name" sortable field="name" filter filterPlaceholder="text"/>
        <Column header="Date" sortable field="date" dataType="date" body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
        <Column header="Context" sortable field="context" body={contextBodyTemplate} filter filterElement={contextFilterTemplate}/>
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
