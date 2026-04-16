
import React, { useEffect, useState, useRef } from 'react';
import {useTranslations} from 'next-intl';


export default function Page()  {
  const t = useTranslations('default');
  

  return (
    <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            
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

