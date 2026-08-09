
/*
  Copyright (C) 2026 CRS4

  HOME page with links
  
  @bobdemo Roberto Demontis demontis@crs4.it

*/

import React, { useState, useEffect, useRef } from 'react';
import { Card } from 'primereact/card';
import Image from 'next/image';
import profileIMG from '../public/img/soil_profile.png'
import toolsIMG from '../public/img/tools.jpg';
import indicatorIMG from '../public/img/soil_indicators.png';
import taxonomiesIMG from '../public/img/taxonomies.jpg';
import uploadIMG from '../public/img/upload.png';
import ptfIMG from '../public/img/ptf.png';
import { useTranslations } from 'next-intl';
import Link from 'next/link';
import UserService from '../service/user';
import { useRouter } from 'next/router';

const Home = () => {
  const t  = useTranslations('default');
  const router = useRouter();
  const [points, setPoints] = useState('');
  const [labData, setLabData] = useState('');
  const [indicators, setIndicators] = useState('');
  const headerA = (
    <Image alt="Upload Soil Data" className="w-full" style="height: 200px;" src={uploadIMG} />
  );
  const headerB = (
    <Image alt="Points Soil Data" className="w-full" style="height: 200px;" src={profileIMG} />
  );
  const headerC = (
    <Image alt="Publish" className="w-full" style="height: 200px;" src={indicatorIMG} />
  );
  const headerD = (
    <Image alt="Taxonomies" className="w-full" style="height: 200px;" src={taxonomiesIMG} />
  );
  const headerE = (
    <Image alt="Tools" className="w-full" style="height: 200px;" src={toolsIMG} />
  );

  const headerF = (
    <Image alt="Tools" className="w-full" style="height: 200px;" src={ptfIMG} />
  );

  const footerA = (
    <div className="text-overflow-ellipsis">
      {t('SIS_BACKOFFICE_UPLOAD')}
    </div>
  );

  const footerB = (
    <div className="text-overflow-ellipsis">
      {t('SIS_BACKOFFICE_POINTS')}   
    </div>
  );

  const footerC = (
    <div className="text-overflow-ellipsis">
      {t('SIS_BACKOFFICE_PUBLISH')}    
    </div>
  );

  const footerD = (
    <div className="text-overflow-ellipsis">
      {t('SIS_BACKOFFICE_TAXONOMY')}  
    </div>
  );

  const footerE = (
    <div className=" text-overflow-ellipsis">
        {t('SIS_BACKOFFICE_CONFIGURE')} 
    </div>
  );

  const footerF = (
    <div className=" text-overflow-ellipsis">
        {t('SIS_BACKOFFICE_HYDROPTF')}  
    </div>
  );
  
  const fetchUser = ( async() => {
    try {
      const user = await UserService.getProfile(document.cookie);
      console.log(user)
      if ( !user || ( user.forbidden !== null && user.forbidden) )
        router.push(`/401`);
    }  
    catch( error ) { 
      console.log(error)
    } 
  }) 

  useEffect(() => {
      fetchUser()       
  },[]);  // eslint-disable-line

  return (
      <div className="layout-dashboard">
        <div className="grid">
          <div className="col text-center justify-content-center m-4 ">
            <h1 className="text-cyan-800">{t('SIS_BACKOFFICE_TITLE')}</h1>
            <div>{t('SIS_BACKOFFICE_SUBTITLE')}</div>
            <div className="flex text-xl text-justify w-full m-2 text-cyan-800">
              <p>{t('SIS_BACKOFFICE_HOME1')}{t('SIS_BACKOFFICE_HOME2')}</p>
            </div>
          </div>
        </div>  
        <div className="grid justify-content-center gap-4">
          <Card title={t('UPLOAD_TITLE')} footer={footerA} header={headerA} 
              className="w-20rem h-40rem cursor-pointer" onClick={ () => router.push(`/uploads`)}>
          </Card>
          <Card  title={t('POINTS_TITLE')} footer={footerB} header={headerB} 
            className="w-20rem h-40rem cursor-pointer"  onClick={ () => router.push(`/points`)}>
          </Card>
          <Card  title={t('PUBLISHING_TITLE')} footer={footerC} header={headerC} 
            className="w-20rem h-40rem cursor-pointer" onClick={ () => router.push(`/publish`)}>
          </Card>
          <Card  title={t('TAXONOMIES_TITLE')} footer={footerD} header={headerD} 
            className="w-20rem h-40rem cursor-pointer" onClick={ () => router.push(`/taxonomy`)}>
          </Card>
          <Card  title={t('CONFIGURE_TITLE')} footer={footerE} header={headerE} 
            className="w-20rem h-40rem cursor-pointer" onClick={ () => router.push(`/configure`)}>
          </Card>
          <Card  title={t('HYDRO_PTF_TITLE')} footer={footerF} header={headerF} 
            className="w-20rem h-40rem cursor-pointer" onClick={ () => router.push(`/hydroptf`)}>
          </Card>
        </div>
      </div>          
    );
};

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../translations/${context.locale}.json`)).default
    },
  }
}

export default Home;

