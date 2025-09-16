"use client"

import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic"
import { TreeTable } from 'primereact/treetable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { useUser } from '../../context/user';
import { ProfileService } from '../../service/profiles';


const MyMap = dynamic(() => import("../../components/PointMap"), { ssr:false })

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const id = router.query.id
  const user = useUser();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [nodes, setNodes] = useState(null);
  const [point, setPoint] = useState(null);
  const toast = useRef(null); 

  
  useEffect(() => {
      if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 )
            router.push(`/401`);
      
  },[user]);  // eslint-disable-line
  
  useEffect(() => {
    const fetchData = ( async(id) => {
      let data = await ProfileService.getLegacy(document.cookie, id)
      if ( !data )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Profile not found ' + id , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'The profile ' + id + ' has been loaded' , life: 3000});
        setProfile(data);
        const main = data ['ProfileGeneral']
        if ( main.lat_wgs84 && main.lon_wgs84 )
          setPoint ( [main.lat_wgs84, main.lon_wgs84] )
      }
      let _nodes = await ProfileService.generateLegacyTreeNode(profile);
      if (_nodes)
        setNodes(_nodes)
      setLoading(false); 
    })
    if ( id )
      fetchData(id);
  }, [id]); // eslint-disable-line


  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      {(!profile && !loading ) && (
        <h2>No legacy profile found</h2>
      )}
      {(loading) && (
        <h2>Loading legacy profile data...</h2>
      )}
      {(profile ) && (
      <div className="grid grid-cols-12">
        <div className="col-6 flex" style={{ height: '300px' }}>
          <h2>legacy profile data head</h2>
        </div>
        <div className="col-6 flex">
        {(point) && (    
          <MyMap point={point} />  
        )}
        </div>
        <div className="col-12 flex justify-center" >
          <Button onClick={toggleApplications} label="Toggle Expand" />
          <TreeTable value={nodes.main} expandedKeys={expandedKeys} onToggle={(e) => setExpandedKeys(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
            <Column field="name" header="Name" expander></Column>
            <Column field="value" header="Value"></Column>
            <Column field="type" header="Actions"></Column>
          </TreeTable>
        </div> 
        <div className="col-12 flex justify-center" >
          <Button onClick={toggleApplications} label="Toggle Expand" />
          <TreeTable value={nodes.layer1} expandedKeys={expandedKeys} onToggle={(e) => setExpandedKeys(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
            <Column field="name" header="Name" expander></Column>
            <Column field="value" header="Value"></Column>
            <Column field="type" header="Actions"></Column>
          </TreeTable>
        </div>
        <div className="col-12 flex justify-center" >
          <Button onClick={toggleApplications} label="Toggle Expand" />
          <TreeTable value={nodes.layer1} expandedKeys={expandedKeys} onToggle={(e) => setExpandedKeys(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
            <Column field="name" header="Name" expander></Column>
            <Column field="value" header="Value"></Column>
            <Column field="type" header="Actions"></Column>
          </TreeTable>
        </div> 
      </div>
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



