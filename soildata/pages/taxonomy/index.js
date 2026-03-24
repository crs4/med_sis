"use client"

import React, { useState, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';
import { Panel } from 'primereact/panel';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import TaxonomyService from '../../service/taxonomies';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../../context/user';


export default function Page( )  {
  
  const [taxonomies, setTaxonomies] = useState(null);
  const [taxonomy, setTaxonomy] = useState(null);
  const [currentCl, setCurrentCl] = useState(null);
  const [currentTx, setCurrentTx] = useState(null);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(true);
  const [visTRemove, setVisTRemove] = useState(false);
  const [visTAdd, setVisTAdd] = useState(false);
  const [visCRemove, setVisCRemove] = useState(false);
  const [visCAdd, setVisCAdd] = useState(false);
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  
  const saveCl = async () => {
    try {
      if ( !currentCl || working )
          return;
      setWorking(true)
      const data = await TaxonomyService.createClassification(document.cookie,currentCl);
      if (data && data.ok ) { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'Class has been sent' , life: 3000});
      } 
      else { 
        toast.current.show({severity:'danger', summary: 'Errors saving class!', detail: msg , life: 3000});
        let _t = taxonomy.filter((cl) => cl.id !== currentCl.id);
        setTaxonomy(_t) 
      } 
    } catch (error) {
      toast.current.show({severity:'danger', summary: 'Errors!', detail: 'System Error!' , life: 3000}); 
    } finally {
      setWorking(false)
    }
  }
  
  const saveTx = async () => { 
    try {
      if ( !currentTx || working )
          return;
      setWorking(true)
      const data = await TaxonomyService.createTaxonomy(document.cookie,currentTx);
      if (data && data.ok ) { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'Data has been sent' , life: 3000});
      } 
      else { 
        toast.current.show({severity:'danger', summary: 'Errors saving data!', detail: msg , life: 3000});
        let _t = taxonomies.filter((cl) => cl.id !== currentTx.id);
        setTaxonomies(_t) 
      } 
    } catch (error) {
      toast.current.show({severity:'danger', summary: 'Errors!', detail: 'System Error!' , life: 3000}); 
    } finally {
      setWorking(false)
    }
  } 

  const removeCl = async () => {
    try {
      if ( !currentCl || working )
        return;
      setWorking(true)
      const res = await TaxonomyService.deleteClassification(document.cookie, currentCl.id);
      if ( res.ok  ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy class '+id+' has been deleted', life: 3000});
        let _t = taxonomy.filter((cl) => cl.id !== currentCl.id);
        setTaxonomy(_t) 
      } 
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting taxonomy class', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setCurrentCl(null);
      setWorking(false);
    }
    initFilters();   
  };

  const removeTx = async () => {
    try {
      if ( !currentTx || working )
        return;
      setWorking(true)
      const res = await TaxonomyService.deleteTaxonomy(document.cookie, currentTx.id);
      if ( res.ok  ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy class '+id+' has been deleted', life: 3000});
        let _t = taxonomies.filter((tx) => tx.id !== currentTx.id);
        setTaxonomies(_t) 
      } 
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors deleting taxonomy class', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setCurrentTx(null);
      setWorking(false);
    }
    initFilters();   
  };

  const loadTx = async () => {
    try {
      setTaxonomy(null);
      if ( !currentTx || !currentTx.id || working )
        return;
      setWorking(true);
      const res = await TaxonomyService.listValues(document.cookie, currentTx.id);
      if ( res.ok  ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy '+ currentTx.id +' has been loaded', life: 3000});
        setTaxonomy(res.data)
      } 
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors loading taxonomy', life: 3000});
    } 
    catch (e) { 
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    finally {
      setWorking(false);
    }   
  };

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`);
    const fetchData = ( async() => {
      try {
        setLoading(true); 
        let response = await TaxonomyService.list(document.cookie)
        if ( !response || !response.ok )
          toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors loading taxonomies' , life: 3000});
        else if ( response.data && !Array.isArray(response.data) || response.data.length === 0 ) 
          toast.current.show({severity:'warning', summary: 'No data!', detail: 'No data found' , life: 3000});
        else {        
          setTaxonomies(response.data);
        }
      } catch (error) {
        toast.current.show({severity:'danger', summary: 'Errors!', detail: 'System Error!' , life: 3000}); 
      } finally {
        setLoading(false); 
      }
    })
    fetchData();
  }, [user]); // eslint-disable-line   

  useEffect(() => {
    if ( currentTx )
      loadTx();
  }, [currentTx]); // eslint-disable-line 

  const headerTemplate1 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}> CREATE TAXONOMY</h4>
  };

  const headerTemplate2 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}> ADD A CLASS</h4>
  };
  
  const actionTemplate = (rowData) => {
      return (
        <>
        {( rowData ) && (
          <div className="flex flex-wrap gap-2">
            <Button type="button" icon="pi pi-pencil" onClick={(e) => { }} severity="success" rounded></Button>
            <Button type="button" icon="pi pi-trash" onClick={(e) => { }} severity="danger" rounded></Button>
          </div>
        )}
        </>
      )
  };

  const rejectDlg1 = () => {
    
  };

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      <Dialog 
        header={headerTemplate1} 
        visible={visTAdd} style={{ width: '50vw' }} 
        onHide={() => {if (!visTAdd) return; setVisTAdd(false);}}
      >
        Pippo
      </Dialog>  
      <Dialog 
        header={headerTemplate2} 
        visible={visCAdd} style={{ width: '50vw' }} 
        onHide={() => {if (!visCAdd) return; setVisCAdd(false);}}
      >
        Pluto
      </Dialog> 
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Taxonomies </h4>
      <div className="card text-cyan-800 flex w-full shadow-2 gap-2 flex-row justify-content-center m-2">         
        <Dropdown value={currentTx} onChange={(e) => {setCurrentTx(e.value);}} options={taxonomies} optionLabel="id" 
                  placeholder="Choose the taxonomy" className="w-full mr-2 md:w-18rem" virtualScrollerOptions={{ itemSize: 38 }} 
                  loading={loading}
        />
        <Button type="button" icon="pi pi-trash" onClick={(e) => { removeTx(); }} severity="danger" rounded></Button>
        <Button type="button" icon="pi pi-plus" onClick={(e) => { setVisTAdd(true); }} severity="success" rounded></Button>
      </div>
      <ConfirmDialog id="dlg_remove" group="declarative"  visible={visTRemove} onHide={() => setVisTRemove(false)} message="Are you sure you want to delete the taxonomy?" 
        header="Confirmation" icon="pi pi-exclamation-triangle" accept={removeTx} reject={rejectDlg1} />
              
      { currentTx && ( 
      <div className="card text-cyan-800 flex w-full shadow-2 flex-column gap-3 justify-content-center m-2">
        <h5 className="w-full font-bold text-cyan-800 p-3 shadow-2">TAXONOMY: 
          <span className="font-bold text-green-800">{ currentTx?.id}</span>
        </h5>
        <span className="font-italic">{ currentTx?.descr}</span>
        { taxonomy && (
        <DataTable value={taxonomy} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
          <Column body={actionTemplate} headerClassName="w-6rem" />
          <Column field="id" headerClassName="w-8rem" header={(<span className='text-xl font-bold'>{t('ID')}</span>)}></Column>
          <Column field="taxonomy" headerClassName="w-8rem" header={(<span className='text-xl font-bold'>{t('TAXONOMY')}</span>)}></Column>
          <Column field="value" headerClassName="w-6rem" header={(<span className='text-xl font-bold'>{t('CLASS')}</span>)}></Column>
          <Column field="descr" headerClassName="w-10rem" header={(<span className='text-xl font-bold'>{t('DESCRIPTION')}</span>)}></Column>
        </DataTable>
        )}     
      </div>
      )}  
    </div>
    
  );
}

export async function getStaticProps(context) {
  return {
    props: {       
      messages: (await import(`../../translations/${context.locale}.json`)).default
    },
  }
}
