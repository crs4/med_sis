import React from 'react';


export default function Loading({ title }) {
  return (
    <div className="layout-dashboard">
      <div className="flex flex-row w-full text-cyan-800 text-xl justify-content-center p-3 m-3">
        <span> <i className="pi pi-spin pi-spinner" /> {title}</span> 
      </div>
    </div>
  );
}
