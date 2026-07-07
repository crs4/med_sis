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
import { Fieldset } from 'primereact/fieldset';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import TaxonomyService from '../../service/taxonomies';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../../context/user';


export default function Page( )  {
  
  const [taxonomies, setTaxonomies] = useState(null);
  const [taxonomy, setTaxonomy] = useState(null);
  const [currentCl, setCurrentCl] = useState(null);
  const [currentTx, setCurrentTx] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isWorking, setIsWorking] = useState(false);
  const [visTRemove, setVisTRemove] = useState(false);
  const [visTAdd, setVisTAdd] = useState(false);
  const [visCRemove, setVisCRemove] = useState(false);
  const [visCAdd, setVisCAdd] = useState(false);
  const [newId, setNewId] = useState(null);
  const [newDescr, setNewDescr] = useState(null);
  const [newValue, setNewValue] = useState(null);
  const [newValueDescr, setNewValueDescr] = useState(null);
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  
  const performCreateClass = async () => {
    setVisCAdd(false);
    setIsWorking(true);
    if ( newValue && !isWorking )
      try {
        const newCl = { 
          "id": currentTx.id + ":" + newValue, 
          "value": newValue, 
          "taxonomy": currentTx.id, 
          "descr": newValueDescr,
        }
        const data = await TaxonomyService.createClassification(document.cookie, newCl);
        if (data && data.ok ) { 
          toast.current.show({severity:'success', summary: 'Success!', detail: 'Class has been sent' , life: 3000});
          taxonomy.push(newCl);
          setTaxonomy(taxonomy); 
        } 
        else 
          toast.current.show({severity:'danger', summary: 'Errors saving the data!', detail: msg , life: 3000});
      } catch (error) {
        console.log(e)
        toast.current.show({severity:'danger', summary: 'Errors!', detail: 'System Error!' , life: 3000}); 
      }
    else  
        toast.current.show({severity:'danger', summary: 'Errors saving the data!', detail: msg , life: 3000});
      
    setNewValue(null);
    setNewValueDescr(null);  
    setIsWorking(false)  
  }
  
  /* This creates a new taxonomy */ 
  const performCreate = async () => {
    setVisTAdd(false);
    setIsWorking(true);
    if ( newId && !isWorking )
      try {
        const toAdd = { "id" : newId, descr : newDescr, custom : true }  
        const response = await TaxonomyService.createTaxonomy( document.cookie, toAdd );
        if ( response.ok ) {
          toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy ' + newId + ' has been created', life: 3000});
          taxonomies.push(toAdd)
          setTaxonomies(taxonomies)
          loadTx(toAdd) 
        }
        else 
          toast.current.show({severity:'error', summary: 'Error', detail:'Errors creating the taxonomy', life: 3000});
      } 
      catch (e) { 
        toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
      }
    else 
      toast.current.show({severity:'error', summary: 'Error', detail:'Errors creating the taxonomy', life: 3000}); 
    setNewId(null);
    setNewDescr(null);  
    setIsWorking(false);
  };

  const removeCl = async () => {
    try {
      if ( !currentCl || isWorking )
        return;
      setIsWorking(true)
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
    setCurrentCl(null);
    setIsWorking(false);
    initFilters();   
  };

  const removeTx = async () => {
    try {
      if ( !currentTx || isWorking )
        return;
      setIsWorking(true)
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
    setCurrentTx(null);
    setIsWorking(false);
    initFilters();   
  };

  const loadTx = async (tax) => {
    setCurrentTx(tax);
    setIsWorking(true);
    try {
      setTaxonomy(null);
      if ( !tax || !tax.id )
        return;
      
      const res = await TaxonomyService.listValues(document.cookie, tax.id);
      if ( res.ok  ) {
        setTaxonomy(res.data)
        console.log(res.data)
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy '+ tax.id +' has been loaded', life: 3000});
      } 
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors loading taxonomy', life: 3000});
    } 
    catch (e) { 
      console.log(e)
      toast.current.show({severity:'error', summary: 'Error', detail:'Something went wrong', life: 3000});
    }
    setIsWorking(false);
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

  const headerTemplate1 = () => {
    return  <h5 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}>{t('CREATE_TAXONOMY')}</h5>
  };

  const headerTemplate2 = () => {
    return  <h5 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}>{t('ADD_CLASS')}</h5>
  };
  
  const uriTemplate = (rowData) => {
      return (
        <>
        {( rowData.uri && 
         ( rowData.uri.startWith('https://qudt.org/vocab/') || 
           rowData.uri.startWith('https://glosis-ld.github.io/') ) ) && (
          <div className="flex flex-wrap gap-2">
            <a href={rowData.uri} >
              <Button type="button" icon="pi pi-book" rounded></Button>
            </a>
          </div>
        )}
        </>
      )
  };

  const actionTemplate = (rowData) => {
      return (
        <>
        {( currentTx?.custom ) && (
          <div className="flex flex-wrap gap-2">
            <Button type="button" icon="pi pi-trash" onClick={(e) => { setVisCRemove(true);}} severity="danger" rounded></Button>
          </div>
        )}
        </>
      )
  };

  const transformT  = (text, isValue ) => {
    let t = null;
    try  {
      let m = ( isValue ? text.toLowerCase() : text.toUpperCase() ).match(/\w/g);
      let t = '';
      if ( m )
        m.forEach( (c) => t += c)
      if ( t === '' ) return null
      else return t   
    } catch (error) {
      console.log(error)  
    };
    return null
  };
  
  const rejectDlg1 = () => {
    setVisTRemove(false);
  };

  const rejectDlg2 = () => {
    setVisCRemove(false);
  };

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      <Dialog header={headerTemplate1} visible={visTAdd} style={{ width: '50vw' }} onHide={() => setVisTAdd(false)} >
        <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          <div className="flex flex-column w-full m-2 align-items-center justify-content-center">
            <Fieldset className="flex flex-column gap-2 w-full" legend={t('ID')+', use uppercase characters A-Z, 0-9, _ (underscore) without spaces'}>
              <InputText className="w-30rem" value={newId} 
                      onChange={(e) => { setNewId( transformT(e.target.value, false)); } } />
            </Fieldset>
            <Fieldset className="w-full" legend={t('DESCRIPTION')}>
              <InputTextarea id="description" value={newDescr} onChange={(e) => setNewDescr(e.target.value) }  rows={5} cols={50} />
            </Fieldset>
          </div>  
          <div class="flex flex-row justify-content-center w-full m-3">
            <Button
              label={t('CANCEL')}
              icon='pi pi-trash'
              type='button'
              className='mt-4 flex mr-4'
              onClick={() => { setVisTAdd(false) }}
            />
            <Button
              label={t('SAVE_CHANGES')}
              icon='pi pi-save'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { performCreate() }}
            /> 
          </div>
        </div>    
      </Dialog>  
      <Dialog header={headerTemplate2} visible={visCAdd} style={{ width: '50vw' }} onHide={() => setVisCAdd(false)} >
        <div className="card flex flex-column gap-3 text-cyan-800 w-full align-items-center">
          <div className="flex flex-column w-full m-2 align-items-center justify-content-center">
            <Fieldset className="align-items-center" legend={t('VALUE') + ', use lowercase characters a-z, 0-9, _ (underscore) without spaces'}>
              <InputText className="w-30rem" value={newValue} onChange={(e) => setNewValue(transformT(e.target.value, true)) } />
            </Fieldset>
            <Fieldset className="w-30rem" legend={t('DESCRIPTION')}>
              <InputTextarea id="description" value={newValueDescr} onChange={(e) => setNewValueDescr(e.target.value)}  rows={5} cols={50} />
            </Fieldset>
          </div>  
          <div class="flex flex-row justify-content-center w-full m-3">
            <Button
              label={t('CANCEL')}
              icon='pi pi-trash'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { setVisCAdd(false) }}
            />
            <Button
              label={t('SAVE_CHANGES')}
              icon='pi pi-save'
              type='button'
              disabled={ isWorking }
              className='mt-4 flex mr-4'
              onClick={() => { performCreateClass() }}
            /> 
          </div>
        </div>    
      </Dialog>  
      
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Taxonomies </h4>
      <div className="card text-cyan-800 flex w-full shadow-2 gap-2 flex-row justify-content-center m-2">   
        <Dropdown value={currentTx}  onChange={(e) => loadTx(e.value)} options={taxonomies} loading={loading}
             optionLabel="id" placeholder="Choose the taxonomy" filter filterDelay={400} className="w-full md:w-30rem font-bold text-cyan-800" />
                          
        { currentTx && currentTx.custom && ( 
          <Button type="button" icon="pi pi-trash" onClick={(e) => { setVisTRemove(true); }} severity="danger" rounded></Button>
        )}
        <Button type="button" icon="pi pi-plus" onClick={(e) => { setVisTAdd(true); }} severity="success" rounded></Button>
      </div>
      <ConfirmDialog id="dlg_remove" group="declarative"  visible={visTRemove} onHide={() => setVisTRemove(false)} message={t("DELETE_TAXONOMY_Q")} 
        header="Confirmation" icon="pi pi-exclamation-triangle" accept={removeTx} reject={rejectDlg1} />            
      { currentTx && ( 
      <div className="card text-cyan-800 flex w-full shadow-2 flex-column gap-3 justify-content-center m-2">
        <h5 className="w-full font-bold text-cyan-800 p-3 shadow-2">TAXONOMY: 
          <span className="font-bold text-green-800">{ currentTx?.id}</span>
          {t('LIST_OF_VALUES')}
        </h5>
        <span className="font-italic m-3">{ currentTx?.descr }</span>
        { currentTx && currentTx.custom && ( 
          <Button className="w-15rem m-3" type="button" icon="pi pi-plus" label="Add a new entry" onClick={(e) => { setVisCAdd(true); }} severity="success" rounded></Button>
        )}
        { taxonomy && (
        <DataTable value={taxonomy} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
          <Column body={actionTemplate}  />
          <Column field="id"  header={(<span className='text-xl font-bold'>{t('ID')}</span>)}></Column>
          <Column field="value"  header={(<span className='text-xl font-bold'>{t('CLASS')}</span>)}></Column>
          <Column field="descr"  header={(<span className='text-xl font-bold'>{t('DESCRIPTION')}</span>)}></Column>
          <Column field="uri" body={uriTemplate} header={(<span className='text-xl font-bold'>{t('URI')}</span>)}></Column>
        </DataTable>
        )}
        <ConfirmDialog id="dlg_remove2" group="declarative"  visible={visCRemove} onHide={() => setVisCRemove(false)} message={t("DELETE_ENTRY_Q")} 
          header="Confirmation" icon="pi pi-exclamation-triangle" accept={removeCl} reject={rejectDlg2} />                     
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
