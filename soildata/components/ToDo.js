import React from 'react';
import Logo from './Logo';
import Link from 'next/link';
import Image from 'next/image';
import ToDoImg from '../public/img/ToDo.png';

export default function ToDo(  ) {
  
  return (
    <>
      <div
        className="p-d-flex p-jc-center p-ai-center text-center p-flex-column"
        style={{ height: '85vh' }}
      >
        <div className="p-d-flex text-center p-ai-center p-flex-column">
          <Logo />
          <div
            className="p-d-flex p-flex-column text-center p-p-6 p-shadow-5 rounded"
          >
            <div className="p-d-flex justify-center">
              <Image  src={ToDoImg}  alt="Coming Soon" width={430} />
            </div>
            <p className="p-col-12 p-md-12 p-text-center p-mt-6">
                <Link href="/">HOME</Link>
            </p> 
          </div>
        </div>
      </div>
    </>
  );
};




