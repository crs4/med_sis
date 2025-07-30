"use client"

import React, { useEffect, useState, useRef  } from 'react';
import { useTranslations } from 'next-intl';
import { ProfileService } from '../../service/profiles';
import { FilterMatchMode, FilterOperator } from 'primereact/api';
import { useUser } from '../../context/user';
import { useRouter } from 'next/router';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog } from 'primereact/confirmdialog'; 
import { Toast } from 'primereact/toast'; 
import Loading from '../../components/Loading';

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const toast = useRef(null);
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState('');   
  const [isWorking, setIsWorking] = useState(false);
  const [current, setCurrent] = useState(null);
  const [profiles, setProfiles] = useState([]);
  const [visibleDlg, setVisibleDlg] = useState(false);
  const [loading, setLoading] = useState(true);
  
         

  useEffect(() => {
      if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 )
          router.push(`/401`);
    },[user]);  // eslint-disable-line
  
  const goToProfile = (id) => {
    router.push(`/profiles/${id}`);
  };

  const removeProfile = async (id) => {
    if ( !id || current )
      return;
    setIsWorking(true);
    setCurrent(id);
    setVisibleDlg(true);
  };

  const performRemove = async () => {
    if ( !current )
      return;
    try {
      const res = await ProfileService.remove(id);
      if ( res && res.status == 200 ) {
        let data = await res.json();
        toast.current.show({severity:'success', summary: 'Done!', detail:'Profile:'+id+'has been deleted', life: 3000});
      }
      else {
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting profile', life: 3000});
      }
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setIsWorking(false);
    }
    setCurrent(null);
    initFilters();   
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
    setCurrent(null);
    setIsWorking(false);
  };
  
  useEffect(() => {
    const fetchData = async  () => {
      const res = await ProfileService.list();
      if ( res && res.status == 200 ) {
        let data = await res.json();
        setProfiles(mapProfiles(data));
        toast.current.show({severity:'success', summary: 'Done!', detail:'Profiles has been loaded', life: 3000});
      }
      else {
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors loading profiles', life: 3000});
      }
      setProfiles([])
      initFilters(); 
    }
    fetchData();
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
      code: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      surveyors: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      location: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      date: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      lat_wgs84: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      lon_wgs84: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      elev_m_asl: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      elev_dem: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      survey_m: {
          operator: FilterOperator.OR,
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

  const mapProfiles = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        d.survey_m = Mapping[d.survey_m]?.name;
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
      tooltip={t('DELETE_PROFILE')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeProfile(rowData.id) }
      aria-controls={visibleDlg ? 'dlg_remove' : null} 
      aria-expanded={visibleDlg ? true : false}
    />
    <Button
      icon="pi pi-folder-open"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('LOAD_PROFILE')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToProfile(rowData.id)}
      label=""
    />
    <Button
      icon="pi pi-map"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('SHOW_PROFILE')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToProfile(rowData.id)}
      label=""
    />
    </> 
  );

  if ( loading )
    return <Loading  title="Loading Soil Prodiles...." />
  else 
    return (
    <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlg} onHide={() => setVisibleDlg(false)} message="Are you sure you want to delete xlsx upload?" 
              header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg} />
            <Toast ref={toast} />
            <h5>Soil Profiles Table</h5>
            <DataTable
                value={profiles}
                paginator
                dataKey="code"
                className="p-datatable-gridlines"
                globalFilterFields={['code','surveyors','location','date lat_wgs84','lon_wgs84','gps','elev_m_asl','elev_dem','survey_m']}
                showGridlines
                rows={10}
                filters={filters}
                filterDisplay="menu"
                loading={loading}
                responsiveLayout="scroll"
                emptyMessage="No uploads found."
                header={header}
            >
              
              <Column header="Identifier" field="code"  filter filterPlaceholder="Search by id" style={{ minWidth: '10rem' }} />
              <Column header="Date"  filterField="date" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
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

