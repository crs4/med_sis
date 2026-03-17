import React, { useEffect, useState, useRef } from 'react';
import Loading from '../../components/Loading';
import { useTranslations } from 'next-intl';
import { useUser } from '../../context/user';
import { useRouter } from 'next/router';
import { Panel } from 'primereact/panel';
import { Toast } from 'primereact/toast';
import { TaxonomyService } from '../../service/taxonomies';
 

export default function Page() {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const toast = useRef(null);
  
  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    const fetcData = async () => {
      setLoading(true);
      setLoading(false);
    }  
    fetcData();
  },[user]);  // eslint-disable-line

  if ( loading )
    return (<div className="layout-dashboard"> <Loading /> </div> )
 
  if ( !data )
     return (<div className="layout-dashboard"></div> ) 
  
  return (
      <div className="layout-dashboard">
      <Toast ref={toast} />
      <div className="card">
        <h5>Title {router.query.id} </h5>
        <Panel header="Info" toggleable>
          <div>Blah,Blah,Blah</div>
        </Panel>
      </div>
    </div>
  )
};

export async function getStaticPaths() {
  return {
    paths: [], //indicates that no page needs be created at build time
    fallback: 'blocking' //indicates the type of fallback
  }
}

export async function getStaticProps(context) {
  return {
    props: {
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}


