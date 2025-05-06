import { UploadService } from '../../service/uploads';

import { FilterMatchMode, FilterOperator } from 'primereact/api';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { MultiSelect } from 'primereact/multiselect';
import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';
import {useTranslations} from 'next-intl';
import { Toast } from 'primereact/toast';

function List (){
  const t = useTranslations('default');
  const [filters, setFilters] = useState(null);
  const [globalFilterValue, setGlobalFilterValue] = useState('');   
  const [isDeleting, setIsDeleting] = useState(false);
  const [loading, setLoading] = useState(true);
  const [uploads, setUploads] = useState(null);
  const router = useRouter();
  const statuses = ['error', 'succes', 'warning'];
  const toast = useRef(null);

  const goToUpload = (id) => {
    router.push(`/soildata/uploads/${id}`);
  };
  
  const removeUpload = async (id) => {
    /*setIsDeleting(id);
    try {
      const res = await UploadService.remove(id);
      const json = await res.json();
      if (json.errors) {
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting upload', life: 3000});
      }
      else  {
        setUploads((omp) => (omp.filter((p) => p.id !== id)));
        toast.current.show({severity:'success', summary: 'Done!', detail:'Upload has been deleted', life: 3000});
      } 
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setIsDeleting(null);
    }*/
  };

  const clearFilters = () => {
    initFilters();
  };

  const formatDate = (value) => {
    return value.toLocaleDateString('en-US', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
  };

  const initFilters = () => {
    setFilters({
      global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      name: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }]
      },
      user: { value: null, matchMode: FilterMatchMode.IN },
      date: {
          operator: FilterOperator.AND,
          constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }]
      },
      type: {
          operator: FilterOperator.OR,
          constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
      status: {
        operator: FilterOperator.OR,
        constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }]
      },
    });
    setGlobalFilterValue('');
  };

  const userFilterTemplate = (options) => {
      return (
          <>
              <div className="mb-3 text-bold">User Picker</div>
              <MultiSelect value={options.value} options={users} itemTemplate={usersItemTemplate} onChange={(e) => options.filterCallback(e.value)} optionLabel="name" placeholder="Any" className="p-column-filter" />
          </>
      );
  };

  const dateBodyTemplate = (rowData) => {
      return formatDate(rowData.date);
  };

  const dateFilterTemplate = (options) => {
      return <Calendar value={options.value} onChange={(e) => options.filterCallback(e.value, options.index)} dateFormat="mm/dd/yy" placeholder="mm/dd/yyyy" mask="99/99/9999" />;
  };

  const statusBodyTemplate = (rowData) => {
    return <span className={`customer-badge status-${rowData.status}`}>{rowData.status}</span>;
  };

  const statusFilterTemplate = (options) => {
    return <Dropdown value={options.value} options={statuses} onChange={(e) => options.filterCallback(e.value, options.index)} itemTemplate={statusItemTemplate} placeholder="Select a Status" className="p-column-filter" showClear />;
  };

  const statusItemTemplate = (option) => {
    return <span className={`customer-badge status-${option}`}>{option}</span>;
  };
  
  const onGlobalFilterChange = (e) => {
    const value = e.target.value;
    let _filters = { ...filters };
    _filters['global'].value = value;
    setFilters(_filters);
    setGlobalFilterValue(value);
  };

  const renderHeader = () => {
    return (
        <div className="flex justify-content-between">
            <Button outlined icon="pi pi-filter-slash" label="Clear" onClick={clearFilters} />
            <span className="p-input-icon-left">
                <i className="pi pi-search" />
                <InputText value={globalFilterValue} onChange={onGlobalFilterChange} placeholder={t('SEARCH')} />
            </span>
        </div>
    );
  };

  const header = renderHeader();

  useEffect(() => {
    initFilters(); 
    data = [ 

    ]
    setUploads(mapUploadsDate(data));
    //UploadService.getUploads().then((data) => setUploads(mapUploadsDate(data)));
    setLoading(false);
  }, []);

  const mapUploadsDate = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        return d;
    });
  };

  const actionsTemplate = (rowData) => (
    <>
    <Button
      icon="pi pi-times"
      className="p-button-danger p-mb-2 p-mr-2"
      label=""
      loading={isDeleting === rowData.id}
      disabled={isDeleting === rowData.id}
      tooltip={t('DELETE_UPLOAD')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => removeUpload(rowData.id)}
    />
    <Button
      icon="pi pi-folder-open"
      className="p-mr-2 p-mb-2"
      disabled={isDeleting === rowData.id}
      tooltip={t('LOAD_UPLOAD')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => goToUpload(rowData)}
      style={{ width: '160px' }}
      label={t('LOAD_UPLOAD')}
    />
    </> 
  );

  return (
    <div className="layout-dashboard">
      <div className="grid">
        <div className="col-12">
          <div className="card">
            <Toast ref={toast} />
            <h5>Filter Menu</h5>
            <DataTable
                value={uploads}
                paginator
                className="p-datatable-gridlines"
                showGridlines
                rows={10}
                filters={filters}
                filterDisplay="menu"
                loading={loading}
                responsiveLayout="scroll"
                emptyMessage="No customers found."
                header={header}
            >
              <Column field="name" header="Name" filter filterPlaceholder="Search by name" style={{ minWidth: '14rem' }} />
              <Column
                  field="user"
                  header="User"
                  filterField="user"
                  showFilterMatchModes={false}
                  filterMenuStyle={{ width: '14rem' }}
                  style={{ minWidth: '14rem' }}
                  filter
                  filterElement={userFilterTemplate}
              />
              <Column header="Date" filterField="date" dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} filter filterElement={dateFilterTemplate} />
              <Column field="status" header="Status" filterMenuStyle={{ width: '14rem' }} style={{ minWidth: '12rem' }} body={statusBodyTemplate} filter filterElement={statusFilterTemplate} />
              <Column header="Actions" body={actionsTemplate} />
            </DataTable>
          </div>
        </div>
      </div>
    </div>
  );
};

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}

export default List;
