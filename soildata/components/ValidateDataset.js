"use client"

import { point, featureCollection } from '@turf/turf';
import React, { useState, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';


import { FileUpload } from 'primereact/fileupload';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import TaxonomyService from '../service/taxonomies';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../context/user';
import { ProfileService } from '../service/profiles';
import dynamic from 'next/dynamic'

const MyMap = dynamic(() => import("./AoiSelectionMap"), { ssr:false })

export default function CreateDataset( { dataset, setDataset })  {
  
  const [taxonomies, setTaxonomies] = useState(null);
  const [loading, setLoading] = useState(true);
  const [map, setMap] = useState(null);
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  
  const openList = () => {
    router.push(`/datasets`);
  };

  const saveDataset = async () => {
    try {
      
    } catch (error) {
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving data' , life: 3000}); 
    } 

  } 
  
  useEffect(() => {
    const fetchData = ( async() => {
       
    })
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    else {
      fetchData();
    }
  }, [user]); // eslint-disable-line


  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
        
    </div>
  );
}

export async function getStaticProps(context) {
  return {
    props: {       
      messages: (await import(`../translations/${context.locale}.json`)).default
    },
  }
}
