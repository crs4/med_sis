import React, { useEffect } from 'react';
import Footer from '../../../components/Footer';
import ToDo from '../../../components/ToDo';
import { useTranslations } from 'next-intl';
import { useUser } from '../../../context/user';
import { useRouter } from 'next/router';
import { useParams } from 'next/navigation'

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const params = useParams();
  
  useEffect(() => {
      if ( !(user.isDataManager()) )
        router.push(`/soildata/401`);
    },[user,router]);


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
      sample: sample,
      messages: (await import(`../../../translations/${context.locale}.json`)).default
     },
  }
}


