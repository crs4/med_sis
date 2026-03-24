"use client"

import React, { useState, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import TaxonomyService from '../../service/taxonomies';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../../context/user';


export default function Page( )  {
  
  const [taxonomies, setTaxonomies] = useState(null);
  const [taxonomy, setTaxonomy] = useState(null);
  const [taxonomyName, setTaxonomyName] = useState(null);
  const [currentCl, setCurrentCl] = useState(null);
  const [currentTx, setCurrentTx] = useState(null);
  const [loading, setLoading] = useState(true);
  const [working, setWorking] = useState(true);
  const [visDlgTRemove, setVisTRemove] = useState(false);
  const [visDlgTAdd, setVisDlgTAdd] = useState(false);
  const [visDlgCRemove, setVisCRemove] = useState(false);
  const [visDlgCAdd, setVisDlgCAdd] = useState(false);
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  
  const saveCl = async () => {
    try {
      if ( !currentCl || working )
          return;
      setWorking(true)
      const data = await TaxonomyService.save(document.cookie,currentCl);
      if (data && data.ok ) { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'Data has been sent' , life: 3000});
      } 
      else { 
        toast.current.show({severity:'danger', summary: 'Errors saving data!', detail: msg , life: 3000});
        let _t = taxonomies.filter((cl) => cl.id === currentCl.id);
        setTaxonomies(_t) 
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
      const data = await TaxonomyService.save(document.cookie,currentTx);
      if (data && data.ok ) { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'Data has been sent' , life: 3000});
      } 
      else { 
        toast.current.show({severity:'danger', summary: 'Errors saving data!', detail: msg , life: 3000});
        let _t = taxonomies.filter((cl) => cl.id === currentTx.id);
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
      const res = await TaxonomyService.removeCl(document.cookie, currentCl.id);
      if ( res.ok  ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy class '+id+' has been deleted', life: 3000});
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
      const res = await TaxonomyService.remove(document.cookie, currentTx.id);
      if ( res.ok  ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy class '+id+' has been deleted', life: 3000});
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

  const loadTx = async (name) => {
    try {
      if ( !name || working )
        return;
      setWorking(true)
      const res = await TaxonomyService.get(document.cookie, name);
      if ( res.ok  ) {
        toast.current.show({severity:'success', summary: 'Done!', detail:'Taxonomy '+ name +' has been loaded', life: 3000});
      } 
      else 
        toast.current.show({severity:'error', summary: 'Error', detail:'Errors creating taxonomy', life: 3000});
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
        if ( !response || !response.data )
          toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors loading taxonomies' , life: 3000});
        else if ( !Array.isArray(response.data) || response.data.length === 0 ) 
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

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      <Dialog 
        header="Create a new taxonomy" 
        visible={visDlgTAdd} style={{ width: '50vw' }} 
        onHide={() => {if (!visDlgTAdd) return; setVisDlgTAdd(false);}}
      >
      </Dialog>  
      <Dialog 
        header="Create a new taxonomy" 
        visible={visDlgTAdd} style={{ width: '50vw' }} 
        onHide={() => {if (!visDlgTAdd) return; setVisDlgTAdd(false);}}
      >
      </Dialog>          
      <div className="card">
        <div class="flex flex-row justify-content-center mt-4">
          <Dropdown value={currentTx} onChange={(e) => setCurrentTx(e.value)} options={taxonomies} optionLabel="name" 
                    placeholder="Choose the taxonomy" className="w-full mr-2 md:w-14rem" 
                    loading={loading}
          />
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold"
                onClick={() => true} 
                aria-controls={visDlgTRemove ? 'dialog to remove taxonomy' : null} 
                aria-expanded={visDlgTRemove ? true : false} >
          </Button> 
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold"
                onClick={() => false}
                aria-controls={visDlgTAdd ? 'dialog to add taxonomy' : null} 
                aria-expanded={visDlgTAdd ? true : false} >
          </Button>
        </div>
      </div> 
      { currentTx && ( 
        <div className="card">  
          <div class="flex flex-row mt-4">
            <span class="font-bold text-lg">Taxonomy name:&nbsp;</span> <span class="font-bold text-lg text-blue-500"> { currentTx?.name }</span>
          </div>     
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
