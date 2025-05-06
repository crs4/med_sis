import React from 'react';
import Footer from '../../components/Footer';
import ToDo from '../../components/ToDo';
import {useTranslations} from 'next-intl';
import Link from 'next/link'

const Page = () => {
  
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
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}

export default Page;

