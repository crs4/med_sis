"use client"

import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic"
import { Toast } from 'primereact/toast';
import { Button } from 'primereact/button';
import { point, featureCollection } from '@turf/turf';
import { useUser } from '../../context/user';
import ReportTable from '../../components/XLSxResultTable';
import { UploadService } from '../../service/uploads';
import { TaxonomyService } from '../../service/taxonomies';


const MyMap = dynamic(() => import("../../components/XLSxMap"), { ssr:false })

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const id = router.query.id
  const user = useUser();
  const [loading, setLoading] = useState(true);
  const [upload, setUpload] = useState(null);
  const [pointsGeoJSON, setPointsGeoJSON] = useState(null);
  const [errors, setErrors] = useState([]);
  const [operations, setOperations] = useState([]);
  const toast = useRef(null);
  const [map, setMap] = useState(null); 

  const openList = () => {
    router.push(`/uploads`);
  };

  const openCreate = () => {
    router.push(`/uploads/create`);
  };

  const createGeoJSON = ( ) => {
    if (!upload || !upload.data || typeof upload.data !== "string" ) 
      return; 
    let points = [];
    const data = JSON.parse(upload.data);
    const errors = upload.report['errors'];
    if ( !data || (
         ( !data['ProfileGeneral'] || !Array.isArray(data['ProfileGeneral']) ) &&
         ( !data['SampleGeneral'] || !Array.isArray(data['SampleGeneral']) ) 
    ))
      return;
    let map_err = []
    if ( errors && Array.isArray(errors) )
      for ( let e=1; e<errors.length; e+=1 ){
        if ( errors[e] )
          map_err.push( errors[e]['element'] )
    }
    let main = data['ProfileGeneral']? data['ProfileGeneral'] : data['SampleGeneral']
    if ( main ) {
      for ( let j=1; j<main.length; j+=1 ){
  /// skip row with null or errors in lat,lon or key
        try {
          let status = 'ok';
          let obj = main[j]
          if ( obj && obj.id && obj.lat_wgs84 && obj.lon_wgs84 ) {
            if ( map_err.indexOf(obj.id) !== -1)
              status = 'ko'
            points.push( point( [obj.lon_wgs84 , obj.lat_wgs84], 
                        { key: obj.id, status: status, popupContent : obj.id  },
                        { id: obj.id } ) );
          }
        } catch (e) {
        
        }
      }
      if ( points.length > 0 ) {
        setPointsGeoJSON( featureCollection(points) );
        toast.current.show({severity:'success', summary: 'GeoJSON created!', detail:'GeoJSON for elements created', life: 3000});
      }
    }    
  }

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);router.push(`/401`);
    
  },[user]);  // eslint-disable-line

  useEffect(() => {
    createGeoJSON ( );
  },[upload]);  // eslint-disable-line

  useEffect(() => {
    const fetchData = ( async(id) => {
      let _data = await UploadService.get(document.cookie,id)
      if ( !_data && !_data.data )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading upload ' + id , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The upload ' + id + ' has been loaded' , life: 3000});
        setUpload(_data.data);
      }
      setLoading(false); 
    })
    if ( id )
      fetchData(id);
  }, [id]);
  
  useEffect(() => {
    const fetchMap = async () => {
      if ( pointsGeoJSON ) {
        const uploadMap = {
          layer : {
            points: pointsGeoJSON,
            styles: {
              'ok' : { radius: 8, fillColor: '#2f2', color: '#0d0', weight: 2, opacity: 1, fillOpacity: 0.8, },
              'ko' : { radius: 8, fillColor: '#f22', color: '#d22', weight: 2, opacity: 1, fillOpacity: 0.8, },
              'warn' : { radius: 8, fillColor: '#f80', color: '#d60', weight: 2, opacity: 1, fillOpacity: 0.8, },
            },
          },
          label: 'elements points',
        };
        setMap(uploadMap);
      }  
    }
    fetchMap();
  }, [pointsGeoJSON]);   

  let reportHeaders = ['Element', 'Section', 'Message'];
  
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <div className="flex flex-row-reverse p-mr-2 p-mb-2 m-1">
        <Button 
          icon="pi pi-list"
          className="flex bg-primary font-bold border-round"
          onClick={() => openList()}
          label={t('UPLOADS_LIST')}
        />
        <Button 
          icon="pi pi-download"
          className="flex bg-primary font-bold border-round mr-3"
          onClick={() => openCreate()}
          label={t('CREATE_UPLOAD')}
        />
      </div>
      {(!upload && !loading ) && (
        <h4>No Upload found</h4>
      )}
      {(loading) && (
        <h4>Loading Upload Info...</h4>
      )}
      {(upload && !loading && ( upload.status === UploadService.STATUSES.IN_PROCESS || upload.status === UploadService.STATUSES.UPLOADED) ) && (
        <h4>The Upload is being processed</h4>
      )}
      
      {(upload && !loading  && upload.status !== UploadService.STATUSES.IN_PROCESS && upload.status !== UploadService.STATUSES.UPLOADED ) && (
        <div className="card text-xl font-bold ">
          <span class="text-blue-600"> Upload:</span><span class="text-gray-600"> { upload.title } </span>
          <span class="text-blue-600"> Date:</span><span class="text-gray-600"> { upload.date.toString() }</span>
          <span class="text-blue-600"> Editor:</span><span class="text-gray-600"> { upload.editor }</span>
        </div>
      )} 
      {(map) && (    
        <div className="card">
          <h4 class="font-bold text-green-500">{ map ? map.label : 'Geo points in upload' }</h4>
          <MyMap data={map} />
        </div>

      )} 
      {(upload && upload.report && upload.report['errors'] && 
        Array.isArray(upload.report['errors']) && upload.report['errors'].length > 0 ) && ( 
          <ReportTable
            elements={upload.report['errors']}
            headers={reportHeaders}
            title={'Table of the ' + upload.report['errors'].length + ' errors in upload ' + upload.title }
            className='p-mt-4 p-mb-4' />         
      )}
      {(upload && upload.report && upload.report['operations'] && 
        Array.isArray(upload.report['operations']) && upload.report['operations'].length > 0 ) && ( 
          <ReportTable
            elements={upload.report['operations']}
            headers={reportHeaders}
            title={'Table of the ' + upload.report['operations'].length + ' operations in upload ' + upload.title  }
            className='p-mt-4 p-mb-4' />  
      )}
    </div>
  );
};
  
export async function getStaticPaths() {
  return {
    paths: [],
    fallback: 'blocking',
  }
}

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}