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
import { point, featureCollection } from '@turf/turf';
import dynamic from "next/dynamic"

const MyMap = dynamic(() => import("../../components/LegacyMap"), { ssr:false })

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const toast = useRef(null);
  const [pointsGeoJSON, setPointsGeoJSON] = useState(null);
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState('');   
  const [isWorking, setIsWorking] = useState(false);
  const [current, setCurrent] = useState(null);
  const [profiles, setProfiles] = useState([]);
  const [visibleDlg, setVisibleDlg] = useState(false);
  const [loading, setLoading] = useState(true);
  const [mapData, setMapData] = useState(null); 
  const [selected, setSelected] = useState(null);
  const mapRef = useRef(null);
  
  const createGeoJSON = ( ) => {
    if (!profiles || pointsGeoJSON ) 
      return; 
    let points = [];
    for ( let j=1; j<profiles.length; j+=1 ){
  /// skip row with null or errors in lat,lon or key
      try {
        let obj = profiles[j]
        if ( obj && obj.id && obj.lat_wgs84 && obj.lon_wgs84 ) {
          let panel = '<div class="flex flex-wrap  justify-content-center">';
          panel += '<span class="text-cyan-500 align-items-center font-bold" >Identifier:</span><span> '+obj.id+'</span></div>';
          panel += '<div><span class="font-bold text-green-500"> Latitude: </span><span class="font-bold"> ' + obj.lat_wgs84  + '</span>';
          panel += '<span class="font-bold text-green-500"> Longitude: </span><span class="font-bold"> ' + obj.lon_wgs84  + '</span>';
          if (obj.elev_m_asl) {
            panel += '<span class="font-bold"> Altitude (ASL):  </span>'
            panel += '<span class="font-bold"> ' + obj.elev_m_asl  + '</span>';
          }
          panel +='</div>'
          points.push( point( [obj.lon_wgs84 , obj.lat_wgs84], 
                        { key: obj.id, popupContent : panel  },
                        { id: obj.id } ) );
        }
      } catch (e) {
        console.log(e);
      }
    }
    if ( points.length > 0 ) {
      setPointsGeoJSON( featureCollection(points) );
      toast.current.show({severity:'success', summary: 'GeoJSON created!', detail:'GeoJSON for elements created', life: 3000});
    }    
  }
         
  useEffect(() => {
    if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 )
        router.push(`/401`);
    const fetchData = async  () => {
      const data = null; //await ProfileService.listLegacy();
      if ( data ) {
        setProfiles(mapProfiles(data));
        toast.current.show({severity:'success', summary: 'Done!', detail:'Legacy data has been loaded', life: 3000});
      }
      else {
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors loading legacy data', life: 3000});
      }
      initFilters(); 
    }
    fetchData();
    setLoading(false);  
  },[user]);  // eslint-disable-line
  
  useEffect(() => {
      createGeoJSON ( );
  },[profiles]);  // eslint-disable-line

  useEffect(() => {
    const fetchMap = async () => {
      if ( pointsGeoJSON ) {
        const legacyData = {
          layer : {
            points: pointsGeoJSON,
            styles: {
              'ok' : { radius: 8, fillColor: '#22f', color: '#00d', weight: 3, opacity: 1, fillOpacity: 0.7, },
            },
          },
          label: 'Legacy data locations',
        };
        setMapData(legacyData);
      }  
    }
    fetchMap();
  }, [pointsGeoJSON]);  

  const goToProfile = (id) => {
    router.push(`/legacy/${id}`);
  };

  const showProfile = (data) => {
    setSelected(data);
    router.push(`/legacy#map`);
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
      const ok = null;//await ProfileService.remove('ProfileGeneral',id);
      if ( ok  ) 
        toast.current.show({severity:'success', summary: 'Done!', detail:'Profile:'+id+'has been deleted', life: 3000});
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting profile', life: 3000});
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
      survey_m: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      old_cls: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      cls_sys: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      new_cls: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      old_code: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      project: {
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

  const mapProfiles = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
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
      tooltip={t('INSPECT_PROFILE')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToProfile(rowData.id)}
      label=""
    />
    <Button
      icon="pi pi-map"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('SHOW_IN_MAP')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => showProfile(rowData)}
      label=""
    />
    </> 
  );

  
  return (
  <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            <Toast ref={toast} />  
    {(loading) && (
            <Loading  title="Loading Legacy data" />
    )}
    {(!loading && !profiles) && (
            <div className="card">
                <h5 class="font-bold text-green-500">Legacy data not found</h5>
            </div>
    )}
    {(profiles) && (
          <>
            <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlg} onHide={() => setVisibleDlg(false)} message="Are you sure you want to delete the profile?" 
              header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg} />
            {(mapData) && ( 
              <div className="card">
                <a name="map"/>   
                <h5 class="font-bold text-green-500">{ mapData ? mapData.label : 'Legacy data locations' }</h5>
                <MyMap selected={selected} data={mapData} />
              </div>
            )}
            <h5>Soil Profiles Table</h5>
            <DataTable
                value={profiles}
                paginator
                dataKey="code"
                className="p-datatable-gridlines"
                globalFilterFields={['id','date','surveyors','survey_m','old_cls','cls_sys','new_cls','project']}
                showGridlines
                rows={20}
                filters={filters}
                filterDisplay="menu"
                loading={loading}
                responsiveLayout="scroll"
                emptyMessage="No Legacy data found found."
                header={header}
            >
              <Column header="Actions" frozen body={actionsTemplate} style={{ minWidth: '12rem' }} />
              <Column header="Code" field="id"  sortable filter filterPlaceholder="Search by id" style={{ minWidth: '8rem' }} />
              <Column header="Date" sortable field="date" filterField="date" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
              <Column header="Surveyors" sortable field="surveyors" filter filterPlaceholder="Search by name" style={{ minWidth: '10rem' }} />
              <Column header="Survey method" sortable field="survey_m" filter filterPlaceholder="Search by code" style={{ minWidth: '8rem' }}  />
              <Column header="Old classification" sortable field="old_cls" filter filterPlaceholder="Search by code" style={{ minWidth: '8rem' }}  />
              <Column header="Classification system" sortable field="cls_sys" filter filterPlaceholder="Search by code" style={{ minWidth: '8rem' }}  />
              <Column header="New classification" sortable field="new_cls" filter filterPlaceholder="Search by code" style={{ minWidth: '8rem' }}  />
              <Column header="Project" sortable field="project" filter filterPlaceholder="Search by name" style={{ minWidth: '10rem' }}  />
              
            </DataTable>
          </>
    )}
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

