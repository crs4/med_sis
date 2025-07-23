"use client"

import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic"
import { Toast } from 'primereact/toast';
import { point, featureCollection } from '@turf/turf';
import { useUser } from '../../context/user';
import ReportTable from '../../components/XLSxResultTable';
import { UploadService } from '../../service/uploads';


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

  const createGeoJSON = ( ) => {
    if (!upload || !upload.data ) 
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
    let main = data['ProfileGeneral']
    if ( !main )
      main = data['SampleGeneral']
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
        console.log(_data.data)
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
      {(!upload && !loading ) && (
        <h2>No Upload found</h2>
      )}
      {(loading) && (
        <h2>Loading Upload Info...</h2>
      )}
      {(upload && !loading && ( upload.status === UploadService.STATUSES.IN_PROCESS || upload.status === UploadService.STATUSES.UPLOADED) ) && (
        <h2>The Upload is being processed</h2>
      )}
      
      {(upload && !loading  && upload.status !== UploadService.STATUSES.IN_PROCESS && upload.status !== UploadService.STATUSES.UPLOADED ) && (
        <div className="card">
          <span class="text-xl font-bold text-blue-600"> Upload:</span><span class="font-bold text-gray-600"> { upload.title } </span>
          <span class="text-xl font-bold text-blue-600"> Date:</span><span class="font-bold text-gray-600"> { upload.date }</span>
          <span class="text-xl font-bold text-blue-600"> Editor:</span><span class="font-bold text-gray-600"> { upload.editor }</span>
        </div>
      )} 
      {(map) && (    
        <div className="card">
          <h5 class="font-bold text-green-500">{ map ? map.label : 'Geo points in upload' }</h5>
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