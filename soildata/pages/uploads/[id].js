"use client"

import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic"
import { Toast } from 'primereact/toast';
import { Button } from 'primereact/button';
import { point, featureCollection } from '@turf/turf';
import UserService from '../../service/user';
import ReportTable from '../../components/table/XLSxResultTable';
import { UploadService } from '../../service/uploads';
import { TaxonomyService } from '../../service/taxonomies';


const MyMap = dynamic(() => import("../../components/map/XLSxMap"), { ssr:false })

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const id = router.query.id;
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
      const user = await UserService.getProfile(document.cookie);
      if ( !user || ( user.forbidden !== null && user.forbidden) )
        router.push(`/401`);    
      if ( !id )
        return;
      let response = await UploadService.get(document.cookie,id)
      if ( !response && !response.data )
        toast.current.show({severity:'error', summary: t('ERRORS'), detail: t('NO_ERRORS') , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: t('SUCCESS') , detail: t('SUCCESS') , life: 3000});
        setUpload(response.data);
      }
      setLoading(false); 
    })
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    fetchData(id);
  },[]);  // eslint-disable-line   

  let reportHeaders = [ t('UPLOADS_REPORT_F1'),  t('UPLOADS_REPORT_F2'),  t('UPLOADS_REPORT_F3')];
  
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('UPLOAD_RESULTS')}</h4>
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
        <h5 className="font-bold text-cyan-800">{t('EMPTY')}</h5>
      )}
      {(loading) && (
        <h5 className="font-bold text-cyan-800">{t('LOADING')}</h5>
      )}
      {(upload && !loading && ( upload.status === UploadService.STATUSES.IN_PROCESS || upload.status === UploadService.STATUSES.UPLOADED) ) && (
        <h5 className="font-bold text-cyan-800">{t('UPLOADS_IN_PROCESS')}</h5>
      )}
      {(upload && !loading  && upload.status !== UploadService.STATUSES.IN_PROCESS && upload.status !== UploadService.STATUSES.UPLOADED ) && (
        <div className="card text-xl  w-full font-bold text-cyan-800 m-2">
          <h4> Upload:<span class="font-bold text-gray-600"> { upload.title } </span></h4>
          <h4> Date:<span class="text-gray-600"> { upload.date.toString() }</span></h4>
          <h4><span class="font-italic text-gray-600"> { upload.editor }</span></h4>
        </div>
      )} 
      {(upload && upload.report && upload.report['errors'] && 
        Array.isArray(upload.report['errors']) && upload.report['errors'].length > 0 ) && ( 
          <ReportTable
            elements={upload.report['errors']}
            headers={reportHeaders}
            title={ upload.title + ': ' + upload.report['errors'].length + ' ' + t('ERRORS')}
            className='p-mt-4 p-mb-4' />         
      )}
      {(upload && upload.report && upload.report['operations'] && 
        Array.isArray(upload.report['operations']) && upload.report['operations'].length > 0 ) && ( 
          <ReportTable
            elements={upload.report['operations']}
            headers={reportHeaders}
            title={upload.title +': ' + t('UPLOADS_OPERATIONS')  }
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