import { NextIntlClientProvider } from 'next-intl';
import { LayoutProvider } from '../layout/context/layoutcontext';
import Layout from '../layout/layout';
import 'primeflex/primeflex.css';
import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.css';
import '../styles/layout/layout.scss';
import '../styles/htmllegend/L.Control.HtmlLegend.css';
import '../styles/mygeoman.css'
import '../styles/timeline.css'

import {useRouter} from 'next/router';

export default function MyApp({ Component, pageProps }) {
    const router = useRouter();
    if (Component.getLayout) {
        return (
            <NextIntlClientProvider locale={router.locale} timeZone="Europe/Vienna" messages={pageProps.messages}>
                <LayoutProvider>
                    {Component.getLayout(<Component {...pageProps} />)}
                </LayoutProvider>
            </NextIntlClientProvider>
        )
    } else {
        return (
            <NextIntlClientProvider locale={router.locale} timeZone="Europe/Vienna" messages={pageProps.messages}>
                <LayoutProvider>
                    <Layout>
                        <Component {...pageProps} />
                    </Layout>
                </LayoutProvider>
            </NextIntlClientProvider>
        );
    }
}
