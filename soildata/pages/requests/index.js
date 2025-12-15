import { RequestService } from '../../service/requests';


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
  const [requests, setRequests] = useState(null);
  const router = useRouter();
  const toast = useRef(null);
  const user = useUser();
  const statuses = Object.keys(RequestService.STATUSES) 
  
  useEffect(() => {
      if ( user.userData && user.userData.forbidden2 !== null && user.userData.forbidden2 )
          router.push(`/401`);
    },[user]);  // eslint-disable-line

  const goToRequest = (id) => {
    router.push(`/requests/${id}`);
  };

  const removeRequest = async (id) => {
    if ( !id || current )
      return;
    setIsWorking(true);
    setCurrent(id);
    setVisibleDlg1(true);
  };

  const performRemove = async () => {
    if ( !current )
      return;
    setRequests( requests.filter((el) => el.id !== current) );
    initFilters();
    /*
    try {
      current.cancel = true;
      const res = await RequestService.update(current,{'cancel': true} );
    //// !!!!!!!!only set cancel = True
      const json = await res.json();
      if (json.errors) {
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors cancelling request', life: 3000});
      }
      else  {
        setRequests( requests.filter((el) => el.id !== current) );
        toast.current.show({severity:'success', summary: 'Done!', detail:'Request has been cancelled', life: 3000});
      } 
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'System Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setCurrent(null);
      setIsWorking(false);
    }*/
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
  
  useEffect(() => {
    const fetchData = ( () => {
/*'Data type: Profiles/Samples/Indicator')
    id: 1
    user: 1004
    username: 'Roberto Demontis'
    useremail: 'demontis@crs4.it'
    creation: new Date('2025/05/19'),
    mgr: 1010
    mgrname: manager1
    mgremail: manager@mysis.org
    mgrmsg: "Data non available for the selected Aoi"
    type: "Profiles"
    dataid: "text_cls"
    purpose: "Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm "
    aoi: .......
    datefrom:  new Date('1968/01/01'),
    dateto: null,
    depth: 10
    cancelled: false
    status: executed
    geonode: pippo
*/    

      const _data = [ 
        { 
          id: 1,
          user: 1004,
          username: 'Roberto Demontis',
          useremail: 'demontis@crs4.it',
          creation: new Date('2025/05/19'),
          mgr: 1010,
          mgrname: manager1,
          mgremail:'manager@mysis.org',
          mgrmsg: 'Data non available for the selected Aoi',
          type: 'Profiles',
          dataid: 'text_cls',
          purpose: 'Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm',
          aoi: null,
          anchor: null,
          datefrom:  new Date('1968/01/01'),
          dateto: null,
          depth: 10,
          cancelled: false,
          geonode: pippo,
          status: RequestService.STATUSES.ELABORATED,
        },
        { 
          id: 1,
          user: 1004,
          username: 'Roberto Demontis',
          useremail: 'demontis@crs4.it',
          creation: new Date('2025/05/19'),
          mgr: 1010,
          mgrname: manager1,
          mgremail:'manager@mysis.org',
          mgrmsg: 'Data non available for the selected Aoi',
          type: 'Profiles',
          dataid: 'text_cls',
          purpose: 'Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm',
          aoi: null,
          anchor: null,
          datefrom:  new Date('1968/01/01'),
          dateto: null,
          depth: 10,
          cancelled: false,
          geonode: pippo,
          status: RequestService.STATUSES.ASSIGNED,
        },
        { 
          id: 1,
          user: 1004,
          username: 'Roberto Demontis',
          useremail: 'demontis@crs4.it',
          creation: new Date('2025/05/19'),
          mgr: 1010,
          mgrname: manager1,
          mgremail:'manager@mysis.org',
          mgrmsg: 'Data non available for the selected Aoi',
          type: 'Profiles',
          dataid: 'text_cls',
          purpose: 'Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm',
          aoi: null,
          anchor: null,
          datefrom:  new Date('1968/01/01'),
          dateto: null,
          depth: 10,
          cancelled: false,
          geonode: pippo,
          status: RequestService.STATUSES.ERRORS,
        }, 
        { 
          id: 1,
          user: 1004,
          username: 'Roberto Demontis',
          useremail: 'demontis@crs4.it',
          creation: new Date('2025/05/19'),
          mgr: 1010,
          mgrname: manager1,
          mgremail:'manager@mysis.org',
          mgrmsg: 'Data non available for the selected Aoi',
          type: 'Profiles',
          dataid: 'text_cls',
          purpose: 'Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm',
          aoi: null,
          anchor: null,
          datefrom:  new Date('1968/01/01'),
          dateto: null,
          depth: 10,
          cancelled: false,
          geonode: pippo,
          status: RequestService.STATUSES.IN_PROCESS,
        }, 
        { 
          id: 1,
          user: 1004,
          username: 'Roberto Demontis',
          useremail: 'demontis@crs4.it',
          creation: new Date('2025/05/19'),
          mgr: 1010,
          mgrname: manager1,
          mgremail:'manager@mysis.org',
          mgrmsg: 'Data non available for the selected Aoi',
          type: 'Profiles',
          dataid: 'text_cls',
          purpose: 'Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm',
          aoi: null,
          anchor: null,
          datefrom:  new Date('1968/01/01'),
          dateto: null,
          depth: 10,
          cancelled: false,
          geonode: pippo,
          status: RequestService.STATUSES.ELABORATED,
        },
        { 
          id: 1,
          user: 1004,
          username: 'Roberto Demontis',
          useremail: 'demontis@crs4.it',
          creation: new Date('2025/05/19'),
          mgr: 1010,
          mgrname: manager1,
          mgremail:'manager@mysis.org',
          mgrmsg: 'Data non available for the selected Aoi',
          type: 'Profiles',
          dataid: 'text_cls',
          purpose: 'Hi SIS. I would like the texture class of profiles acquired in period from 1968 to now  for area y at depth 10 cm',
          aoi: null,
          anchor: null,
          datefrom:  new Date('1968/01/01'),
          dateto: null,
          depth: 10,
          cancelled: false,
          geonode: pippo,
          status: RequestService.STATUSES.CREATED,
        }
      ]
      /*const _users = _data.map ((upload) => {
        return upload.user;
      });*/
      setRequests(mapRequests(_data));
      initFilters(); 
    })
    fetchData();
    //RequestService.list().then((data) => setRequests(mapUploadsDate(data)));
    setLoading(false);
  }, []); // eslint-disable-line

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
      useremail: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      creation: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      type: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      mgrname: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      type: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
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
  
  const statusBodyTemplate = (rowData) => {
    if ( rowData.status ==="Elaborated" )
      return ( <Tag icon="pi pi-check" severity="success" value="Elaborated"></Tag>)
    else if ( rowData.status === "Rejected" )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="Rejected"></Tag>)
    else if ( rowData.status === "Elaborating" )
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Elaborating"></Tag>)
    else 
      return ( <Tag icon="pi pi-cog" severity="info" value="Created"></Tag>)
  };

  const statusFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={statuses} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={statusItemTemplate} placeholder="Select a Status" className="p-column-filter" showClear />;
  };

  const statusItemTemplate = (option) => {
    if ( option === "Elaborated" )
      return ( <Tag severity="success" value="Elaborated"></Tag>)
    else if ( option === "Elaborating" )
      return ( <Tag severity="warning" value="Elaborating"></Tag>)
    else if ( option === "Created" )
      return ( <Tag severity="info" value="Created"></Tag>)
    else if ( option === "Rejected" )
      return ( <Tag severity="danger" value="Rejected"></Tag>)
  };

  const header = renderHeader();

  const mapRequests = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        /*if ( d.status === IndicatorService.STATUS.CRITICAL_ERROR )
          d.status = "Critical Error"
        else if ( d.status === IndicatorService.STATUS.CREATED )
          d.status ="Created";
        else if ( d.status === IndicatorService.STATUS.INITIALIZED )
          d.status ="Initialized";
        else  
          d.status ="Critical error";*/
        //d.type = IndicatorService.TYPES[d.type]?.label;
        return d;
    });
  };

  const actionsTemplate = (rowData) => (
    
    <>
    <Button
      icon="pi pi-times"
      className="p-button-danger p-mb-2 p-mr-2 m-1"
      label=""
      loading={loading}
      disabled={isWorking}
      tooltip={t('CANCEL_REQUEST')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeRequest(rowData.id) }
      aria-controls={visibleDlg1 ? 'dlg_remove' : null} 
      aria-expanded={visibleDlg1 ? true : false}
    />
    <Button
      icon="pi pi-folder-open"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('LOAD_REQUEST')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToRequest(rowData.id)}
      label=""
    />
    </> 
  );

  return (
    <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlg1} onHide={() => setVisibleDlg1(false)} message="Are you sure you want to cancel request?" 
              header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg1} />
            <Toast ref={toast} />
            <h5>Requests</h5>
            <DataTable
                value={requests}
                paginator
                dataKey="id"
                className="p-datatable-gridlines"
                globalFilterFields={['id', 'name', 'user', 'data_keys', 'data_type', 'status']}
                showGridlines
                rows={15}
                filters={filters}
                filterDisplay="menu"
                loading={loading}
                responsiveLayout="scroll"
                emptyMessage="No requests found."
                header={header}
            >
              <Column header="Identifier" field="id"  filter filterPlaceholder="Search by id" style={{ minWidth: '10rem' }} />
              <Column header="Name" field="name"  filter filterPlaceholder="Search by name" style={{ minWidth: '14rem' }} />
              <Column header="User" field="user"  filter filterPlaceholder="Search by user" style={{ minWidth: '14rem' }} />
              <Column header="Date"  filterField="date" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
              <Column header="Type"  field="data_type" filter filterPlaceholder="Search by Type" style={{ minWidth: '10rem' }} />
              <Column header="Keys"  field="data_keys" filter filterPlaceholder="Search by Keys" style={{ minWidth: '10rem' }} />
              <Column header="From"  filterField="data_from" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
              <Column header="To"  filterField="data_to" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
              <Column header="Status"  field="status" filterMenuStyle={{ width: '12rem' }} style={{ minWidth: '14rem' }} body={statusBodyTemplate} filter filterElement={statusFilterTemplate} />
              <Column header="Actions" body={actionsTemplate} />
            </DataTable>
          </div>
        </div>
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

