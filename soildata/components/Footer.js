import React from 'react';
import Image from 'next/image';
import license from '../public/img/license.png';
import CRS4Logo from '../public/img/logo-dark.png';

export default function Footer() {
  return (
    <div className="layout-footer">
      <div
        className="footer-logo-container flex flex-row"
        style={{ width: '100%', justifyContent: 'space-between' }}
      >
        <div className="flex flex-row align-items-center">
          <span className="p-mr-3">powered by</span>
          <a href="/" rel="noreferrer" target="_blank">
            <img src='soildata/img/loghi.png' alt="Soils4med Logo - Crs4 Logo" height={40} 
            />
          </a>
        </div>
      </div>
    </div>
  )
}
