import React, { forwardRef, useImperativeHandle, useContext, useRef } from 'react';
import Link from 'next/link';
import AppBreadCrumb from './AppBreadCrumb';
import { LayoutContext } from './context/layoutcontext';
import { useUser } from '../context/user';
import AppSidebar from './AppSidebar';
import { StyleClass } from 'primereact/styleclass';
import { useRouter } from 'next/router';
import {useTranslations} from 'next-intl';

const AppTopbar = forwardRef((props, ref) => {
    const t = useTranslations();
    const btnRef1 = useRef(null);
    const menubuttonRef = useRef(null);
    const { locale, locales, route } = useRouter();
    const { onMenuToggle, layoutConfig } = useContext(LayoutContext);
    const { userData } = useUser();
    const otherLocale = locales?.find((cur) => cur !== locale);
    const otherlang = (otherLocale === 'fr'? 'French' : 'Anglais');

    useImperativeHandle(ref, () => ({
        menubutton: menubuttonRef.current
    }));

    return (
        <div className="layout-topbar">
            <div className="topbar-left">
                <button ref={menubuttonRef} type="button" className="menu-button p-link" onClick={onMenuToggle}>
                    <i className="pi pi-chevron-left"></i>
                </button>
                <Link href="/">
                    <img 
                        id="logo-horizontal" 
                        className="horizontal-logo" 
                        src={`/soildata/img/logo-${layoutConfig.colorScheme === 'light' && (layoutConfig.menuTheme === 'white' || layoutConfig.menuTheme === 'orange') ? 'dark' : 'white'}.png`}
                        alt="s4m" 
                    />
                </Link>
                <span className="topbar-separator"></span>
                <AppBreadCrumb />
                <img
                    id="logo-mobile"
                    className="mobile-logo"
                    src={`/soildata/img/logo-${layoutConfig.colorScheme === 'light' && (layoutConfig.menuTheme === 'white' || layoutConfig.menuTheme === 'orange') ? 'dark' : 'white'}.png`}
                    alt="S4M"
                />
            </div>
            <div className="layout-topbar-menu-section">
                <AppSidebar sidebarRef={props.sidebarRef} />
            </div>
            <div className="layout-mask modal-in"></div>
            <div className="topbar-right">
                <ul className="topbar-menu">                   
                    <li className="profile-item static sm:relative">
                        <Link href={route} locale={otherLocale}>
                            <img className="language-image pr-4" style={{width: '50px'}} src={`/soildata/img/${otherLocale}.png`} alt="" />
                            <span className="text-lg uppercase ">{otherlang}</span>
                        </Link>   
                    </li>
                    <li className="profile-item static sm:relative">
                        <StyleClass nodeRef={btnRef1} selector="@next" enterClassName="hidden" enterActiveClassName="scalein" leaveToClassName="hidden" leaveActiveClassName="fadeout" hideOnOutsideClick="true">
                            <a tabIndex={0} ref={btnRef1}>
                                <img src='/soildata/img/user-default.png' alt="user" className="profile-image" />
                                <span className="profile-name">{userData.preferred_username}</span>
                            </a>
                        </StyleClass>
                    </li>
                </ul>
            </div>
        </div>
    );
});

export async function getStaticProps(context) {
    return {
      props: { 
        messages: (await import(`../translations/${context.locale}.json`)).default
      },
    }
}

export default AppTopbar;
