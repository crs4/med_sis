import React, { useState, useContext } from 'react';
import AppConfig from '../../layout/AppConfig';
import { LayoutContext } from '../../layout/context/layoutcontext';
import { Button } from 'primereact/button';
import {useTranslations} from 'next-intl';

export default function Forbidden() { 
    const { layoutConfig } = useContext(LayoutContext);
    const t = useTranslations('default');

    return (
        <>
            <div className="px-5 min-h-screen flex justify-content-center align-items-center bg-cover bg-center" style={{ backgroundImage: 'url(/soildata/img/bg-error.jpg)' }}>
                <div className="z-1 text-center">
                    <div className="text-900 font-bold text-white text-8xl mb-4">System Error</div>
                    <p className="line-height-3 text-white mt-0 mb-5 text-700 text-xl font-medium">Some went wrong.</p>
                    <Button
                        raised
                        className="font-medium"
                        onClick={() => {
                            window.location.href = '/soildata';
                        }}
                        label="Go to BackOffice Home"
                    />
                </div>
            </div>
        </>
    );
}

Forbidden.getLayout = function getLayout(page) {
    return (
        <React.Fragment>
            {page}
            <AppConfig minimal />
        </React.Fragment>
    );
};

export async function getStaticProps(context) {
    return {
      props: { 
        messages: (await import(`../../translations/${context.locale}.json`)).default
       },
    }
}



