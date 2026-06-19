"use client"

import React, { useEffect, useState, useRef  } from 'react';

import { ProfileService } from '../../service/profiles';
import BaseDatasets from '../../data/basedatasets';
import { useUser } from '../../context/user';
import Loading from '../../components/Loading';

import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';

import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { Card } from 'primereact/card'; 
import { Toast } from 'primereact/toast';   

//// only admin
// execute updateLayers
// execute setMetadata
// execute setKeywords

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
  const [points, setPoints] = useState([]);
  const [visibleDlg, setVisibleDlg] = useState(false);
  const [loading, setLoading] = useState(true);
  const [mapData, setMapData] = useState(null);
  const [selected, setSelected] = useState(null); 
  const [types, setTypes] = useState([]);
  const [cls_systems, setCls_systems] = useState([]);
  
  const srcDatasetsList = BaseDatasets.indicators

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
        router.push(`/401`);
    const fetchData = async  () => {
      const _data = await ProfileService.list(document.cookie,'point-generals');
      if ( !_data || !_data.ok )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading soil data points' , life: 3000});
      else if ( !_data.data || !Array.isArray(_data.data) || _data.data.length === 0 ) 
        toast.current.show({severity:'warn', summary: 'No data!', detail: 'No Points Found' , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The soil data data list has been loaded' , life: 3000});
      }
      const _tdata = await TaxonomyService.listValues(document.cookie,'POINT_DATA_TYPES');
      if ( !_tdata || !_tdata.ok ) { 
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading taxonomies' , life: 3000});
        setTypes([])
      }
      else {
        let _ts = [];
        _tdata.data.forEach( function (t) { _ts[t.id] = t  });
        setTypes(_ts)
      }   
      const _cls_sys = await TaxonomyService.listValues(document.cookie,'CLASSIFICATION_SYSTEMS');
      if ( !_cls_sys || !_cls_sys.ok ) { 
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading soil classifications systems info' , life: 3000});
        setCls_systems([])  
      }
      else { 
        let _cs = []
        _cls_sys.data.forEach( function (t) { _cs[t.id] = t });
        setCls_systems(_cs)  
      }  
      setPoints(setDate(_data.data));
      initFilters();
    }
    fetchData();
    setLoading(false);  
  },[user]);  // eslint-disable-line
  
  
    
              
  
  return (
  <div className="layout-dashboard">
    <Toast ref={toast} />
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Points Soil Data List</h5>
    <Card className="flex w-full" >      
    {(loading) && (
      <Loading  title="Loading points" />
    )}
      
    </Card>
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

