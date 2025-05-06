import Head from 'next/head';
import React, { useState } from 'react';

export const LayoutContext = React.createContext();

export const LayoutProvider = (props) => {
    const [breadcrumbs, setBreadcrumbs] = useState([]);
    const [layoutConfig, setLayoutConfig] = useState({
        ripple: false,
        inputStyle: 'outlined',
        menuMode: 'slim',
        menuTheme: 'brown',
        colorScheme: 'light',
        theme: 'blue',
        scale: 14
    });

    const [layoutState, setLayoutState] = useState({
        staticMenuDesktopInactive: false,
        overlayMenuActive: false,
        overlaySubmenuActive: false,
        rightMenuVisible: false,
        configSidebarVisible: false,
        staticMenuMobileActive: false,
        menuHoverActive: false,
        searchBarActive: false,
        resetMenu: false,
        sidebarActive: false,
        anchored: false
    });

    const onMenuToggle = (event) => {
        if (isOverlay()) {
            setLayoutState((prevLayoutState) => ({
                ...prevLayoutState,
                overlayMenuActive: !prevLayoutState.overlayMenuActive
            }));
        }
        if (isDesktop()) {
            setLayoutState((prevLayoutState) => ({
                ...prevLayoutState,
                staticMenuDesktopInactive: !prevLayoutState.staticMenuDesktopInactive
            }));
        } else {
            setLayoutState((prevLayoutState) => ({
                ...prevLayoutState,
                staticMenuMobileActive: !prevLayoutState.staticMenuMobileActive
            }));

            event.preventDefault();
        }
    };

    const hideOverlayMenu = () => {
        setLayoutState((prevLayoutState) => ({
            ...prevLayoutState,
            overlayMenuActive: false,
            staticMenuMobileActive: false
        }));
    };

    const toggleSearch = () => {
        setLayoutState((prevLayoutState) => ({
            ...prevLayoutState,
            searchBarActive: !layoutState.searchBarActive
        }));
    };

    const onSearchHide = () => {
        setLayoutState((prevLayoutState) => ({
            ...prevLayoutState,
            searchBarActive: false
        }));
    };

    const onRightMenuButtonClick = (event) => {
        setLayoutState((prevLayoutState) => ({
            ...prevLayoutState,
            rightMenuVisible: !layoutState.rightMenuVisible
        }));
        hideOverlayMenu();

        event.preventDefault();
    };

    const isOverlay = () => {
        return layoutConfig.menuMode === 'overlay';
    };

    const isSlim = () => {
        return layoutConfig.menuMode === 'slim';
    };

    const isCompact = () => {
        return layoutConfig.menuMode === 'compact';
    };

    const isHorizontal = () => {
        return layoutConfig.menuMode === 'horizontal';
    };

    const isDesktop = () => {
        return window.innerWidth > 991;
    };

    const value = {
        layoutConfig,
        setLayoutConfig,
        layoutState,
        setLayoutState,
        isSlim,
        isCompact,
        isHorizontal,
        isDesktop,
        onMenuToggle,
        toggleSearch,
        onSearchHide,
        onRightMenuButtonClick,
        breadcrumbs,
        setBreadcrumbs
    };

    return (
        <LayoutContext.Provider value={value}>
            <>
                <Head>
                    <title>Soil4Med Back-Office</title>
                    <meta charSet="UTF-8" />
                    <meta name="description" content="The ultimate collection of design-agnostic, flexible and accessible React UI Components." />
                    <meta name="robots" content="index, follow" />
                    <meta name="viewport" content="initial-scale=1, width=device-width" />
                    <meta property="og:type" content="website"></meta>
                    <meta property="og:title" content="Soil4Med Back-Office"></meta>
                    <meta property="og:url" content="https://soils4med.crs4.it/soildata"></meta>
                    <meta property="og:description" content="Soils4Med tool for soils data management" />
                    <meta property="og:image" content="/soildata/img/logo-dark.png"></meta>
                    <meta property="og:ttl" content="604800"></meta>
                    <link rel="icon" href={`/soildata/favicon.ico`} type="image/x-icon"></link>
                    <link id="theme-link" href="/soildata/theme/theme-light/blue/theme.css" rel="stylesheet"></link>
                </Head>
                {props.children}
            </>
        </LayoutContext.Provider>
    );
};
