import React, { useEffect } from 'react';
import Footer from '../../../components/Footer';
import ToDo from '../../../components/ToDo';
import { useTranslations } from 'next-intl';
import { useUser } from '../../../context/user';
import { useRouter } from 'next/router';

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();

  useEffect(() => {
      if ( user.forbidden )
        router.push(`/soildata/401`);
    },[user,router]);

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
      messages: (await import(`../../../translations/${context.locale}.json`)).default
     },
  }
}


