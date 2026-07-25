/* 
PAGE: Hydro Ptf Elaboration

@author Roberto Demontis
2026 CRS4  
*/

"use client"

import  PTFService from '../../service/ptf';
import { Button } from 'primereact/button';
import { Calendar } from 'primereact/calendar';
import { Column } from 'primereact/column';
import { DataTable } from 'primereact/datatable';
import { Dialog } from 'primereact/dialog';
import { Fieldset } from 'primereact/fieldset';
import { FileUpload } from 'primereact/fileupload';
import { Message } from 'primereact/message';
import { InputText } from 'primereact/inputtext';
import { RadioButton } from 'primereact/radiobutton';
import { InputNumber } from 'primereact/inputnumber';
import { ConfirmDialog } from 'primereact/confirmdialog';
import { Ripple } from 'primereact/ripple';
import { Divider  } from 'primereact/divider'; 
import { Panel } from 'primereact/panel'; 
import { Tag } from 'primereact/tag';
import { Checkbox } from 'primereact/checkbox';
import React, { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/router';
import {useTranslations} from 'next-intl';
import { Toast } from 'primereact/toast';
import { useUser } from '../../context/user';
import { validateXLSFilePtfElaboration } from '../../utilities/xls';
import PtfGraph from '../../components/PtfGraph';

export default function Page()  {
  const t = useTranslations('default');
  const router = useRouter();
  const toast = useRef(null);
  const user = useUser();
  // run mode (single or batch)
  const [mode, setMode] = useState('single');
  //Single shot inputs 
  const [organicCarbon, setOrganicCarbon] = useState(null);
  const [clay, setClay] = useState(null);
  const [sand, setSand] = useState(null);
  const [bulkDensity, setBulkDensity] = useState(null);
  const [singleShotResult, setSingleShotResult] = useState(null)
  const [singleShotGraphData, setSingleShotGraphData] = useState(null)
  //Remove Dialog visibility status 
  const [visibleDlgRemove, setVisibleDlgRemove] = useState(false);
  //Batch\Single panels visibility status 
  const [visiblePanelBatch, setVisiblePanelBatch] = useState(false);
  //Batch create dialog visibility status 
  const [visibleCreateDlg, setVisibleCreateDlg] = useState(false);
  //Batch result dialog visibility status 
  const [batchResultVisibility, setBatchResultVisibility] = useState(false);
  //Create batch elaboration help visibility status 
  const [helpVisibility, setHelpVisibility] = useState(false);
  //selected batch elaboration 
  const [current, setCurrent] = useState(null);
  //selected batch elaboration 
  const [currentData, setCurrentData] = useState(null);
  //Loading elaborations status
  const [isLoading, setIsLoading] = useState(true);
  //Working on elaborations status
  const [isWorking, setIsWorking] = useState(false);
  //Set of loaded elaborations 
  const [elaborations, setElaborations] = useState(null);
  //Set the input data for a new elaboration 
  const [inputData, setInputData] = useState(null);
  //Set the title for a new bulk elaboration 
  const [newTitle, setNewTitle] = useState(null);
  const [useBulk, setUseBulk] = useState(false);
  //Message returned by xls file validation 
  const [msg, setMsg] = useState('');
  //XLSx file for a new elaboration
  const [fileId, setFileId] = useState(null);
  //XLSx file ref 
  const xlsxFile = useRef(null);
  //Elaboration Statuses
  const statuses = PTFService.HYDRO_PTF_ELABORATION_STATUSES;
  
  // fetch list of elaborations
  const fetchData = async() => {
    setIsLoading(true);
    try {
      let _data = await PTFService.list(document.cookie)
      if ( !_data || _data.error )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading PTF batch elaborations' , life: 3000});
      else if ( !_data.data || !Array.isArray(_data.data) || _data.data.length === 0 ) 
        toast.current.show({severity:'warn', summary: 'No data!', detail: 'No batch elaborations Found' , life: 3000});
      else { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'Batch elaborations list has been loaded' , life: 3000});
        setElaborations(mapElaborations(_data.data));
      }
    } catch (error) {
      console.log(error)
    }
    setIsLoading(false);
  }

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
      router.push(`/401`); 
    fetchData();
  },[user]);  // eslint-disable-line
  
  useEffect(() => {
    ( mode === 'single' ) ? openSingleShot() : openBatch()
  },[mode]); // eslint-disable-line

  // download result in CSV format
  const DownloadBatchCSV = () => {
    if ( !currentData || !currentData.output_data )
      return
    let dataStr = "CLAY,SAND,OC,BD,Pot,Gravimetric,Volumetric" + '\n'
    currentData.output_data.forEach( elem => {
        dataStr += ( elem.CLAY? elem.CLAY : '' ) + ','
        dataStr += ( elem.SAND? elem.SAND : '' ) + ','
        dataStr += ( elem.OC? elem.OC : '' ) + ','
        dataStr += ( elem.BD? elem.BD : '' ) + ','
        dataStr += ( elem.Pot? elem.Pot : '' ) + ','
        dataStr += ( elem.Gravimetric? elem.Gravimetric : '' ) + ','
        dataStr += ( elem.Volumetric? elem.Volumetric : '' ) 
        dataStr += '\n'
    })
    const csvStr =
      'data:text/csv;charset=utf-8,' +
      encodeURIComponent(dataStr);
    const download = document.createElement('a');
    download.setAttribute('href', csvStr);
    download.setAttribute('download', 'result' + '.csv');
    document.body.appendChild(download);
    download.click();
    download.remove();  
  };

  const openBachResultDlg = async (id) => {
    if (!id)
      return
    //// load output_data
    setIsWorking(true);
    try {
      let _data = await PTFService.get(document.cookie,id)
      if ( !_data || !_data.ok )
        return
      setCurrent(id)
      setCurrentData(_data.data)
    } catch (error) {
      console.log(error)
    }
    setIsWorking(false)
    setBatchResultVisibility(true);
  };

  // validate input data
  const validateOrganicCarbon = (v) => { 
    setOrganicCarbon( (v<0)? 0 : ( (v>100)? 100 : v )  ); 
  };

  // validate input data
  const validateClay = (v) => { 
    setClay( (v<0)? 0 : ( (v>100)? 100 : (v+sand>100 )? 100-sand: v )  ); 
  };

  // validate input data
  const validateBulkDensity = (v) => { 
    setBulkDensity( (v<0)? 0 :  v ); 
  };

  // validate input data
  const validateSand = (v) => { 
    setSand( (v<0)? 0 : ( (v>100)? 100 : (v+clay>100 )? 100-clay: v )  ); 
  };

  // Open SingleShot Panel
  const openSingleShot =  () => {
    resetData();
    setVisiblePanelBatch(false);
  };

  // Open SingleShot Panel
  const openBatch =  () => {
    setVisiblePanelBatch(true);
  };

  // Initial configuration of a new bulk elaboration 
  const generateElaboration = () => {
    if ( !inputData )
      return null
    const nowd = formatDate(Date.now())
    return {
      title : newTitle,
      date : nowd,
      useBulkDensity : useBulk,
      input_data : inputData, 
      status : statuses.CREATED,
    }
  };
  
  // It creates a new elaboration 
  const performCreate = async () => {
    if ( !inputData )
      return;
    setVisibleCreateDlg(false);
    try {  
      setIsWorking(true)
      const res = await PTFService.create(document.cookie, generateElaboration());
      if ( res.status < 200 && res.status > 299 ) 
        toast.current.show({severity:'Error', summary: 'Error', detail:'Errors initialising HydroPTF Bulk Elaboration', life: 3000});
      else  {
        toast.current.show({severity:'success', summary: 'Done!', detail:'New HydroPTF Bulk Elaboration has been created', life: 3000});
        const res2 = await PTFService.update(document.cookie, res.data.id, res.data );
        await fetchData()
      }
      setIsWorking(false); 
    } catch (error) {
      console.log(error)
    }
    resetData();
  }; 

  const resetData = () => {
    setInputData(null);
    setFileId(null);
    xlsxFile.current?.clear();
  }; 

  // Open remove dialog 
  const openRemove = async (id) => {
    if ( !id || current )
      return;
    setCurrent(id);
    setVisibleDlgRemove(true);
  };

  // It removes selected elaboration 
  const performRemove = async () => {
    if ( !current )
      return;
    setIsWorking(true);
    try {  
      const res = await PTFService.remove(document.cookie,current);
      if ( res.status != 204 && res.status != 202 && res.status != 203 ) {
          toast.current.show({severity:'Error', summary: 'Error', detail:'Errors deleting Hydro PTF elaboration ' + current, life: 3000});
      }
      else  {
          setElaborations((omp) => (omp.filter((p) => p.id !== current)));
          toast.current.show({severity:'success', summary: 'Done!', detail:'Hydro PTF Elaboration ' + current +' has been deleted', life: 3000});
      } 
      setCurrent(null);
      
    } catch (error) {
      console.log(error)  
    }
    setIsWorking(false);
    setVisibleDlgRemove(false)
  }; 
  
  // Cancel remove
  const rejectDlgRemove = () => {
    setCurrent(null);
  };

  const resetSingleShot = async () => {
    setClay(null);
    setOrganicCarbon(null);
    setSand(null);
    setBulkDensity(null);
    setSingleShotResult(null)
  }; 
  
  // It creates a new elaboration 
  const performSingleShot = async () => {
    if ( !clay || !sand || !organicCarbon )
      return;
    const payload = { "sand": sand , "clay": clay, "org_car": organicCarbon, "bulk_density": bulkDensity };
    try {  
      setIsWorking(true)
      const res = await PTFService.postSingleShot(document.cookie, payload);
      setIsWorking(false);
      if ( res.status === 400  ) 
        toast.current.show({severity:'Error', summary: 'Error', detail:'Errors wrong parameters', life: 3000});
      else if ( res.status === 500 ) 
        toast.current.show({severity:'Error', summary: 'Error', detail:'Errors running the model', life: 3000});
      else if ( res.status === 200 ) {
        if ( res.data.result && res.data.result.columns && res.data.result.data ) { 
          const results = []
          const columns = res.data.result.columns 
          const rows = res.data.result.data 
          rows.forEach( row => {
            const r = { }
            for ( let i = 0; i < row.length; i++ ) {
              if ( isNaN(Number.parseFloat(row[i])) )  
                r[columns[i]] = null
              else {
                const value = Number.parseFloat(Number.parseFloat(row[i]).toFixed(3))
                if ( i === 3 )
                  r[columns[i]] = -value
                else r[columns[i]] = value
              }
            }
            results.push(r)
          });
          setSingleShotResult(results)
          setSingleShotGraphData(generatePtfGraphData(results))
        }
        toast.current.show({severity:'success', summary: 'Done!', detail:'Hydro PTF model runned', life: 3000});
      } 
    } catch (error) {
      console.log(error)
    }
  }; 

  const generatePtfGraphData = (data) => {
    if ( data ) {
      const points = []
      const max = 0;
      data.forEach((elem) => {
        points.push ( { x: -elem.Pot , y: elem.Volumetric } )
        if ( max < elem.Volumetric )
          max = elem.Volumetric
      });
      if ( max > 0 )
        return { pts: points, max: max }  
    }
    return null    
  };
  
  // Validate XLXx file with input data
  const validateFile = async (files) => {
    if ( files && files[0] )
    try {
      let msg = 'Errors in file!'
      setFileId(files[0].name);
      // validate file in utils/ptf.js
      setIsWorking(true);
      const result = await validateXLSFilePtfElaboration ( files[0], useBulk );
      setIsWorking(false);
      if ( result && result.data ){
        setInputData(result.data)
        toast.current.show({severity:'success', summary: 'Validated!', detail:'The file has been validated!', life: 4000});
        return true;
      }
    } catch (error) {
      console.log(error) 
      resetData()
    }
    toast.current.show({severity:'error', summary: 'Errors in file!', detail:'wrong file!', life: 4000});
    return false 
  }

  const formatDate = (value) => {
    const date = new Date(value) 
    return (date.toISOString()).substring(0,10);
  };

  const dateBodyTemplate = (rowData) => {
      return formatDate(new Date(rowData.date));
  };

  const statusBodyTemplate = (rowData) => {
    if ( rowData.status === statuses.SUCCESS )
      return ( <Tag icon="pi pi-check" severity="success" value="Elaborated"></Tag>)
    else if ( rowData.status === statuses.IN_PROCESS )
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Elaborating"></Tag>)
    else if ( rowData.status === statuses.CREATED )
      return ( <Tag icon="pi pi-spin pi-cog" severity="info" value="Waiting Elaboration"></Tag>)
    else if ( rowData.status === statuses.ERRORS )
      return ( <Tag icon="pi pi-exclamation-triangle" severity="danger" value="Critical error"></Tag>)
  };

  // manage dates 
  const mapElaborations = (data) => {
    return [...(data || [])].map((d) => {
        d.date = new Date(d.date);
        return d;
    });
  };

  const actionsTemplate = (rowData) => (
    <>     
    <Button
      icon="pi pi-times"
      className="p-button-danger p-mb-2 p-mr-2 m-1"
      label=""
      disabled={isWorking}
      tooltip={t('PTF_DELETE_ELABORATION')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => openRemove(rowData.id) }
      aria-controls={visibleDlgRemove ? 'dlg_remove' : null} 
      aria-expanded={visibleDlgRemove ? true : false}
    />
    {( rowData.status === statuses.SUCCESS ) && (
    <Button
      icon="pi pi-folder-open"
      className="p-mr-2 p-mb-2 m-1"
      disabled={isWorking}
      tooltip={t('PTF_SHOW_BACH_RESULT')}
      tooltipOptions={{ position: 'top' }}
      onClick={() => openBachResultDlg(rowData.id)}
      label=""
    />
    )}
    </> 
  );

  // Templates for the resultss table 
  const renderHeaderSingle = (
        <div className="flex justify-content-between">
          <Button 
            icon="pi pi-download"
            className="flex bg-primary w-20rem font-bold border-round"
            onClick={() => { DownloadCSV({ singleShotResult }) }}
            label={t('DOWNLOAD')}
          />
        </div>
  );

  // Templates for the resultss table 
  const renderHeaderBatch = (
    <div className="flex justify-content-between">
          <Button 
            icon="pi pi-download"
            className="flex bg-primary w-20rem font-bold border-round"
            onClick={() => { DownloadBatchCSV() }}
            label={t('DOWNLOAD')}
          />
    </div>
  );

  const headerSingle = (
    <h5 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('PTF_ELABORATION_SINGLE')}</h5>
  );

  const headerBatch = (
    <div className="w-full surface-200 p-3 mb-3 shadow-2 flex flex-row gap-2">
      <h5 className="font-bold text-cyan-800 m-2">{t('PTF_ELABORATIONS_LIST')}</h5>
    </div>
  );

  const headerResult = (
    <h5 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}>{t('PTF_BATCH_ELABORATION_RESULT')}</h5>
  )

  const headerCreate = (
    <h5 className="w-10 surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t('PTF_ELABORATION_BATCH_NEW')}</h5>
  );

  const DownloadCSV = (data) => {
    let dataStr = "CLAY,SAND,OC,BD,Pot,Gravimetric,Volumetric" + '\n'
    //for ( let i =0; i < data.length; i+=1 ) {   
    //    const elem = data[i]
    data.singleShotResult.forEach( elem => {
        dataStr += ( elem.CLAY? elem.CLAY : '' ) + ','
        dataStr += ( elem.SAND? elem.SAND : '' ) + ','
        dataStr += ( elem.OC? elem.OC : '' ) + ','
        dataStr += ( elem.BD? elem.BD : '' ) + ','
        dataStr += ( elem.Pot? elem.Pot : '' ) + ','
        dataStr += ( elem.Gravimetric? elem.Gravimetric : '' ) + ','
        dataStr += ( elem.Volumetric? elem.Volumetric : '' ) 
        dataStr += '\n'
    })
    const csvStr =
      'data:text/csv;charset=utf-8,' +
      encodeURIComponent(dataStr);
    const download = document.createElement('a');
    download.setAttribute('href', csvStr);
    download.setAttribute('download', 'result' + '.csv');
    document.body.appendChild(download);
    download.click();
    download.remove();
  };

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">Hydro PTF4MED</h4>
      <Dialog header={headerResult} visible={batchResultVisibility} style={{ width: '50vw' }} onHide={() => setBatchResultVisibility(false)} >
        <div className="card flex flex-column align-items-center">
          <DataTable
              value={currentData?.output_data}
              className="p-datatable-gridlines"
              showGridlines
              disabled={isWorking}
              responsiveLayout="scroll"
              emptyMessage="No results"
              header={renderHeaderBatch}
          >
            <Column header={t("Identifier")} field="Sample_id" sortable />
            <Column header={t("PTF_SAND")} field="SAND" sortable />
            <Column header={t("PTF_CLAY")} field="CLAY" sortable/>
            <Column header={t("PTF_OC")} field="OC" sortable/>
            <Column header={t("PTF_BULK")} field="BD" sortable/>
            <Column header={t("PTF_POT")} field="Pot" sortable/>
            <Column header={t("PTF_GRAVIMETRIC")} field="Gravimetric" sortable />
            <Column header={t("PTF_VOLUMETRIC")} field="Volumetric" sortable />
          </DataTable>
        </div>    
      </Dialog> 
      <div className="card text-lg text-cyan-800">
        <p><span className="font-bold">HydroPTF4MED</span> 
            is the first basin-scale pseudo-continuous pedotransfer function specifically
            developed for the Mediterranean region.</p>
        <p> It integrates harmonized legacy soil datasets from multiple countries of the Soils4Med project.</p> 
        <p> HydroPTF4MED is a screening tool based on harmonized legacy datasets. It does not replace site-specific laboratory
            measurements or locally calibrated PTFs. Extrapolation beyond the calibration range
            (ψ 4..1500 kPa; Mediterranean pedoclimatic domain) is not recommended.</p>
        <p className="font-italic">Giacomo Belvisi ( email: giacomo.belvisi@unipa.it )</p> 
        <p>Belvisi G., Iovino M., Gristina L., Al-Bakri J.T., Triantakonstantis D., Zucca C., Scalenghe R. (2026). 
        <span className="font-italic"> TITOLO PAPER.</span> - Under review at NAME .</p> 
        <Divider type="solid" />
        <div className="card flex flex-column gap-2 font-bold m-3 text-blue-800">
          On this page, you can run the model for :
          <div className="font-bold font-italic m-2">
            <RadioButton inputId="single" value="single" name="mode" onChange={(e) => setMode(e.value)} checked={mode === 'single'} />
            <label htmlFor="single" className=" ml-2">A Single record by providing data on sand, clay, and organic carbon and optionally the bulk density</label> 
          </div>
          <div className="font-bold font-italic m-2">
            <RadioButton inputId="batch" value="batch" name="mode" onChange={(e) => setMode(e.value)} checked={mode === 'batch'} />
            <label htmlFor="batch" className=" ml-2">Multiple records using an XLSX file</label> 
          </div>  
        </div>
        <Divider type="solid" />
      </div>     
      { !visiblePanelBatch && (
        <Panel  header={headerSingle} className="surface-200 w-full font-bold text-cyan-800" >
          <div className="card flex flex-column gap-2 w-full align-items-center justify-content-center">
            <div className="card flex flex-row gap-2 w-full justify-content-center">
              <Fieldset legend={t('PTF_CLAY')}>
                <InputNumber useGrouping={false} maxFractionDigits={3} min={0} max={100} value={clay} 
                  onChange={(e) => { validateClay( e.value ); } } />
              </Fieldset>
              <Fieldset legend={t('PTF_SAND')}>
                <InputNumber useGrouping={false} maxFractionDigits={3} min={0} max={100} value={sand} 
                  onChange={(e) => { validateSand( e.value ); } } />
              </Fieldset>
              <Fieldset legend={t('PTF_OC')}>
                <InputNumber useGrouping={false} maxFractionDigits={3} min={0} max={100} value={organicCarbon} 
                  onChange={(e) => { validateOrganicCarbon( e.value ); } } />
              </Fieldset>
              <Fieldset legend={t('PTF_BULK')}>
                <InputNumber useGrouping={false} maxFractionDigits={8} min={0} value={bulkDensity} 
                  onChange={(e) => { validateBulkDensity( e.value ); } } />
              </Fieldset>
            </div>
            
            <Button 
              icon="pi pi-wrench"
              className="flex bg-primary w-20rem font-bold border-round"
              disabled={isWorking}
              onClick={() => performSingleShot()}
              label={t('PTF_ELABORATE')}
            />
          </div>
          { singleShotResult && (
          <div>
            { singleShotGraphData && (
              <PtfGraph data={singleShotGraphData} />
            )} 
            <div className="card m-3 flex flex-columns w-full font-bold text-cyan-800">
              <h4 className="m-3">{t('FIELD_CAPACITY')}: <span className="text-green-800">{singleShotResult[2].Volumetric}</span></h4>
              <h4 className="m-3">{t('WILTING_POINT')}: <span className="text-green-800">{singleShotResult[6].Volumetric}</span></h4>
              <h4 className="m-3">{t('AWC')}: <span className="text-green-800">{ Number.parseFloat(Number.parseFloat(singleShotResult[2].Volumetric - singleShotResult[6].Volumetric).toFixed(3))}</span></h4>
            </div>
            <DataTable
              value={singleShotResult}
              className="p-datatable-gridlines"
              showGridlines
              disabled={isWorking}
              responsiveLayout="scroll"
              emptyMessage="No results"
              header={renderHeader}
            >
              <Column header={t("PTF_SAND")} field="SAND"  />
              <Column header={t("PTF_CLAY")} field="CLAY"  />
              <Column header={t("PTF_OC")} field="OC"  />
              <Column header={t("PTF_BULK")} field="BD"  />
              <Column header={t("PTF_POT")} field="Pot"  />
              <Column header={t("PTF_GRAVIMETRIC")} field="Gravimetric"  />
              <Column header={t("PTF_VOLUMETRIC")} field="Volumetric"  />
            </DataTable>
            
          </div>
          )}
        </Panel>
      )}   
      { visiblePanelBatch && (
        <>
        { !isLoading && (
        <>
        <Dialog header={headerCreate} visible={visibleCreateDlg} style={{ width: '50vw' }} onHide={() => setVisibleCreateDlg(false)} >
          <div className="card flex flex-column gap-2 w-full justify-content-center">
            <Fieldset className="flex flex-column gap-2 w-full" legend={t('TITLE')}>
              <InputText className="w-30rem" value={newTitle} placeholder={ t('TITLE_INSERT')}
                  onChange={(e) => { setNewTitle( e.target.value ); } } />
            </Fieldset>
            <Fieldset className="flex flex-column gap-2 w-full" legend={t('PTF_USE_BULK')}>
              <Checkbox inputId="useBulk" onChange={e => setUseBulk(e.checked)} checked={useBulk}></Checkbox>
              <label htmlFor="useBulk" className="ml-2 font-bold text-orange-900">Warning! if set the bulk density should be present in input data</label>
            </Fieldset>
            {(fileId === null) && (
            <>  
            <div class="flex flex-row gap-2 mt-4">
                <FileUpload 
                  disabled={fileId !== null || isWorking}
                  id="file"
                  ref={xlsxFile}
                  accept='.xlsx'
                  chooseLabel={t('CHOOSE_FILE')}
                  mode="basic"
                  multiple={false}
                  customUpload
                  auto
                  className='mb-4 mr-2 mt-4'
                  uploadHandler={(e) => validateFile(e.files)}
                />
                <Button 
                  icon="pi pi-question"
                  className="p-button-icon p-button-rounded mt-4"
                  disabled={isWorking}
                  onClick={() => setHelpVisibility(!helpVisibility)}
                />
            </div> 
            { helpVisibility && (
              <div className="card flex flex-column gap-2 items-align-center" >
                <Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text='This form permits to upload Hydro PTF XLSx input data for the new batch elaboration' />
                <Message className="p-inline-message p-component p-inline-message-error font-bold block" severity="error" text='!WARNING Formatted text and formulas are not allowed.'/>
                <a href="/static/doc/ptf_input_data.xlsx" target="_blank">
                <Button
                  label="Download the XLSx template" 
                />
                </a>   
              </div> 
            )}
            </> 
            )}
            {(fileId !== null) && ( 
              <div class="mt-4">
                <Button severity="success" outlined label={'File: ' + fileId} className='m-2 font-bold text-cyan-900' disabled /> 
                <Button
                      label={t('RESET')}
                      icon='pi pi-plus'
                      type='button'
                      disabled={isWorking}
                      className='m-2'
                      onClick={() => { resetData(); }}
                />
                <Button 
                      label={t('PTF_CREATE_ELABORATION')} 
                      icon="pi pi-save"
                      type="button" className="m-2"   
                      disabled={(inputData === null)} 
                      onClick={(e) => performCreate()}
                />
              </div>  
            )}
          </div>
        </Dialog>       
        <Panel  header={headerBatch} className="surface-200 w-full font-bold text-cyan-800" >  
          <ConfirmDialog id="dlg_remove" group="declarative"  visible={visibleDlgRemove} onHide={() => setVisibleDlgRemove(false)} message="Are you sure you want to delete Hydro PTF batch elaboration?" 
            header="Confirmation" icon="pi pi-exclamation-triangle" accept={performRemove} reject={rejectDlgRemove} />
          <div className="card flex flex-row  m-4"> 
            <Button icon="pi pi-plus" className="m-2" label={t('PTF_ELABORATION_BATCH_NEW')} disabled={isWorking}
              onClick={() => setVisibleCreateDlg(true)}
            />
            <Button icon="pi pi-replay" className="m-2" label={t('REFRESH_LIST')} disabled={isWorking}
              onClick={() => fetchData()}
            />
          </div>
          <DataTable
            value={elaborations}
            paginator
            dataKey="id"
            className="p-datatable-gridlines"
            showGridlines
            rows={20}
            disabled={isWorking}
            responsiveLayout="scroll"
            emptyMessage="No batch elaborations found."
          >
            <Column header="Identifier" field="id" sortable style={{ minWidth: '4rem' }} />
            <Column header="Name" field="title" sortable style={{ minWidth: '14rem' }} />
            <Column header="Date"  field="date" sortable dataType="date" style={{ minWidth: '10rem' }} body={dateBodyTemplate} />
            <Column header="Status"  field="status" sortable style={{ minWidth: '12rem' }} body={statusBodyTemplate} />
            <Column header="Actions" body={actionsTemplate} style={{ minWidth: '10rem' }} />
          </DataTable>
        </Panel>
        </>
        )}
        { isLoading && (
          <h6 className="font-bold text-cyan-800">Loading Hydro PTF batch elaborations list...</h6>
        )}
      </>
      )}
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
