"use client"

import { point, featureCollection } from '@turf/turf';
import React, { useState, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';

import { Badge } from 'primereact/badge';
import { Tag } from 'primereact/tag';
import { FileUpload } from 'primereact/fileupload';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import Taxonomies from '../../data/taxonomies';
import Mapping from '../../data/mapping';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import { useUser } from '../../context/user';
import { UploadService } from '../../service/uploads';
import { createObjects, validateXLSFile } from '../../utilities/XLSxUtils';
import ReportTable from '../../components/XLSxTable';
import dynamic from "next/dynamic"

const MyMap = dynamic(() => import("../../components/XLSxMap"), { ssr:false })

export default function Page( )  {
  
  const [upload, setUpload] = useState(null);
  const [uploadType, setUploadType] = useState(null);
  const [uploadAction, setUploadAction] = useState(null);
  const [visibleDlg1, setVisibleDlg1] = useState(false);
  const [visibleDlg2, setVisibleDlg2] = useState(false);
  const [map, setMap] = useState(null);
  const [validated, setValidated] = useState(0);
  const [validating, setValidating] = useState(false);
  const [uploaded, setUploaded] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [pointsGeoJSON, setPointsGeoJSON] = useState(null);
  const [fileId, setFileId] = useState(null);
  const user = useUser();
  const xlsxFile = useRef(null);
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  
  
  function createPopupContent (code, result) {
      let panel = '<div><span class="font-bold">No data</span></div>';
      if ( !result || !code )
        return panel;
      try {
        panel = '<div class="flex flex-wrap  justify-content-center">';
        panel += '<span class="text-cyan-500 align-items-center font-bold" >Profile:</span><span> '+code+'</span></div>';
        let keys = Object.keys(result);
        let values;
        let v;
        keys.forEach( (key) => {
          if ( result[key] ) {
            panel += '<div><span class="text-blue-500 font-bold ">'+key+'</span>:';
            if ( key != 'wrong' && result[key]) {
              values = result[key].split(':');
              if ( values.length === 2 && values[0] && values[1] ) {
                v = Math.floor(values[0]);
                panel += '<span class="font-bold"> Filled: </span>';
                panel += '<span class="font-bold text-green-500"> ' + v + '%</span>';
                panel += '<span class="font-bold"> Errors: </span>';
                panel += '<span class="font-bold text-orange-600"> ' + values[1] + '</span>';
              }  
              else panel += '<span class="font-bold">' + result[key] + '</span>';
              
            } 
            panel += '</div>'; 
          }
        });
      } catch (e) {
        console.log(e);
      }
      return panel;  
  }

  const createGeoJSON = ( data_sheets, data_report ) => {
    const sheetname = UploadService.TYPES[upload.type].sheets[0]
    const data_sheet = data_sheets[ sheetname ]
    if (!data_sheet || !data_report ) 
      return; 
    let j;
    let points = [];
    const results = data_report['tree'];
    if ( !results ) //// wrong data
      return;
    for ( j=1; j<data_sheet.length; j+=1 ){
/// skip row with null or errors in lat,lon or key
      try {
        if ( data_sheet[j] && data_sheet[j][1] && 
             data_sheet[j][6] && data_sheet[j][7] &&
             data_sheet[j][6] < 90 && data_sheet[j][6] > -90 &&
             data_sheet[j][7] < 180 && data_sheet[j][7] > -180
        ){
          const key = data_sheet[j][1];
          let status = 'warn'
          if ( !results[key] || results[key]['wrong'] === 0) 
                status = 'ok';
          else  status = 'ko';
          points.push( point( [data_sheet[j][7] , data_sheet[j][6]], 
                      { key: key, status: status, popupContent : createPopupContent( key, results[key])  },
                      { id: key } ) );
        }
      } catch (e) {
        console.log(e);
      }
    }
    if ( points.length > 0 ) {
      setPointsGeoJSON( featureCollection(points));
      toast.current.show({severity:'success', summary: 'GeoJSON created!', detail:'GeoJSON for geo points created', life: 3000});
    }  
  } 

  const validateFile = async (files) => {
    if ( !upload )
      return 
    
    if ( !files || !files[0]  ){
      toast.current.show({severity:'error', summary: 'Error!', detail:'Wrong file!', life: 3000});
      return;
    }
    setValidating(true);
    setFileId(files[0].name);
    let result = await validateXLSFile (files,upload.type);
    if ( result  ){ 
      setValidated(result['validated'])
      if  ( result['data'] && result['report'] ) {
        const _data = createObjects(result['data'],upload.type)
        upload.data = JSON.stringify(_data);
        upload.report = result['report'] 
        try { 
          if ( upload.type === UploadService.TYPES['XLS_P'].name || upload.type === UploadService.TYPES['XLS_S'].name )
            createGeoJSON ( result['data'], result['report'] );
        } catch (e) {
          console.log(e);
          toast.current.show({severity:'error', summary: 'Errors generating points!', detail:'Map points not created!', life: 3000});
        }
      }
    }
    else { 
      toast.current.show({severity:'error', summary: 'Errors in file!', detail:'wrong file or sheets!', life: 3000});
      setValidating(false);
      return;
    }
    setValidating(false);
  }

  const saveData = async () => {
    try {
      if ( !upload || !uploading )
          return;
      upload.report = {}
      upload.editor = user.userData.preferred_username
      const data = await UploadService.save(document.cookie,upload);
      if (data && data.ok ) { 
        toast.current.show({severity:'success', summary: 'Success!', detail: 'Data has been sent' , life: 3000});
        setTimeout(() => {
          router.push('/uploads') 
        }, 3000);
      } 
      else { 
        let msg = 'Errors saving data'
        if ( data && data.msg )
          msg = data.msg
        toast.current.show({severity:'error', summary: 'Errors!', detail: msg , life: 3000});
      } 

    } catch (error) {
      toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors sending data' , life: 3000}); 
    } finally {
      setUploaded(true);
      setUploading(false);
    }
  } 
  
  let reportHeaders = ['Element', 'Row', 'Column', 'Error'];

  const resetData = () => {
    setMap(null);
    setUpload(null);
    setValidated(0);
    setPointsGeoJSON(null);
    setUploaded(false);
    setUploading(false);
    setFileId(null);
    xlsxFile.current?.clear();
  }; 
  
  const showTypeInfo = async () => {
    setVisibleDlg1(true);
  };

  const showActionInfo = async () => {
    setVisibleDlg2(true);
  };
  useEffect(() => {
      if ( uploading )
        saveData();
    },[uploading]);  // eslint-disable-line

  useEffect(() => {
      if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 )
          router.push(`/401`);
      
    },[user]);  // eslint-disable-line

  useEffect(() => {
    const today = new Date();
    if (!upload && uploadType && uploadAction) {
      setUpload ({
        date : today,
        title : uploadType.label+' upload - ' + today.toDateString(),
        type: uploadType.name,
        data: {},
        report: {},
        status: UploadService.STATUSES.UPLOADED,
        operation: uploadAction.name
      })
    } 
    else if ( upload && uploadType ) {
      upload.type = uploadType.name; 
      upload.title = uploadType.label+' '+today.toDateString();   
    }  
  },[upload, uploadType, uploadAction]);

  useEffect(() => {
    const fetchMap = async () => {
      if ( pointsGeoJSON ) {
        const uploadMap = {
          layer : {
            points: pointsGeoJSON,
            styles: {
              'ok' : { radius: 8, fillColor: '#2f2', color: '#0d0', weight: 2, opacity: 1, fillOpacity: 0.8, },
              'ko' : { radius: 8, fillColor: '#f22', color: '#d22', weight: 2, opacity: 1, fillOpacity: 0.8, },
              'warn' : { radius: 8, fillColor: '#f80', color: '#d60', weight: 2, opacity: 1, fillOpacity: 0.8, },
            },
          },
          label: 'Profiles geo points',
        };
        setMap(uploadMap);
      }  
    }
    fetchMap();
  }, [pointsGeoJSON]);   

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <Dialog 
        header="Help on upload type selection" 
        visible={visibleDlg1} style={{ width: '50vw' }} 
        onHide={() => {if (!visibleDlg1) return; setVisibleDlg1(false);     
      }}>
      {(!uploadType) && (
        <p className="m-4">
          <h4 className="font-bold">You must choose the type of data you want to upload:</h4>
          <ul className="font-bold">
            <li>Soil Profiles</li>
            <li>Soil Samples</li>
            <li>Profiles&apos; Genealogy</li>
            <li>Samples&apos; Genealogy</li>
          </ul>
        </p>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_P) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Soil Profiles data upload </h4>   
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_profiles_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold mr-8">
              Download the XLSx template
            </a>
            <a href="/soildata/doc/upload_instructions_profiles.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold">
              Download the instructions for filling in the data
            </a>
          </div>    
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_S) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Soil Samples data upload </h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_profiles_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              Download the XLSx template
            </a>
            <a href="/soildata/doc/upload_instructions_profiles.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              Download the instructions for filling in the data
            </a>    
          </div>
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_PG) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Soil Profiles genealogy upload </h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_profiles_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold  m-4">
              Download the XLSx template
            </a>
            <a href="/soildata/doc/upload_instructions_profiles.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              Download the instructions for filling in the data
            </a>
          </div>    
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_SG) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Soil Samples Genealogy upload </h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_profiles_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              Download the XLSx template
            </a>
            <a href="/soildata/doc/upload_instructions_profiles.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              Download the instructions for filling in the data
            </a>
          </div>    
        </div>
        </>
      )}
      </Dialog>
      <Dialog header="Help on database action selection" visible={visibleDlg2} style={{ width: '50vw' }} onHide={() => {if (!visibleDlg2) return; setVisibleDlg2(false); }}>
      {(!uploadAction) && (
        <p className="m-4">
          <h4 className="font-bold">You need to choose the action used to write items in the database:</h4>
          <ul className="font-bold">
            <li>{UploadService.ACTIONS['POST'].label}: {UploadService.ACTIONS['POST'].info}.</li>
            <li>{UploadService.ACTIONS['PUT'].label}: {UploadService.ACTIONS['PUT'].info}</li>
            <li>{UploadService.ACTIONS['PATCH'].label}: {UploadService.ACTIONS['PATCH'].info}</li>
          </ul>
        </p>
      )}
      {(uploadAction) && ( 
        <div>
          <h4 className="font-bold m-4">{uploadAction.label} </h4>  
          <p className="m-4 font-bold">
            {uploadAction.info}        
          </p> 
        </div>    
      )}
      </Dialog>          
      <div className="card">
        <h4 class="font-bold">Soil Data XLS Upload</h4>
        <Panel header="INFORMATION" toggleable>
          <div><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text='This page permits to upload Soil Data using a XSLx SpreadSheet' /></div>
          <ol>
            <li><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text='First choose the type of data' /></li>
            <li><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text='Second choose the action to perform in the database' /></li>
            <li><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text='Third select the local file to upload' /></li>
            <ul>  
              <li><Message className="p-inline-message p-component p-inline-message-warn font-bold block" severity="warn" text='Please STAY ON THIS PAGE when pre-validating data.' /></li>
              <li><Message className="p-inline-message p-component p-inline-message-success font-bold block" severity="success" text='If the pre-validation is successful, you will be able to upload the soil data to the server by clicking on "Save data".'/></li>
              <li><Message className="p-inline-message p-component p-inline-message-error font-bold block" severity="error" text='If the data is not valid you can see a report that show errors.'/></li>
            </ul>
          </ol>    
        </Panel>
        <div class="flex flex-row justify-content-center mt-4">
          <Dropdown value={uploadType} onChange={(e) => setUploadType(e.value)} options={UploadService.GET_TYPES_ARRAY()} optionLabel="label" 
                    placeholder="Choose the Type" className="w-full mr-2 md:w-18rem" 
                    disabled={fileId !== null}
          />
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold mr-8"
                onClick={() => showTypeInfo()} 
                aria-controls={visibleDlg1 ? 'dialog_for_type' : null} 
                aria-expanded={visibleDlg1 ? true : false} >
          </Button> 
          <Dropdown value={uploadAction} onChange={(e) => setUploadAction(e.value)} options={UploadService.GET_ACTIONS_ARRAY()} optionLabel="label" 
                    placeholder="Choose the Action" className="w-full mr-2 md:w-14rem" 
                    disabled={fileId !== null}
          />
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold"
                onClick={() => showActionInfo()}
                aria-controls={visibleDlg2 ? 'dialog_for_action' : null} 
                aria-expanded={visibleDlg2 ? true : false} >
          </Button>
        </div> 
        {(upload) && ( 
        <>
          <div class="flex flex-row mt-4">
            <span class="font-bold text-lg">Upload title:&nbsp;</span> <span class="font-bold text-lg text-blue-500"> { upload?.title }</span>
          </div>     
          <div class="flex flex-row mt-4">
            <FileUpload 
              disabled={fileId !== null || validating}
              id="file"
              ref={xlsxFile}
              accept='.xlsx'
              chooseLabel={t('CHOOSE_FILE')}
              mode="basic"
              multiple={false}
              customUpload
              auto
              className='p-mb-4 p-mr-2 mt-4'
              uploadHandler={(e) => validateFile(e.files)}
            /> 
          </div>
        </>
        )}  
        {(upload && fileId !== null) && ( 
        <>
          <Message severity="success" content={'File: ' + fileId} /> 
          <div class="flex flex-row mt-4 mb-4">
            <Button
                label={t('RESET')}
                icon='pi pi-plus'
                type='button'
                disabled={validating || uploading}
                className='p-mr-2 p-mt-4 flex mr-4'
                onClick={() => { resetData(); }}
            />
            <Button
                label={t('IMPORT_DATA')}
                icon='pi pi-save'
                type='button'
                loading={uploading}
                disabled={validated < 100 || uploading || uploaded }
                className='p-mr-2 p-mt-4  flex'
                onClick={() => { setUploading(true); }} 
            /> 
          </div>
        </>
        )}    
        {(validating) && ( 
          <Message severity="warning" text="PRE-VALIDATING, Please Stay On This Page!" />
        )}
      </div>
      {(map) && (    
      <div className="card">
      <h5>{ map ? map.label : 'Pre-Validation Map' }</h5>
      <MyMap data={map} />
      </div>
      )}
      <div className="card"> 
      {( upload && upload.report && upload.report['errors'] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[0]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[0]]['total_errors'] > 0 ) && ( 
        <ReportTable
          elements={upload.report['errors'][UploadService.TYPES.XLS_P.sheets[0]]}
          headers={reportHeaders}
          title={'Sheet "' + UploadService.TYPES.XLS_P.sheets[0] + '": ' + upload.report['errors'][UploadService.TYPES.XLS_P.sheets[0]]['total_errors'] + ' Errors'}
          className='p-mt-4 p-mb-4' />         
      )}
      {( upload && upload.report && upload.report['errors'] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[0]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[0]]['total_errors'] === 0 ) && ( 
        <div className="card">
          <h5 class="font-bold text-green-500">No errors found in sheet {UploadService.TYPES.XLS_P.sheets[0]}</h5>
        </div> 
      )}
      {( upload && upload.report && upload.report['errors'] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[1]] && UploadService.TYPES.XLS_P.sheets[1] &&
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[1]]['total_errors'] > 0 ) && ( 
        <ReportTable
          elements={upload.report['errors'][UploadService.TYPES.XLS_P.sheets[1]]}
          headers={reportHeaders}
          title={'Sheet "' + UploadService.TYPES.XLS_P.sheets[1] + '": ' + upload.report['errors'][UploadService.TYPES.XLS_P.sheets[1]]['total_errors'] + ' Errors'}
          className='p-mt-4 p-mb-4' />  
      )}
      {( upload && upload.report && upload.report['errors'] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[1]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[1]]['total_errors'] === 0 ) && ( 
        <div className="card">
          <h5 class="font-bold text-green-500">No errors found in sheet {UploadService.TYPES.XLS_P.sheets[1]}</h5>
        </div> 
      )}
      {( upload && upload.report && upload.report['errors'] && UploadService.TYPES.XLS_P.sheets[2] &&
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[2]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[2]]['total_errors'] > 0 ) && ( 
        <ReportTable
          elements={upload.report['errors'][UploadService.TYPES.XLS_P.sheets[2]]}
          headers={reportHeaders}
          title={'Sheet "' + UploadService.TYPES.XLS_P.sheets[2] + '": ' + upload.report['errors'][UploadService.TYPES.XLS_P.sheets[2]]['total_errors'] + ' Errors'}
          className='p-mt-4 p-mb-4' />   
      )}
      {( upload && upload.report && upload.report['errors'] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[2]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[2]]['total_errors'] === 0 ) && ( 
        <div className="card">
          <h5 class="font-bold text-green-500">No errors found in sheet {UploadService.TYPES.XLS_P.sheets[2]}</h5>
        </div> 
      )}
      
      {( upload && upload.report && upload.report['errors'] && UploadService.TYPES.XLS_P.sheets[3] &&
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[3]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[3]]['total_errors'] > 0 ) && ( 
        <ReportTable
          elements={upload.report['errors'][UploadService.TYPES.XLS_P.sheets[3]]}
          headers={reportHeaders}
          title={'Sheet "' + UploadService.TYPES.XLS_P.sheets[3] + '": ' + upload.report['errors'][UploadService.TYPES.XLS_P.sheets[3]]['total_errors'] + ' Errors'}
          className='p-mt-4 p-mb-4' />   
      )}
      {( upload && upload.report && upload.report['errors'] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[3]] && 
         upload.report['errors'][UploadService.TYPES.XLS_P.sheets[3]]['total_errors'] === 0 ) && ( 
        <div className="card">
          <h5 class="font-bold text-green-500">No errors found in sheet {UploadService.TYPES.XLS_P.sheets[3]}</h5>
        </div> 
      )}
      </div>  
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


