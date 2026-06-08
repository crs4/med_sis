import { Button } from 'primereact/button';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import 'primereact/resources/primereact.min.css';
import React, { useState } from 'react';
import {useTranslations} from 'next-intl';


const PointsTable = ({
  elements,
  headers,
  title,
  classname,
}) => {

  const t  = useTranslations('default');
  const [isCollapsed, setIsCollapsed] = useState(true);
  
  const dateBodyTemplate = (rowData) => {
    return rowData[2].toLocaleDateString('en-US', {
      day: '2-digit', month: '2-digit', year: 'numeric'
    });
  };

  const header = (
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
  
  return (
    <DataTable
      value={elements}
      paginator
      dataKey="id"
      className="p-datatable-gridlines"
      showGridlines
      rows={10}
      responsiveLayout="scroll"
      emptyMessage="No points soil data found."
      header={header}
    >
      <Column header="Id" sortable field="id" style={{ minWidth: '8rem' }} />
      <Column header="Type" sortable field="type" style={{ minWidth: '8rem' }} body={typeBodyTemplate} />
      <Column header="Date" sortable field="date" dataType="date" style={{ minWidth: '8rem' }} body={dateBodyTemplate} />
      <Column header="Upper" sortable field="upper" dataType="numeric" style={{ minWidth: '5rem' }} />
      <Column header="Lower" sortable field="lower" dataType="numeric" style={{ minWidth: '5rem' }} />
      <Column header="Project" sortable field="project" style={{ minWidth: '8rem' }} />
      <Column header="SurveyMethod" sortable field="survey_m_id" style={{ minWidth: '8rem' }} />
      <Column header="Measure" sortable field="value" style={{ minWidth: '10rem' }}  />
      <Column header="UnitOfMeasure" sortable field="unit" style={{ minWidth: '8rem' }}  />
      <Column header="Method" sortable field="method" style={{ minWidth: '8rem' }}  />             
    </DataTable>
  );
};

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}

export default XLSxTable;
