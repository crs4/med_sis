import React from 'react';

export default function Loading(title) {
  return (
    <div className="layout-dashboard">
      <div className="p-grid p-jc-center p-ai-center">
        <div className="p-text-center">
          <h4>{ title? title :'Loading' }</h4>
          <i className="pi pi-spin pi-spinner" style={{ fontSize: '2em' }} />
        </div>
      </div>
    </div>
  );
}
