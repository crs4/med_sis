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
  const toast = useRef(null); 

  const openList = () => {
    router.push(`/uploads`);
  };

  const openCreate = () => {
    router.push(`/uploads/create`);
  };

  useEffect(() => {
    const fetchData = ( async(id) => {
      if ( !id )
        return;
      let response = await UploadService.get(document.cookie,id)
      if ( !response && !response.data )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading upload ' + id , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The upload ' + id + ' has been loaded' , life: 3000});
        setUpload(response.data);
      }
      setLoading(false); 
    })
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    fetchData(id);
  },[user]);  // eslint-disable-line   

  let reportHeaders = ['Element', 'Section', 'Message'];
  
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('UPLOADS_LIST')}</h4>
      <div className="card text-cyan-800 shadow-2">
        <div className="flex flex-row-reverse  w-full gap-2 m-2">
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
        <h5 className="font-bold text-cyan-800">No Upload found</h5>
      )}
      {(loading) && (
        <h5 className="font-bold text-cyan-800">Loading Upload Info...</h5>
      )}
      {(upload && !loading && ( upload.status === UploadService.STATUSES.IN_PROCESS || upload.status === UploadService.STATUSES.UPLOADED) ) && (
        <h5 className="font-bold text-cyan-800">The Upload is being processed</h5>
      )}
      {(upload && !loading  && upload.status !== UploadService.STATUSES.IN_PROCESS && upload.status !== UploadService.STATUSES.UPLOADED ) && (
        <div className="card text-xl  w-full font-bold text-cyan-800 m-2">
          <h6> Upload:<span class="text-gray-600"> { upload.title } </span></h6>
          <h6> Date:<span class="text-gray-600"> { upload.date.toString() }</span></h6>
          <h6> Editor:<span class="text-gray-600"> { upload.editor }</span></h6>
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