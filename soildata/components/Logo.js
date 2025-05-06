import React from 'react';
import Link  from 'next/link';
import Image from 'next/image';
import S4MLogo from '../public/img/soils4med-logo.png';


export default function Logo() {
  return (
    <div className="p-text-center">
      <Link href="/soildata/">
        <div className="p-d-flex p-ai-center">
          <Image
            src={S4MLogo}
            alt="SOILS4MED logo"
            width={200}
            style={{ margin: '25px 15px 25px 0' }}
          />
        </div>
      </Link>
    </div>
  );
}

