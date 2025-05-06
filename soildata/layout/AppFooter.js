import React, { useState } from 'react';

import { useContext, useEffect } from 'react';

import { LayoutContext } from './context/layoutcontext';

const AppFooter = () => {
    const { layoutConfig } = useContext(LayoutContext);

    return (
        <div className="layout-footer">
            <div className="footer-logo-container">
                <img src='/soildata/img/soils4med-logo.png' alt="s4m" />
                <span className="footer-app-name">S4M Back Office</span>
            </div>
            <span className="footer-copyright">&#169; CRS4 - 2025</span>
        </div>
    );
};

export default AppFooter;
