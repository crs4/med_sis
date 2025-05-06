import React from 'react';
import NotFound from '../pages/notfound/index';

const Custom404 = () => {
    return <NotFound />;
};

Custom404.getLayout = function getLayout(page) {
    return page;
};

export async function getStaticProps(context) {
    return {
      props: { 
        messages: (await import(`../translations/${context.locale}.json`)).default
       },
    }
}

export default Custom404;
