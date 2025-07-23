import React from 'react';


export default function Loading({ title }) {
  return (
    <div className="layout-dashboard">
      <div className="grid grid-cols-12">
          <div className="col-4 flex justify-center">
            <div className="p-text-center">
              <h2>{title}</h2>
              <i className="pi pi-spin pi-spinner" style={{ fontSize: '2em' }} />
            </div>
          </div>
      </div>
    </div>
  );
}
