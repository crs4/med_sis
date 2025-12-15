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
import TaxonomyService from '../../service/taxonomies';
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
  const [taxonomies, setTaxonomies] = useState(null);
  const [loading, setLoading] = useState(true);
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
        panel += '<span class="text-cyan-500 align-items-center font-bold" >Identifier:</span><span> '+code+'</span></div>';
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
    if ( !results ) {//// wrong data
      toast.current.show({severity:'danger', summary: 'GeoJSON error', detail:'No validation data', life: 3000});
      return;
    }
    for ( j=1; j<data_sheet.length; j+=1 ){
/// skip row with null or errors in lat,lon or key
      try {
        if ( data_sheet[j] && data_sheet[j][1] && 
             data_sheet[j][10] && data_sheet[j][11] &&
             data_sheet[j][10] < 90 && data_sheet[j][10] > -90 &&
             data_sheet[j][11] < 180 && data_sheet[j][11] > -180
        ){
          const key = data_sheet[j][1];
          let status = 'warn'
          if ( !results[key] || results[key]['wrong'] === 0) 
                status = 'ok';
          else  status = 'ko';
          points.push( point( [data_sheet[j][11] , data_sheet[j][10]], 
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
    let result = await validateXLSFile (files,upload.type,taxonomies);
    if ( result && result.validated  ){ 
      setValidated(result.validated)
      if  ( result['data'] && result['report'] ) {
        const _data = await createObjects(result,upload.type,document.cookie);
        setUpload({ 
          ...upload,
          title: files[0].name,
          data: JSON.stringify(_data),
          report: result['report'],
          operation: uploadAction?.name
        })
        
        try { 
          if ( upload.type === 'XLS_P' )
            createGeoJSON ( result['data'], result['report'] );
        } catch (e) {
          console.log(e);
          toast.current.show({severity:'error', summary: 'Errors generating points!', detail:'Map points not created!', life: 3000});
        }
      }
    }
    else if ( result && !result.validated  ){ 
      toast.current.show({severity:'error', summary: 'Errors in file!', detail:'wrong data!', life: 3000});
      setValidating(false);
      return;
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
    setUploadType(null);
    setUploadAction(null);
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
    const fetchData = ( async() => {
      let t =  await TaxonomyService.listAllValues(document.cookie)
      if ( !t )
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors reading data' , life: 5000});
      else if ( !t.data || !Array.isArray(t.data) || t.data.length === 0 ) 
        toast.current.show({severity:'warning', summary: 'No data!', detail: 'No data found' , life: 5000});
      else {
        
        let data = t.data;
        let taxms = {}
        for ( let i=0; i<data.length; i+=1 )
        {
          let v = data[i]
          if (v  && v.taxonomy ) {
            if (!taxms[v.taxonomy]) {
              taxms[v.taxonomy] = {} 
            }
            taxms[v.taxonomy][v.value] = v.descr;
          } 
        }

        setTaxonomies(taxms);
      }
      setLoading(false); 
    })
    if ( user.userData && user.userData.forbidden1 !== null && user.userData.forbidden1 ) {
      router.push(`/401`);
    }
    else {
      fetchData();
    }
  }, [user]); // eslint-disable-line

  useEffect(() => {
    if ( uploading ){
      saveData();
    }
  },[uploading]);  // eslint-disable-line

  useEffect(() => {
    const today = new Date();
    if ( uploadType ) {
      if (!upload ) {
        setUpload({
          date : today,
          title : uploadType.label+' '+today.toDateString(),
          type: uploadType.name,
          data: '',
          report: {},
          status: UploadService.STATUSES.UPLOADED,
          operation: uploadAction?.name
        })
      }
      else {
        setUpload({ 
          ...upload,
          date : today,
          title : uploadType.label+' '+today.toDateString(),
          type: uploadType.name,
          operation: uploadAction?.name
        })
      }  
    }
  },[uploadType]); // eslint-disable-line

  useEffect(() => {
    const fetchMap = async () => {
      if ( pointsGeoJSON ) {
        const uploadMap = {
          layer : {
            points: pointsGeoJSON,
            styles: {
              'New point -success' : { radius: 6, fillColor: '#0d0', color: 'rgba(0, 7, 221, 1)', weight: 3, opacity: 1, fillOpacity: 1, },
              'New point -errors' : { radius: 6, fillColor: '#f22', color: 'rgba(0, 7, 221, 1)', weight: 3, opacity: 1, fillOpacity: 1, },
              'New point -warnings' : { radius: 6, fillColor: '#f80', color: 'rgba(0, 7, 221, 1)', weight: 3, opacity: 1, fillOpacity: 1, },
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
            <li>New Point Soil Data</li>
            <li>Point Soil Data Genealogies</li>
            <li>Photos</li>
          </ul>
        </p>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_P) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Soil Point Data upload </h4>   
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
      {(uploadType && uploadType === UploadService.TYPES.XLS_PJ) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Genealogies of Data upload </h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_genealogy_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold  m-4">
              Download the XLSx template
            </a>
            <a href="/soildata/doc/upload_instructions_genealogies.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              Download the instructions for filling in the data
            </a>
          </div>    
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_PH) && ( 
        <>
        <div>
          <h4 className="font-bold m-4">Selected: Metadata of Photos upload </h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_genealogy_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold  m-4">
              Download the XLSx template
            </a>
            <a href="/soildata/doc/upload_instructions_genealogies.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
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
                    placeholder="Choose the Type" className="w-full mr-2 md:w-14rem" 
                    disabled={fileId !== null}
          />
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold"
                onClick={() => showTypeInfo()} 
                aria-controls={visibleDlg1 ? 'dialog_for_type' : null} 
                aria-expanded={visibleDlg1 ? true : false} >
          </Button> 
          <Dropdown value={uploadAction} onChange={(e) => setUploadAction(e.value)} options={UploadService.GET_ACTIONS_ARRAY()} optionLabel="label" 
                    placeholder="Choose the Action" className="w-full ml-8 mr-2 md:w-14rem" 
                    disabled={fileId !== null}
          />
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold"
                onClick={() => showActionInfo()}
                aria-controls={visibleDlg2 ? 'dialog_for_action' : null} 
                aria-expanded={visibleDlg2 ? true : false} >
          </Button>
        </div> 
        {(uploadAction && uploadType) && ( 
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
              className='mb-4 mr-2 mt-4'
              uploadHandler={(e) => validateFile(e.files)}
            /> 
          </div>
        </>
        )}  
        {(fileId !== null) && ( 
        <>
          <Message severity="success" content={'File: ' + fileId} /> 
          <div class="flex flex-row mt-4 mb-4">
            <Button
                label={t('RESET')}
                icon='pi pi-plus'
                type='button'
                disabled={validating || uploading}
                className='mr-2 mt-4 flex mr-4'
                onClick={() => { resetData(); }}
            />
            <Button
                label={t('IMPORT_DATA')}
                icon='pi pi-save'
                type='button'
                loading={uploading}
                disabled={validated < 100 || validating ||  uploading || uploaded }
                className='mr-2 mt-4 flex'
                onClick={() => { setUploading(true); }} 
            /> 
          </div>
        </>
        )}    
        {(validating) && ( 
          <Message severity="warn" content="PRE-VALIDATING, Please Stay On This Page!" />
        )}
      </div>
      {(map) && (    
      <div className="card">
      <h5>{ map ? map.label : 'Pre-Validation Map' }</h5>
      <MyMap data={map} />
      </div>
      )}
      { (taxonomies) && (
      <div className="card"> 
      {( upload && upload.report && upload.report['errors'] && uploadType  && uploadType.sheets && upload.report['errors'][uploadType.sheets[0]].constructor == Array && (
        <>
        {( upload.report['total_errors'] > 0 ) && (
          <Message severity="danger" content={"Found " + upload.report.total_errors + " errors in sheets" } />
        )}
        {( uploadType.sheets[0] && upload.report['errors'][uploadType.sheets[0]] && (
          <>
          {( upload.report['errors'][uploadType.sheets[0]].length > 0 ) && ( 
            <ReportTable
              elements={upload.report['errors'][uploadType.sheets[0]]}
              headers={reportHeaders}
              title={'Sheet "' + uploadType.sheets[0] + '": ' + upload.report['errors'][uploadType.sheets[0]].length + ' Errors'}
              className='p-mt-4 p-mb-4' />         
          )}
          {(  upload.report['errors'][uploadType.sheets[0]].length === 0 ) && ( 
            <div className="card">
              <h5 class="font-bold text-green-500">No errors found in sheet {uploadType.sheets[0]}</h5>
            </div> 
          )}
          </>
        ))}  
        {( uploadType.sheets[1] && upload.report['errors'][uploadType.sheets[1]] && upload.report['errors'][uploadType.sheets[1]].constructor == Array &&(
          <> 
          {( upload.report['errors'][uploadType.sheets[1]].length > 0 ) && ( 
           
            <ReportTable
              elements={upload.report['errors'][uploadType.sheets[1]]}
              headers={reportHeaders}
              title={'Sheet "' + uploadType.sheets[1] + '": ' + upload.report['errors'][uploadType.sheets[1]].length + ' Errors'}
              className='p-mt-4 p-mb-4' />         
          )}
          {(  upload.report['errors'][uploadType.sheets[1]].length === 0 ) && ( 
          
            <div className="card">
              <h5 class="font-bold text-green-500">No errors found in sheet {uploadType.sheets[1]}</h5>
            </div> 
          )}
          </>
        ))}
        {( uploadType.sheets[2] && upload.report['errors'][uploadType.sheets[2]] && upload.report['errors'][uploadType.sheets[2]].constructor == Array && (
         <>
          {( upload.report['errors'][uploadType.sheets[2]].length > 0 ) && ( 
            <ReportTable
              elements={upload.report['errors'][uploadType.sheets[2]]}
              headers={reportHeaders}
              title={'Sheet "' + uploadType.sheets[2] + '": ' + upload.report['errors'][uploadType.sheets[2]].length + ' Errors'}
              className='p-mt-4 p-mb-4' />         
          )}
          {( upload.report['errors'][uploadType.sheets[2]].length === 0 ) && ( 
            <div className="card">
              <h5 class="font-bold text-green-500">No errors found in sheet {uploadType.sheets[2]}</h5>
            </div> 
          )}
          </>
        ))}  
        {( uploadType.sheets[3] && upload.report['errors'][uploadType.sheets[3]] && upload.report['errors'][uploadType.sheets[3]].constructor == Array && ( 
          <>
          {( upload.report['errors'][uploadType.sheets[3]].length > 0 ) && ( 
            <ReportTable
              elements={upload.report['errors'][uploadType.sheets[3]]}
              headers={reportHeaders}
              title={'Sheet "' + uploadType.sheets[3] + '": ' + upload.report['errors'][uploadType.sheets[3]].length + ' Errors'}
              className='p-mt-4 p-mb-4' />         
          )}
          {( upload.report['errors'][uploadType.sheets[3]].length === 0 ) && ( 
            <div className="card">
              <h5 class="font-bold text-green-500">No errors found in sheet {uploadType.sheets[3]}</h5>
            </div> 
          )}
          </>
        ))}
        </>
      ))}
      </div>
      )}
      {(loading) && (
        <h2>Loading Data...</h2>
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
