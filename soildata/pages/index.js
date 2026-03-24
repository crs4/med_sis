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
  const [points, setPoints] = useState('');
  const [labData, setLabData] = useState('');
  const [indicators, setIndicators] = useState('');
  const headerP = (
    <Image alt="Points Data" src={profileIMG} />
  );

  const headerS = (
    <Image alt="Laboratory data" src={sampleIMG} />
  );

  const headerI = (
    <Image alt="Soil Indicators" src={indicatorIMG} />
  );

  const footerP = (
    
    <div className="flex flex-wrap justify-content-center gap-2">
      
    </div>
  );

  const footerS = (
    <div className="flex flex-wrap justify-content-center gap-2">
      
    </div>
  );

  const footerI = (
    <div className="flex flex-wrap justify-content-center gap-2">
        
    </div>
  );

  const readNumber = (xml) => {
    if (!xml)
      return
    try {
      let i = xml.indexOf('numberMatched="');
      let number = xml.substring(i);
      i = px.indexOf('"');
      number = number.substring(0,i)
      if ( parseInt(number) != NaN )
        return px;
      else return '';
    }
    catch (e){
      console.log(e);
    }  
    return '';
  }

  useEffect(() => {
    if (  !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ) )
      router.push(`/401`);
    
  },[user]);  // eslint-disable-line

  return (
      <div className="layout-dashboard">
        <div className="grid">
          <div className="col text-center justify-content-center m-4 ">
            <h1 className="text-brown-700">SIS Back Office</h1>
            <div>SOIL POINT DATA MANAGING TOOLS</div>
          </div>
        </div>  
        <div className="grid">
          <div className="col-4 flex justify-center">
            <Card title={t('POINTS DATA')} subTitle={points + " points"} footer={footerP} header={headerP} className="col-25rem">
                
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('LABORATORY DATA')} subTitle={labData + " records"}  footer={footerS} header={headerS} className="col-25rem">
                
            </Card>
          </div>
          <div className="col-4 flex justify-center">
            <Card  title={t('INDICATORS')} subTitle={indicators + " Soil Indicators"} footer={footerI} header={headerI} className="col-25rem">
                   
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

