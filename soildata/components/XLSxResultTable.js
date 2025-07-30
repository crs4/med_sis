import { Button } from 'primereact/button';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import 'primereact/resources/primereact.min.css';
import React, { useState } from 'react';
import {useTranslations} from 'next-intl';


const XLSxTable = ({
  elements,
  headers,
  title,
  classname,
}) => {

  const t  = useTranslations('default');
  const [isCollapsed, setIsCollapsed] = useState(true);
  
  const tableHeader = (
    <div className="p-d-flex p-jc-between p-ai-center"> 
      <div>
        <h5 className="p-mb-0p-text-capitalize ">{title}</h5>
      </div> 
      <div>
        <Button
          icon={`pi ${isCollapsed ? 'pi-angle-right' : 'pi-angle-down'}`}
          className="p-togglebutton"
          label={isCollapsed ? t('EXPAND') : t('COLLAPSE')}
          onClick={() => setIsCollapsed((v) => !v)}
        />
      </div>
    </div>
  );
/// [key,j,i,code]
  const valueTemplate0 = (rowData) => (
    <>
      <div className="p-d-flex p-jc-start p-ai-center">
        <div>{rowData['element']? rowData['element']:''}</div>
      </div>
    </>
  );

  const valueTemplate1 = (rowData) => (
    <>
      <div className="p-d-flex p-jc-start p-ai-center">
        <div>{rowData['model']? rowData['model']:''}</div>
      </div>
    </>
  );

  

  const valueTemplate2 = (rowData) => (
    <>
      <div className="p-d-flex p-jc-start p-ai-center">
        <div>{rowData['msg']? rowData['msg']:''}</div>
      </div>
    </>
  );

  return (
    <DataTable
      header={tableHeader}
      emptyMessage={t('NO_ELEMENT_FOUND')}
      value={elements}
      paginator
      sortMode="multiple"
      rows={20}
      rowsPerPageOptions={[10, 20, 50]}
      totalRecords={(elements && elements.length)? elements.length : 0}
      className={classname}
    >
    {!isCollapsed && headers[0] && (<Column header={headers[0]} field='element' sortable  body={valueTemplate0} />)}
    {!isCollapsed && headers[1] &&  (<Column header={headers[1]} field='model' sortable  body={valueTemplate1} />)}
    {!isCollapsed && headers[2] &&  (<Column header={headers[2]} field='msg' sortable  body={valueTemplate2} />)}
    
    </DataTable>
  );
};

export async function getStaticProps(context) {
  return {
    props: { 
      
      messages: (await import(`../translations/${context.locale}.json`)).default
     },
  }
}

export default XLSxTable;
