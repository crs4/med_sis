import React from 'react';
import Footer from '../../../components/Footer';
import ToDo from '../../../components/ToDo';
import {useTranslations} from 'next-intl';

export default function Page()  {
  
  const t = useTranslations('default');

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

