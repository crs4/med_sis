"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { ProfileService } from '../../service/profiles';
import { TaxonomyService } from '../../service/taxonomies';
import { useUser } from '../../context/user';
import Loading from '../../components/Loading';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic"

import { FilterMatchMode, FilterOperator } from 'primereact/api';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog } from 'primereact/confirmdialog'; 
import { Toast } from 'primereact/toast'; 

import { point, featureCollection } from '@turf/turf';

const MyMap = dynamic(() => import("../../components/PointsMap"), { ssr:false })

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
  const [types, setTypes] = useState([]);
  const [cls_systems, setCls_systems] = useState([]);
  
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
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    const fetchData = async  () => {
      const _data = await ProfileService.list(document.cookie,'point-generals');
      if ( !_data || _data.error )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading soil data points' , life: 3000});
      else if ( !_data.data || !Array.isArray(_data.data) || _data.data.length === 0 ) 
        toast.current.show({severity:'warning', summary: 'No data!', detail: 'No Points Found' , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The soil data data list has been loaded' , life: 3000});
      }
      const _tdata = await TaxonomyService.listValues(document.cookie,'POINT_DATA_TYPES');
      if ( !_tdata || _tdata.error ) { 
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading soil data types' , life: 3000});
        setTypes([])
      }
      else {
        let _ts = [];
        _tdata.data.forEach( function (t) { _ts[t.id] = t  });
        setTypes(_ts)
      }   
      const _cls_sys = await TaxonomyService.listValues(document.cookie,'CLASSIFICATION_SYSTEMS');
      if ( !_cls_sys || _cls_sys.error ) { 
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading soil classifications systems info' , life: 3000});
        setCls_systems([])  
      }
      else { 
        let _cs = []
        _cls_sys.data.forEach( function (t) { _cs[t.id] = t });
        setCls_systems(_cs)  
      }  
      setProfiles(mapProfiles(_data.data));
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
        const pointsData = {
          layer : {
            points: pointsGeoJSON,
            styles: {
              'ok' : { radius: 8, fillColor: '#22f', color: '#00d', weight: 3, opacity: 1, fillOpacity: 0.7, },
            },
          },
          label: 'Legacy data locations',
        };
        setMapData(pointsData);
      }  
    }
    fetchMap();
  }, [pointsGeoJSON]);  

  const goTo = (id) => {
    router.push(`/points/${id}`);
  };

  const show = (data) => {
    setSelected(data);
    const element = document.getElementById('mymap')
    element?.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
  };

  const remove = async (id) => {
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
      const ok = await ProfileService.remove('point-generals',id);
      if ( ok  ) 
        toast.current.show({severity:'success', summary: 'Done!', detail:'Point soil data:'+id+'has been deleted', life: 3000});
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting point soil data', life: 3000});
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
  
  const mapProfiles = (data) => {
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
      type: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      date: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      location: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      lon_wgs84: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      lat_wgs84: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      elev_m_asl: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      survey_m: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      surveyors: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      project: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      cls_sys: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      old_cls: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      old_code: {
        operator: FilterOperator.AND,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      new_cls: {
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

  const typeBodyTemplate = (rowData) => {
    if (rowData.type)
      return <span >{types[rowData.type]?.descr}</span>;
    else return '';
  };

  const typeFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={Object.keys(types)} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={typeItemTemplate} placeholder="Select a soil point data type" className="p-column-filter" showClear />;
  };

  const typeItemTemplate = (option) => {
    return <span >{types[option]?.descr}</span>;
  };

  const cls_sysBodyTemplate = (rowData) => {
    if (rowData.cls_sys)
      return <span >{cls_systems[rowData.cls_sys]?.descr}</span>;
    else return '';
  };

  const cls_sysFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={Object.keys(cls_systems)} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={cls_sysItemTemplate} placeholder="Select a code" className="p-column-filter" showClear />;
  };

  const cls_sysItemTemplate = (option) => {
    return <span >{cls_systems[option]?.descr}</span>;
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
      onClick={() => remove(rowData.id) }
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
      onClick={() => goTo(rowData.id)}
      label=""
    />
    <Button
      icon="pi pi-map"
      className="p-mr-2 p-mb-2 m-1"
      loading={loading}
      disabled={isWorking}
      tooltip={t('SHOW_IN_MAP')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => show(rowData)}
      label=""
    />
    </> 
  );
//  
              
  
  return (
  <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            <Toast ref={toast} />  
    {(loading) && (
            <Loading  title="Loading points soil data" />
    )}
    {(!loading && !profiles) && (
            <div className="card">
                <h5 class="font-bold text-green-500">Points soil data not found</h5>
            </div>
    )} 
    {(profiles) && (
          <>
            <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlg} onHide={() => setVisibleDlg(false)} message="Are you sure you want to delete the point soil data?" 
              header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlg} />
            {(mapData) && ( 
              <div id="mymap" className="card">
                  
                <h5 class="font-bold text-green-500">{ mapData ? mapData.label : 'Points soil data locations' }</h5>
                <MyMap data={mapData} selected={selected} />
              </div>
            )}
            <h5>Points Soil Data Table</h5>
            <DataTable
                value={profiles}
                paginator
                dataKey="code"
                className="p-datatable-gridlines"
                globalFilterFields={['id','date','type','location','old_cls','cls_sys','new_cls','project']}
                showGridlines
                rows={20}
                filters={filters}
                filterDisplay="menu"
                loading={loading}
                responsiveLayout="scroll"
                emptyMessage="No points soil data found."
                header={header}
            >
              <Column header="Actions" frozen body={actionsTemplate} style={{ minWidth: '12rem' }} />
              <Column header="Code" sortable field="id" filter filterPlaceholder="Search by id" style={{ minWidth: '8rem' }} />
              <Column header="Type" sortable field="type" filter filterPlaceholder="Search by type" style={{ minWidth: '8rem' }} body={typeBodyTemplate} filterElement={typeFilterTemplate} />
              <Column header="Date" sortable field="date" dataType="date" style={{ minWidth: '8rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
              <Column header="Altitude(asl)" sortable field="elev_m_asl" dataType="numeric" style={{ minWidth: '5rem' }} />
              <Column header="Project" sortable field="project" filter filterPlaceholder="Search by project" style={{ minWidth: '8rem' }} />
              <Column header="Original Cls system" sortable field="cls_sys" filter filterPlaceholder="Search by original cls system" style={{ minWidth: '8rem' }} body={cls_sysBodyTemplate} filterElement={cls_sysFilterTemplate} />
              <Column header="Original code" sortable field="old_code" filter filterPlaceholder="Search by old code" style={{ minWidth: '10rem' }}  />
              <Column header="Original classification" sortable field="old_cls" filter filterPlaceholder="Search by old classification" style={{ minWidth: '8rem' }}  />
              <Column header="New classification" sortable field="new_cls" filter filterPlaceholder="Search by new classification" style={{ minWidth: '8rem' }}  />             
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

