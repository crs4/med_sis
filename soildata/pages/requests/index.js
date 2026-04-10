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
  const [globalFilterValue, setGlobalFilterValue] = useState('');   
  const [isWorking, setIsWorking] = useState(false);
  const [visibleCreateDlg, setVisibleCreateDlg] = useState(false);
  const [visibleRemoveDlg, setVisibleRemoveDlg] = useState(false);
  const [visibleInfoDlg, setVisibleInfoDlg] = useState(false);
  const [loading, setLoading] = useState(true);
  const [request, setRequest] = useState(null); 
  const [requests, setRequests] = useState([]); 
  
  const initialRequestData = {
    name: 'New Dataset' + Date.now().toLocaleString(),
    user_name: user.username,
    user_email: user.email,
    date: Date.now(),
    src_name: null,
    src_typename: null, // geoserver typename
    src_count: 0,
    src_data: null,
    f_aoi: null,
    f_from: null,
    f_to: null,
    f_upper: null,
    f_lower: null,
    f_project: null,
    f_type: null,
    f_method: null,
    f_data: null,
    kriging: false,
    k_measure: false,
    k_validated: false,
    k_variogram: false,
    k_params: null,
    k_data: null,
    k_gn_raster: null,  // geonode id
    gn_result: null,
    status: ProfileService.REQUEST_STATUSES.CREATED  // geonode id
  }
  
  const removeRequest = async (id) => {
    if ( !id || request )
      return;
    const req = (requests.map( (e) => e.id === id ))
    if ( req[0] ) {
      setRequest(req[0]);
      setVisibleRemoveDlg(true);
    }
    else toast.current.show({severity:'error', summary: 'Error', detail:'Errors request data not found', life: 3000}); 
  };

  const createRequest = async () => {
    setRequest(initialRequestData);
    setVisibleRemoveDlg(true);
  };

  const cloneRequest = async (id) => {
    if ( !id || !requests )
      return;
    setIsWorking(true);
    try {
      const response = await ProfileService.get( document.cookie, id, 'requests' );
      if ( !response || !response.ok || !response.data )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading request' , life: 3000});
      else {
        let req = JSON.parse(JSON.stringify(response.data));
        if ( req ) {
          req.date = Date.now();
          req.name = 'New Dataset' + formatDate(Date.now());
          req.user_name = user.username;
          req.user_email = user.email; 
          req.kriging = false;
          req.k_validated = false;
          req.k_diagram = false;
          req.k_gn_raster = null;  // geonode id
          req.gn_result = null;  // geonode id
          setRequest(req);
          setVisibleCreateDlg(true);
        }
        setVisibleCreateDlg();
      }
    } catch (error) {
      toast.current.show({severity:'error', summary: 'Error', detail:'Errors reading data', life: 3000});
    }
    setIsWorking(false); 
  };

  const performCreate = async () => {
    setIsWorking(true);
    const response = await ProfileService.save( 'requests', document.cookie, request  );
    setIsWorking(false);
    if ( !response || !response.ok || !response.data )
    {
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors creating request' , life: 3000});
      return;
    }
    setRequest( response.data );
    const rs = requests;
    rs.push( response.data );
    setRequests( rs );
    setVisibleCreateDlg(false)
    initFilters();
  };

  const performRemove = async () => {
    if ( !request )
      return;
    try {
      const ok = await ProfileService.remove('requests', request.id);
      if ( ok ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'request data ' + request.id + ' has been deleted', life: 3000});
        setRequests(request.map( (e) => e.id !== request.id ));
      }
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting data', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    setIsWorking(false);
    setRequest(null);
    initFilters();   
  };

  const changeTypename = async (dataset)  => {
    if ( !request )
      return
    const r = request;
    if ( dataset ) {
      r.src_typename = dataset.typename;
      r.src_name = dataset.name;
    }
    if ( r.src_typename )  {
      try {
        r.src_count = 0,
        r.src_data = []
        setIsWorking(true)
        const response = await ProfileService.getDataset( r.src_typename, document.cookie )
        if ( !response || !response.ok || !response.data || !response.data.features )
        {
          r.src_count = response.data.features.length
          r.src_data = response.data
        }
        const response2 = await ProfileService.update( document.cookie, request.id, request, 'requests' )
        if ( !response2 || !response2.ok || !response2.data )
        {
          const rs = requests;
          rs.push(r)
          setRequests(rs)
        }
        toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Source data has been loaded.'});
      } catch (e) {
        console.log(e);
        toast.current.show({ severity: 'error', summary: 'Errors!', detail: 'Data not available.'});
      }
      setIsWorking(false)
    }
  }

  const changeName = (name) => {
    if ( !request || !name )
      return
    request.name = name;
    setRequest(request);
  }

  const resetRequestData = ()  => {
    if ( !request )
      return;
    request.src_count = 0;
    request.src_typename = null;
    request.src_name = null;
    request.src_data = [];  
  }
         
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    const fetchData = async  () => {
      setLoading(true);
      const response = await ProfileService.list(document.cookie,'requests');
      if ( !response || !response.ok )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading requests' , life: 3000});
      else if ( !response.data || !Array.isArray(response.data) || response.data.length === 0 ) 
        toast.current.show({severity:'warn', summary: 'No data!', detail: 'No Request Found' , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The new dataset requests list has been loaded' , life: 3000});
      } 
      setRequests(setDates(response.data));
      initFilters();
      setLoading(false); 
    }
    fetchData(); 
  },[user]);  // eslint-disable-line
  
  const goTo = (id) => {
    router.push(`/requests/${id}`);
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
  
  const rejectDlg = () => {
    setRequest(null);
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
      name: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      date: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      src_typename: {
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
      tooltip={t('INSPECT_REQUEST')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goTo(rowData.id)}
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
      onClick={() => cloneRequest(rowData)}
      aria-controls={visibleCreateDlg ? 'clone and open create request dialog' : null}
      aria-expanded={visibleCreateDlg ? true : false}
    />
    <Button icon="pi pi-times"
      className="p-button-danger mb-2 mr-2"
      label=""
      loading={isWorking}
      disabled={isWorking}
      tooltip={t('DELETE_PROFILE')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeRequest(rowData.id) }
      aria-controls={visibleRemoveDlg ? 'open dialog remove request' : null}
      aria-expanded={visibleRemoveDlg ? true : false}
    />
    </> 
  );
 
  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Request for New Datasets List</h5>
    <div className="card flex w-full" >      
    {(loading) && (
      <Loading  title="Loading Requests" />
    )}
    {(!loading && !requests) && (
      <h6 class="font-bold cyan-800">No Data Found</h6>
    )} 
    {(!loading && requests) && (
      <>
      <Dialog  header='Create a new request' visible={visibleCreateDlg} style={{ width: '50vw' }} onHide={() => { setRequest(null) }}> 
      { request &&  (
        <div className="card md:w-30rem flex flex-column gap-3 m-3 align-items-center">
          <Fieldset legend="Name">
            <div className="flex flex-column gap-2">
              <label htmlFor="name">Name</label>
              <InputText value={ request.name } onChange={ (e) => changeName(e.target.value) } id="name" aria-describedby="name-help" />
              <small id="name-help">
                Change the display name of the request.
              </small>
            </div>
          </Fieldset>
          <Fieldset legend="Source dataset">
          { request.src_count && request.src_data && ( 
            <div className="flex flex-column item-align-center gap-2">
              <Button icon="pi pi-trash" onClick={resetRequestData} severity="danger"/>
              <h5 className="font-bold text-green-600 m-2">
                <span className="font-bold text-gray-800">Source: </span> 
                {request.src_typename} 
              </h5>
              <h5 className="font-bold text-green-600 m-2">
                <span className="font-bold text-gray-800">Points: </span>
                {request.src_count}
              </h5>
            </div>
          )}
          { isWorking && (
            <Loading  title="Loading ..." />
          )}
          { !isWorking && !request.src_typename && (
            <div className="flex flex-column item-align-center gap-2">
              <div className=" xl:flex xl:justify-content-center">  
                <ListBox value={request.src_typename} onChange={(e) => changeTypename(e.value)} disabled={isWorking} 
                  options={datasets} optionLabel="name" className="w-full md:w-30rem" listStyle={{ maxHeight: '250px' }} />
              </div>
            </div>    
          )}
          </Fieldset>
          <div className="flex flex-row item-align-center m-3 gap-2">
            <Button icon="pi pi-save" label="Save" disabled={ !request || request.src_count } onClick={() => performCreate() } severity="success" raised />
            <Button icon="pi pi-" label="Save" disabled={ !request || request.src_count } onClick={() => setRequest(null) } severity="success" raised />
          </div>
        </div>
      )}
      </Dialog>
      <Dialog  header="Description of fields" visible={visibleInfoDlg} style={{ width: '50vw' }} 
        onHide={() => setVisibleInfoDlg(false)}>
        { selected && (  
        <div className="card grid text-cyan-800 w-full">
          <h5 className={className1}> name: </h5>
          <h5 className={className2}> {selected.data?.model} </h5>
          <h5 className={className1}> date: </h5>
          <h5 className={className2}> {selected.data?.name} </h5>
          <h5 className={className1}> xxxxx: </h5>
          <h5 className={className2}> {selected.data?.descr} </h5>
          <h5 className={className1}> xxxxx: </h5>
          <h5 className={className2}> {selected.data?.type} </h5>
        </div>
        )}
      </Dialog>
            
      <div className="card flex flex-reverse w-full m-3"> 
        <Button icon="pi pi-plus" className="mr-2 mb-2" label="New Request" loading={isWorking} disabled={isWorking}
          tooltip={t('CREATE_REQUEST')} tooltipOptions={{ position: 'top' }}
          onClick={() => createRequest()}
          aria-controls={visibleCreateDlg ? 'Create new request dialog' : null}
          aria-expanded={visibleCreateDlg ? true : false}
        />
        <Button icon="pi pi-question" className="mr-2 mb-2" label="Help"
          tooltip={t('HELP_ON_REQUEST')} tooltipOptions={{ position: 'top' }}
          onClick={() => setVisibleInfoDlg(true)}
          aria-controls={visibleInfoDlg ? 'Help on request fields' : null}
          aria-expanded={visibleInfoDlg ? true : false}
        />  
      </div>
    
      <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleRemoveDlg} onHide={() => setVisibleRemoveDlg(false)} 
          message="Are you sure you want to delete the Request? (Note: this don't remove datasets in the catalogue.)" 
          header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectRemove} />
      <DataTable value={requests} paginator dataKey="id" className="p-datatable-gridlines"
        globalFilterFields={['id','name','date','src_typename','username','useremail']}
        showGridlines
        rows={20}
        filters={filters}
        filterDisplay="menu"
        loading={isWorking}
        responsiveLayout="scroll"
        emptyMessage="No request data found."
        header={header}
      >
        <Column header="Actions" frozen body={actionsTemplate} style={{ minWidth: '8rem' }} />
        <Column header="Code" sortable field="id" filter filterPlaceholder="Search by id" />
        <Column header="Date" sortable field="date" dataType="date" body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
        <Column header="Name" sortable field="name" filter filterPlaceholder="text"/>
        <Column header="Source" sortable field="src_typename" filter filterPlaceholder="text"/>
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

