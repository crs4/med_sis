import React, { useState, useEffect, useRef } from 'react';
import { Card } from 'primereact/card';
import Image from 'next/image';
import profileIMG from '../public/img/soil_profile.png'
import sampleIMG from '../public/img/soil_sample.jpg';
import indicatorIMG from '../public/img/soil_indicator.jpg';
import { useTranslations } from 'next-intl';
import Link from 'next/link';
import { useUser } from '../context/user';
import { useRouter } from 'next/router';

const Home = () => {
  const t  = useTranslations('default');
  const user = useUser();
  const router = useRouter();
  const headerP = (
    <Image alt="Profiles" src={profileIMG} />
  );

  const headerS = (
    <Image alt="Samples" src={sampleIMG} />
  );

  const headerI = (
    <Image alt="Indicators" src={indicatorIMG} />
  );

  const footerP = (
    
    <div className="flex flex-wrap justify-content-center gap-2">
      <Link href="/profiles">
        <i className="layout-menuitem-icon fad fa-columns"></i>
        <span className="layout-menuitem-text p-m-2">{t('GO_TO_PROFILES')}</span>
      </Link>
    </div>
  );

  const footerS = (
    <div className="flex flex-wrap justify-content-center gap-2">
      <Link href="/samples">
        <i className="layout-menuitem-icon fad fa-columns"></i>
        <span className="layout-menuitem-text p-m-2">{t('GO_TO_SAMPLES')}</span>
      </Link>
    </div>
  );

  const footerI = (
    <div className="flex flex-wrap justify-content-center gap-2">
      <Link href="/indicators">
        <i className="layout-menuitem-icon fad fa-columns"></i>
        <span className="layout-menuitem-text p-m-2">{t('GO_TO_INDICATORS')}</span>
      </Link>  
    </div>
  );

  useEffect(() => {
      if ( user.forbidden )
        router.push(`/soildata/401`);
  },[user, router]);

  return (
      <div className="layout-dashboard">
        <div className="grid grid-cols-12">
          <div className="col-4 flex justify-center">
            <Card title={t('PROFILES')} subTitle="Some text and metrics" footer={footerP} header={headerP} className="col-25rem">
                
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('SAMPLES')} subTitle="Some text and metrics"  footer={footerS} header={headerS} className="col-25rem">
                
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('INDICATORS')} subTitle="Some text and metrics" footer={footerI} header={headerI} className="col-25rem">
                   
            </Card>
          </div>
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
