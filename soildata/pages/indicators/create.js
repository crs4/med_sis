import { IndicatorService } from '../../service/indicators';


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
  const [visibleDlg2, setVisibleDlg2] = useState(false);
  const [loading, setLoading] = useState(true);
  const [indicators, setIndicators] = useState(null);
  const router = useRouter();
  const toast = useRef(null);
  const user = useUser();
  const statuses = [ "Created", "Initialized", "Critical error" ];
  

  useEffect(() => {
      if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 )
          router.push(`/401`);
  },[user]);  // eslint-disable-line
  
  const goToUpload = (id) => {
    router.push(`/indicators/${id}`);
  };

  const removeUpload = async (id) => {
    if ( !id || current )
      return;
    setIsWorking(true);
    setCurrent(id);
    setVisibleDlg1(true);
  };

  const performRemove = async () => {
    if ( !current )
      return;
    setIndicators( indicators.filter((el) => el.id !== current) );
    initFilters();
    /*
    try {
      const res = await UploadService.remove(id);
      const json = await res.json();
      if (json.errors) {
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting upload', life: 3000});
      }
      else  {
        setUploads((omp) => (omp.filter((p) => p.id !== id)));
        toast.current.show({severity:'success', summary: 'Done!', detail:'Upload has been deleted', life: 3000});
      } 
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setIsDeleting(null);
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

  const rejectDlg2 = () => {
    setCurrent(null);
    setIsWorking(false);
  };
  
  useEffect(() => {
    const fetchData = ( () => {
      const _data = [ 
        { 
          id: 1,
          name: 'Indicatorstest1',
          user: 'admin', 
          date: new Date('2025/05/10'),
          type: 'SIMPLE',
          status: IndicatorService.STATUS.CREATED
        },
        { id: 2,
          name: 'Indicatorstest2',
          user: 'datamanager', 
          date: new Date('2025/05/10'),
          type: 'SIMPLE',
          status: IndicatorService.STATUS.INITIALIZED
        },
        { id: 3,
          name: 'Indicatorstest3',
          user: 'datamanager', 
          date: new Date('2025/05/12'),
          type: 'SIMPLE',
          status: IndicatorService.STATUS.CRITICAL_ERROR
        }, 
      ]
      /*const _users = _data.map ((upload) => {
        return upload.user;
      });*/
      setIndicators(mapIndicators(_data));
      initFilters(); 
    })
    fetchData();
    //UploadService.getUploads().then((data) => setUploads(mapUploadsDate(data)));
    setLoading(false);
  }, []);

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
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      user: {
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

  const statusBodyTemplate = (rowData) => {
    if ( rowData.status ==="All saved" )
      return ( <Tag icon="pi pi-check" severity="success" value="All saved"></Tag>)
    else if ( rowData.status === "Some Errors" )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="warning" value="Some Errors"></Tag>)
    else if ( rowData.status === "Elaborating" )
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Elaborating"></Tag>)
    else 
      return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="Critical error"></Tag>)
  };

  const statusFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={statuses} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={statusItemTemplate} placeholder="Select a Status" className="p-column-filter" showClear />;
  };

  const statusItemTemplate = (option) => {
    if ( option === IndicatorService.STATUS.SUCCESFULLY_IMPORTED )
      return ( <Tag severity="success" value="All saved"></Tag>)
    else if ( option === IndicatorService.STATUS.IMPORTED_WITH_ERROR )
      return ( <Tag severity="warning" value="Some Errors"></Tag>)
    else if ( option === IndicatorService.STATUS.UPLOADED )
      return ( <Tag severity="info" value="Elaborating"></Tag>)
    else if ( option === IndicatorService.STATUS.CRITICAL_ERROR )
      return ( <Tag severity="danger" value="Critical error"></Tag>)
  };

  

  const header = renderHeader();

  const mapIndicators = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        if ( d.status === IndicatorService.STATUS.CRITICAL_ERROR )
          d.status = "Critical Error"
        else if ( d.status === IndicatorService.STATUS.CREATED )
          d.status ="Created";
        else if ( d.status === IndicatorService.STATUS.INITIALIZED )
          d.status ="Initialized";
        else  
          d.status ="Critical error";
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
      tooltip={t('DELETE_INDICATOR')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeUpload(rowData.id) }
      aria-controls={visibleDlg1 ? 'dlg_remove' : null} 
      aria-expanded={visibleDlg1 ? true : false}
    />
    <Button
      icon="pi pi-folder-open"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('LOAD_INDICATOR')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToUpload(rowData.id)}
      label=""
    />
    </> 
  );

  return (
    <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlg1} onHide={() => setVisibleDlg1(false)} message="Are you sure you want to delete xlsx upload?" 
              header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg1} />
            <Toast ref={toast} />
            <h5>XLSx Uploads Table</h5>
            <DataTable
                value={indicators}
                paginator
                dataKey="id"
                className="p-datatable-gridlines"
                globalFilterFields={['id', 'name', 'user', 'status']}
                showGridlines
                rows={10}
                filters={filters}
                filterDisplay="menu"
                loading={loading}
                responsiveLayout="scroll"
                emptyMessage="No uploads found."
                header={header}
            >
              <Column header="Identifier" field="id"  filter filterPlaceholder="Search by id" style={{ minWidth: '10rem' }} />
              <Column header="Name" field="name"  filter filterPlaceholder="Search by name" style={{ minWidth: '14rem' }} />
              <Column header="User" field="user"  filter filterPlaceholder="Search by user" style={{ minWidth: '14rem' }} />
              <Column header="Date"  filterField="date" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
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

