import React from 'react';
import Image from 'next/image';
import license from '../public/img/license.png';
import CRS4Logo from '../public/img/logo-dark.png';

export default function Footer() {
  return (
    <div className="layout-footer">
      <div
        className="footer-logo-container p-d-flex p-flex-row"
        style={{ width: '100%', justifyContent: 'space-between' }}
      >
        <div className="p-d-flex p-flex-row p-ai-center">
          <a
            href="https://creativecommons.org/licenses/by-nc-sa/4.0/"
            title="Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)"
            target="_blank"
            aria-label="license"
            rel="noreferrer"
          >
            <Image src={license} alt="License" height={30} />
          </a>
        </div>
        <div className="p-d-flex p-flex-row p-ai-center">
          <span className="p-mr-3">powered by</span>
          <a href="https://www.crs4.it" rel="noreferrer" target="_blank">
            <Image src={CRS4Logo} alt="CRS4 Logo" height={30} 
            />
          </a>
        </div>
      </div>
    </div>
  )
}
