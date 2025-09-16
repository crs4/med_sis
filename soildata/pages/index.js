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
    <Image alt="Points Data" src={profileIMG} />
  );

  const headerS = (
    <Image alt="Laboratory data" src={sampleIMG} />
  );

  const headerI = (
    <Image alt="Soil Indicators" src={indicatorIMG} />
  );

  const headerM = (
    <Image alt="Soil Maps" src={indicatorIMG} />
  );

  const footerP = (
    
    <div className="flex flex-wrap justify-content-center gap-2">
      <Link href="/points">
        <i className="layout-menuitem-icon fad fa-columns"></i>
        <span className="layout-menuitem-text p-m-2">{t('GO_TO_LEGACY')}</span>
      </Link>
    </div>
  );

  const footerS = (
    <div className="flex flex-wrap justify-content-center gap-2">
      <Link href="/todo">
        <i className="layout-menuitem-icon fad fa-columns"></i>
        <span className="layout-menuitem-text p-m-2">{t('GO_TO_MONITORING')}</span>
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

  const footerM = (
    <div className="flex flex-wrap justify-content-center gap-2">
      <Link href="/todo">
        <i className="layout-menuitem-icon fad fa-columns"></i>
        <span className="layout-menuitem-text p-m-2">{t('GO_TO_SOILS_MAP')}</span>
      </Link>  
    </div>
  );

  useEffect(() => {
    if ( user.userData.forbidden2 !== null && user.userData.forbidden2 )
        router.push(`/401`);
    },[user]);  // eslint-disable-line

  return (
      <div className="layout-dashboard">
        <div className="grid grid-cols-12">
          <div className="col-4 flex justify-center">
            <Card title={t('POINTS DATA')} subTitle="Some text and metrics" footer={footerP} header={headerP} className="col-25rem">
                
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('LABORATORY DATA')} subTitle="Some text and metrics"  footer={footerS} header={headerS} className="col-25rem">
                
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('INDICATORS')} subTitle="Some text and metrics" footer={footerI} header={headerI} className="col-25rem">
                   
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('SOILS_MAP')} subTitle="Some text and metrics" footer={footerM} header={headerM} className="col-25rem">
                   
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
