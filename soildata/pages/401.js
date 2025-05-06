import React from 'react';
import Forbidden from '../pages/forbidden/index';

const Custom401 = () => {
    return <Forbidden />;
};

Custom401.getLayout = function getLayout(page) {
    return page;
};

export async function getStaticProps(context) {
    return {
      props: { 
        messages: (await import(`../translations/${context.locale}.json`)).default
       },
    }
}


export default Custom401;
