import React, { useEffect } from 'react';
import Footer from '../../components/Footer';
import ToDo from '../../components/todo';
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
    if ( user.userData.forbidden1 !== null && user.userData.forbidden1 )
        router.push(`/401`);
  },[user]);  // eslint-disable-line

  return (
    <>
      <ToDo />
      <Footer />
    </>
  );
};



export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}






