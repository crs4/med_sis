import React, { useEffect } from 'react';
import Footer from '../../components/Footer';
import ToDo from '../../components/ToDo';
import { useTranslations } from 'next-intl';
import { useUser } from '../../context/user';
import { useRouter } from 'next/router';
import { useParams } from 'next/navigation'
 
export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const params = useParams();
  

  useEffect(() => {
    if ( user.userData.forbidden !== null && user.userData.forbidden )
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
      indicator: indicator,
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}