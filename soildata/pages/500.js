import React from 'react';
import SystemError from './error/index';

const Custom500 = () => {
    return <SystemError />;
};

Custom500.getLayout = function getLayout(page) {
    return page;
};

export async function getStaticProps(context) {
    return {
      props: { 
        messages: (await import(`../translations/${context.locale}.json`)).default
       },
    }
}

export default Custom500;
