"use client"

import { point, featureCollection } from '@turf/turf';
import React, { useState, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';
import { FileUpload } from 'primereact/fileupload';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { Dropdown } from 'primereact/dropdown';
import { Dialog } from 'primereact/dialog';
import TaxonomyService from '../../service/taxonomies';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import UserService from '../../service/user';
import { UploadService } from '../../service/uploads';
import { createObjects, validateXLSFile } from '../../utilities/xls';
import ReportTable from '../../components/table/XLSxTable';
import dynamic from "next/dynamic"

const MyMap = dynamic(() => import("../../components/map/XLSxMap"), { ssr:false })

export default function Page( )  {
  
  // new upload object
  const [upload, setUpload] = useState(null);
  // new upload object type
  const [uploadType, setUploadType] = useState(null);
  // new upload object action
  const [uploadAction, setUploadAction] = useState(null);
  // MED SIS taxonomies 
  const [taxonomies, setTaxonomies] = useState(null);
  // Loading data state
  const [loading, setLoading] = useState(true);
  // Visibility state of the type selection dialog
  const [visibleDlg1, setVisibleDlg1] = useState(false);
  // Visibility state of the action selection dialog
  const [visibleDlg2, setVisibleDlg2] = useState(false);
  // validated status of the new upload 
  const [validated, setValidated] = useState(0);
  // validating state 
  const [validating, setValidating] = useState(false);
  // uploaded status of the XLSx file of the new upload 
  const [uploaded, setUploaded] = useState(false);
  // uploading state 
  const [uploading, setUploading] = useState(false);
  // map to show validated points of the new upload 
  const [map, setMap] = useState(null);
  // geoJSON of the validated  points to show in the map 
  const [pointsGeoJSON, setPointsGeoJSON] = useState(null);
  // XLSx file identifier
  const [fileId, setFileId] = useState(null);
  // XLSx file component reference
  const xlsxFile = useRef(null);
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();
  
  // To return to the uploads list
  const openList = () => {
    router.push(`/uploads`);
  };

  // to create Popup Content for the validated points
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
              panel += '<span class="font-bold">' + t('Filled') + ': </span>';
              panel += '<span class="font-bold text-green-500"> ' + v + '%</span>';
              panel += '<span class="font-bold">' + t('ERRORS') +': </span>';
              panel += '<span class="font-bold text-orange-600"> ' + values[1] + '</span>';
            }  
            else panel += '<span class="font-bold">' + result[key] + '</span>';
            
          } 
          panel += '</div>'; 
        }
      });
    } catch (e) {
      console(e)
    }
    return panel;  
  }

  // to create the GeoJSON for the validated points 
  const createGeoJSON = ( data_sheets, data_report ) => {
    const sheetname = UploadService.TYPES[upload.type].sheets[0]
    const data_sheet = data_sheets[ sheetname ]
    if (!data_sheet || !data_report ) 
      return; 
    let j;
    let points = [];
    const results = data_report['tree'];
    if ( !results ) {//// wrong data
      toast.current.show({severity:'danger', summary: 'GeoJSON error', detail:t('EMPTY'), life: 3000});
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
       
      }
    }
    if ( points.length > 0 ) {
      setPointsGeoJSON( featureCollection(points));
      toast.current.show({severity:'success', summary: 'GeoJSON created!', detail:'GeoJSON created', life: 3000});
    }  
  } 
 
  // to validate XLSx file content 
  const validateFile = async (files) => {
    if ( !upload )
      return   
    if ( !files || !files[0]  ){
      toast.current.show({severity:'error', summary: t('ERRORS'), detail:t('WRONG_FILE'), life: 3000});
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
        
        try {  /// create GeoJSON only for a point soil data XLSx file
          if ( upload.type === 'XLS_P' )
            createGeoJSON ( result['data'], result['report'] );
        } catch (e) {
          
          toast.current.show({severity:'error', summary: t('ERRORS'), detail:t('MAP_NOT_CREATED'), life: 3000});
        }
      }
    }
    else if ( result && !result.validated  ){ 
      toast.current.show({severity:'error', summary: t('ERRORS'), detail:t('WRONG_FILE'), life: 3000});
      setValidating(false);
      return;
    }
    else { 
      toast.current.show({severity:'error', summary: t('ERRORS'), detail:t('WRONG_FILE'), life: 3000});
      setValidating(false);
      return;
    }
    setValidating(false);
  }

  // Send the data to the backend 
  const saveData = async () => {
    try {
      if ( !upload || !uploading )
        return;
      let nu = { ...upload }
      nu.report = {}
      const response = await UploadService.save(document.cookie, nu);
      if (response && response.ok ) { 
        toast.current.show({severity:'success', summary: t('SUCCESS'), detail: t('DATA_SENT') , life: 3000});
        setTimeout(() => {
          router.push('/uploads') 
        }, 3000);
      } 
      else toast.current.show({severity:'error', summary: t('ERRORS'), detail: 'ERRORS' , life: 3000});

    } catch (error) {
      toast.current.show({severity:'error', summary: t('CRITICAL_ERROR'), detail: t('CRITICAL_ERROR') , life: 3000}); 
    } 
    setUploaded(true);
    setUploading(false);
  } 
  
  let reportHeaders = [t('ELEMENT'), t('ROW'), t('COLUMN'), t('ERROR')];

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
      const user = await UserService.getProfile(document.cookie);
      if ( !user || ( user.forbidden !== null && user.forbidden) )
        router.push(`/401`);    
      let t =  await TaxonomyService.listValues(document.cookie,null)
      if ( !t || ( !t.data || !Array.isArray(t.data) || t.data.length === 0 )) 
        toast.current.show({severity:'warning', summary: t('ERRORS'), detail: t('ERRORS') , life: 5000});
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
    fetchData();
  }, []); // eslint-disable-line

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
          label: 'geoJSON points',
        };
        setMap(uploadMap);
      }  
    }
    fetchMap();
  }, [pointsGeoJSON]);   

  const headerTemplate1 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}>{t("UPLOADS_HELP_TYPES")} </h4>
  };

  const headerTemplate2 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }} >{t("UPLOADS_HELP_ACTIONS")}</h4>
  };

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      <Dialog 
        header={headerTemplate1} 
        visible={visibleDlg1} style={{ width: '50vw' }} 
        onHide={() => {if (!visibleDlg1) return; setVisibleDlg1(false);     
      }}>
      {(!uploadType) && (
        <div className="m-4 font-bold text-cyan-800">
          <h4>{t("UPLOADS_CHOOSE_TYPE")}</h4>
          <h4>{t("TYPES")}:</h4>
          <ul className="text-lg">
            <li>{t("POINTS_SOIL_DATA")}</li>
            <li>{t("PROJECTS")}</li>
            <li>{t("PHOTOS")}</li>
            <li>{t("EXTRA_LABORATORY_DATA")}</li>
          </ul>
        </div>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_P) && ( 
        <>
        <div className="m-4 font-bold text-cyan-800">
          <h4>{t("POINTS_SOIL_DATA")} </h4>   
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_profiles_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold mr-8">
              {t("DOWNLOAD_XLSX_TEMPLATE")}
            </a>
            <a href="/soildata/doc/upload_instructions_profiles.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold">
              {t("DOWNLOAD_XLSX_INSTRUCTIONS")}
            </a>
          </div>    
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_PJ) && ( 
        <>
        <div className="m-4 font-bold text-cyan-800">
          <h4>{t("PROJECTS")}</h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_genealogy_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold  m-4">
              {t("DOWNLOAD_XLSX_TEMPLATE")}
            </a>
            <a href="/soildata/doc/upload_instructions_genealogies.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
             {t("DOWNLOAD_XLSX_INSTRUCTIONS")}
            </a>
          </div>    
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_PH) && ( 
        <>
        <div className="m-4 font-bold text-cyan-800">
          <h4>{t("PHOTOS")}</h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_genealogy_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold  m-4">
              {t("DOWNLOAD_XLSX_TEMPLATE")}
            </a>
            <a href="/soildata/doc/upload_instructions_genealogies.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              {t("DOWNLOAD_XLSX_INSTRUCTIONS")}
            </a>
          </div>    
        </div>
        </>
      )}
      {(uploadType && uploadType === UploadService.TYPES.XLS_EL) && ( 
        <>
        <div className="m-4 font-bold text-cyan-800">
          <h4>{t("EXTRA_LABORATORY_DATA")}</h4>       
          <div class="flex flex-row justify-content-center ">
            <a href="/soildata/doc/xlsx_extra_lab_data_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold  m-4">
              {t("DOWNLOAD_XLSX_TEMPLATE")}
            </a>
            <a href="/soildata/doc/upload_instructions_extra_lab_data.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold m-4">
              {t("DOWNLOAD_XLSX_INSTRUCTIONS")}
            </a>
          </div>    
        </div>
        </>
      )}
      </Dialog>
      <Dialog header={headerTemplate2} visible={visibleDlg2} style={{ width: '50vw' }} onHide={() => {if (!visibleDlg2) return; setVisibleDlg2(false); }}>
      {(!uploadAction) && (
        <div className="m-4 font-bold text-cyan-800">
          <h4>{t("UPLOADS_CHOOSE_ACTION")}:</h4>
          <ul className="text-lg">
            <li>{UploadService.ACTIONS['POST'].label}: {t("POST_DESCR")}</li>
            <li>{UploadService.ACTIONS['PUT'].label}: {t("PUT_DESCR")}</li>
            <li>{UploadService.ACTIONS['PATCH'].label}: {t("PATCH_DESCR")}</li>
          </ul>
        </div>
      )}
      {(uploadAction) && ( 
        <div className="m-4 font-bold text-cyan-800">
          <h4>{uploadAction.label}</h4>  
          <p>
            {t(uploadAction.name+"_DESCR")}        
          </p> 
        </div>    
      )}
      </Dialog>          
      <h4 className="w-full surface-200 font-bold text-cyan-800 p-3 mb-3 shadow-2">{t("UPLOADS_TITLE")}</h4>
      <div className="card text-cyan-800 w-full shadow-2">
        <div className="flex flex-row-reverse w-full p-2">
          <Button 
            icon="pi pi-download"
            className="flex bg-primary font-bold border-round"
            disabled={validating && uploading}
            onClick={() => openList()}
            label={t('UPLOADS_LIST')}
          />
        </div>
        <Panel header={t('UPLOAD_HELP')} toggleable collapsed>
          <div><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text={t('UPLOADS_MSG1')}/></div>
          <ol>
            <li><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text={t('UPLOADS_MSG2')}/></li>
            <li><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text={t('UPLOADS_MSG3')}/></li>
            <li><Message className="p-inline-message p-component p-inline-message-info font-bold block" severity="info" text={t('UPLOADS_MSG4')}/></li>
            <ul>  
              <li><Message className="p-inline-message p-component p-inline-message-warn font-bold block" severity="warn" text={t('UPLOADS_MSG5')}/></li>
              <li><Message className="p-inline-message p-component p-inline-message-success font-bold block" severity="success" text={t('UPLOADS_MSG6')}/></li>
              <li><Message className="p-inline-message p-component p-inline-message-error font-bold block" severity="error" text={t('UPLOADS_MSG7')}/></li>
            </ul>
          </ol>    
        </Panel>
        <div class="flex flex-row justify-content-center mt-4">
          <Dropdown value={uploadType} onChange={(e) => setUploadType(e.value)} options={UploadService.GET_TYPES_ARRAY()} optionLabel="label" 
                    placeholder={t('UPLOADS_CHOOSE_T')} className="w-full mr-2 md:w-14rem" 
                    disabled={fileId !== null}
          />
          <Button label="?" class="p-button p-component p-button-outlined p-button-rounded p-button-info font-bold"
                onClick={() => showTypeInfo()} 
                aria-controls={visibleDlg1 ? 'dialog_for_type' : null} 
                aria-expanded={visibleDlg1 ? true : false} >
          </Button> 
          <Dropdown value={uploadAction} onChange={(e) => setUploadAction(e.value)} options={UploadService.GET_ACTIONS_ARRAY()} optionLabel="label" 
                    placeholder={t('UPLOADS_CHOOSE_A')} className="w-full ml-8 mr-2 md:w-14rem" 
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
            <span class="font-bold text-lg">{t('UPLOADS_TITLE')}:&nbsp;</span> <span class="font-bold text-lg text-blue-500"> { upload?.title }</span>
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
          <Message severity="warn" content={t('UPLOADS_MSG5')} />
        )}
      </div>
      {(map) && (    
      <div className="card">
      <h5>{ map ? map.label : t('UPLOADS_MAP') }</h5>
      <MyMap data={map} />
      </div>
      )}
      {( taxonomies && upload && upload.report && upload.report['errors'] && uploadType  && uploadType.sheets && upload.report['errors'][uploadType.sheets[0]].constructor == Array && (
        <div className="card">
        {( upload.report['total_errors'] > 0 ) && (
          <Message severity="danger" content={upload.report.total_errors + t('ERRORS')   } />
        )}
        {( uploadType.sheets[0] && upload.report['errors'][uploadType.sheets[0]] && (
          <>
          {( upload.report['errors'][uploadType.sheets[0]].length > 0 ) && ( 
            <ReportTable
              elements={upload.report['errors'][uploadType.sheets[0]]}
              headers={reportHeaders}
              title={uploadType.sheets[0] + '": ' + upload.report['errors'][uploadType.sheets[0]].length + ' ' + t('ERRORS')}
              className='p-mt-4 p-mb-4' />         
          )}
          {(  upload.report['errors'][uploadType.sheets[0]].length === 0 ) && ( 
            <div className="card">
              <h5 class="font-bold text-green-500">{uploadType.sheets[0]}: {t('NO_ERRORS')}</h5>
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
              title={uploadType.sheets[1] + '": ' + upload.report['errors'][uploadType.sheets[1]].length + t('ERRORS')}
              className='p-mt-4 p-mb-4' />         
          )}
          {(  upload.report['errors'][uploadType.sheets[1]].length === 0 ) && ( 
          
            <div className="card">
              <h5 class="font-bold text-green-500">{uploadType.sheets[1]}: {t('NO_ERRORS')}</h5>
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
              title={'Sheet "' + uploadType.sheets[2] + '": ' + upload.report['errors'][uploadType.sheets[2]].length + t('ERRORS')}
              className='p-mt-4 p-mb-4' />         
          )}
          {( upload.report['errors'][uploadType.sheets[2]].length === 0 ) && ( 
            <div className="card">
              <h5 class="font-bold text-green-500">{uploadType.sheets[2]}: {t('NO_ERRORS')}</h5>
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
              title={'Sheet "' + uploadType.sheets[3] + '": ' + upload.report['errors'][uploadType.sheets[3]].length  + t('ERRORS')}
              className='p-mt-4 p-mb-4' />         
          )}
          {( upload.report['errors'][uploadType.sheets[3]].length === 0 ) && ( 
            <div className="card">
              <h5 class="font-bold text-green-500">{uploadType.sheets[3]}: {t('NO_ERRORS')}</h5>
            </div> 
          )}
          </>
        ))}
        </div>
      ))}
      {(loading) && (
        <h2>{t('LOADING')}</h2>
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
