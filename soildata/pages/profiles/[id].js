import React, { useEffect } from 'react';
import Footer from '../../components/Footer';
import ToDo from '../../components/ToDo';
import { useParams } from 'next/navigation';
import { Button } from 'primereact/button';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import Taxonomies from '../../data/taxonomies';
import Mapping from '../../data/mapping';
//import Test from '../../data/test';
import { useTranslations } from 'next-intl';
import { useUser } from '../../context/user';
import { useRouter } from 'next/router';
import { ProfileService } from '../../service/profiles';

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const params = useParams();
  

  useEffect(() => {
      if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 )
          router.push(`/401`);
    },[user]);  // eslint-disable-line

  return (
    <>
      <ToDo />
      <Footer />
    </>
  );
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
      profile: profile,
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}



