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

  const colLabel = (index) => {
    if ( !index ) 
      return '';
    const a = Number(index);
    if ( isNaN(a) || a < 1  )
      return '' ;
    let q = Math.floor(a/26) ;
    let r = a % 26;
    if ( r === 0 ){
      r=26
      q-=1
    }
    const label = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if ( a < 27 )
      return index.toString() + ' or ' + label.charAt(a - 1);
    else 
      return index.toString() + ' or ' + label.charAt(q - 1) +label.charAt(r - 1);
  }
  
  
  
  const tableHeader = (
    <div className="p-d-flex p-jc-between p-ai-center"> 
      <div>
        <h5 className="p-mb-0p-text-capitalize">{title}</h5>
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
        <div>{rowData[0]? rowData[0]:''}</div>
      </div>
    </>
  );

  const valueTemplate1 = (rowData) => (
    <>
      <div className="p-d-flex p-jc-start p-ai-center">
        <div>{rowData[1]? rowData[1]:''}</div>
      </div>
    </>
  );

  const valueTemplate2 = (rowData) => (
    <>
      <div className="p-d-flex p-jc-start p-ai-center">
        <div>{ rowData[2]? colLabel(rowData[2]):''}</div>
      </div>
    </>
  );

  const valueTemplate3 = (rowData) => (
    <>
      <div className="p-d-flex p-jc-start p-ai-center">
        <div>
          {rowData[3]==='-t'? 'Wrong Classification code field':''}
          {rowData[3]==='-n'? 'Wrong Number field':''}
          {rowData[3]==='-b'? 'Wrong Boolean field':''}
          {rowData[3]==='-d'? 'Wrong Date field':''}
          {rowData[3]==='-%'? 'Wrong Percentage value field':''}
          {rowData[3]==='-0'? 'Wrong Positive value field':''}
          {rowData[3]==='-lat'? 'Wrong Latitude value field':''}
          {rowData[3]==='-lon'? 'Wrong Logitude value field':''}
          {rowData[3]==='-rt'? 'found Rich Text instead of Plain Text':''}
          {rowData[3]==='-k'? 'Error: duplicate key found':''}
        </div>
      </div>
    </>
  );

  return (
    <DataTable
      header={tableHeader}
      emptyMessage={t('NO_ERROR_FOUND')}
      value={elements}
      paginator
      sortMode="multiple"
      rows={10}
      rowsPerPageOptions={[10, 20, 50]}
      totalRecords={(elements && elements.length)? elements.length : 0}
      className={classname}
    >
    {!isCollapsed && headers[0] && (<Column header={headers[0]} field='0' sortable  body={valueTemplate0} />)}
    {!isCollapsed && headers[1] &&  (<Column header={headers[1]} field='1' sortable  body={valueTemplate1} />)}
    {!isCollapsed && headers[2] &&  (<Column header={headers[2]} field='2' sortable  body={valueTemplate2} />)}
    {!isCollapsed && headers[2] &&  (<Column header={headers[3]} field='3' sortable  body={valueTemplate3} />)}
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
