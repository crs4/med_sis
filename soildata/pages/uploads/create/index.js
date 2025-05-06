import { point, featureCollection } from '@turf/turf';
import React, { useState, useContext, useEffect, useRef } from 'react';
import { Button } from 'primereact/button';
import { FileUpload } from 'primereact/fileupload';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { useUser } from '../../../context/user';
import Taxonomies from '../../../data/taxonomies';
import Mapping from '../../../data/mapping';
import {useTranslations} from 'next-intl';

import { UploadService } from '../../../service/uploads';
import { validateXLSFile } from '../../../utilities/XLSxUtils';

import ReportTable from '../../../components/XLSxTable';
import {useRouter} from 'next/router';
import dynamic from "next/dynamic"
 
const MyMap = dynamic(() => import("../../../components/XLSxMap"), { ssr:false })
 
function Upload () {
  const [upload, setUpload] = useState(null);
  const [map, setMap] = useState(null);
  const [data, setData] = useState(null);
  const [report, setReport] = useState(null);
  const [validated, setValidated] = useState(0);
  const [validating, setValidating] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [pointsGeoJSON, setPointsGeoJSON] = useState(null);
  const [currentModel, setCurrentModel] = useState(null);
  const [modelsGeoJSON, setModelsGeoJSON] = useState(null);
  const [fileId, setFileId] = useState(null);
  const user = useUser();
  const xlsxFile = useRef(null);
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();

  function createPopupContent (code, result) {
      let panel = '<div><span>No data</span></div>';
      if ( !result || !code )
        return panel;
      try {
        panel = '<div><span class="t-900 text-green">Profile '+code+'</span></div>';
        let keys = Object.keys(result);
        let values;
        let v;
        keys.forEach( (key) => {
          if ( result[key] ) {
            panel += '<div><span class="t-900 text-blue">'+key+'</span>:';
            if ( key != 'wrong' && result[key]) {
              values = result[key].split(':');
              
              if ( values.length === 2 && values[0] && values[1] ) {
                v = Math.floor(values[0]);
                panel += '<span class="t-900 text-green"> Filled: </span><span> ' + 
                  v + '%</span>' +
                  '<span class="t-900 text-red"> Errors: </span><span> ' + 
                  values[1] + '</span>';
              }  
              else panel += '<span>' + result[key] + '</span>';
            }  
            else panel += '<span>' + result[key] + '</span>';
          }
          panel += '</div>';
        });
      } catch (e) {
        console.log(e);
      }
      return panel;  
  }
  
  const createGeoJSON = ( general_sheet, data_report ) => {
    if (!general_sheet || !data_report ) 
      return; 
    let j;
    let points = [];
    const results = data_report['tree'];
    if ( !results ) //// wrong data
      return;
    for ( j=1; j<data_sheet.length; j+=1 ){
/// skip row with null or errors in lat,lon or key
      try {
        const key = data_sheet[j][1];
        let status = 'warn'
        if ( !results[key] || results[key]['wrong'] === 0) 
              status = 'ok';
        else status = 'ko';
        points.push( point( [data_sheet[j][7] , data_sheet[j][6]], 
                    { key: key, status: status, popupContent : createPopupContent( key, results[key])  },
                    { id: key }));
      } catch (e) {
        console.log(e);
      }
    }
    if ( points.length > 0 ) {
      setPointsGeoJSON( featureCollection(points));
      toast.current.show({severity:'success', summary: 'GeoJSON created!', detail:'GeoJSON for elements created', life: 3000});
    }  
  } 

  const validateFile = async (files) => {
    // eslint-disable-next-line
    const isProfile = ( UploadService.TYPES[upload.type].name === "PROFILES" );
    const isSample = ( UploadService.TYPES[upload.type].name === "SAMPLES" );
    let sheets = UploadService.TYPES[upload.type].sheets;
    
    if ( (!isProfile && !isSample && !sheets ) || !files || !files[0]  ){
      toast.current.show({severity:'error', summary: 'Error!', detail:'Wrong upload type or missing file!', life: 3000});
      return;
    }
    setValidating(true);
    setFileId(files[0].name);
    let result = await validateXLSFile (files,isProfile,sheets,Taxonomies,Mapping);
    console.log(result);
    if ( result  ){ 
      
      setData(result['data']);
      setReport(result['report']);
      if  ( sheets[0] && result['data'] && result['report'] && ( isProfile || isSample ) ) {
          createGeoJSON ( result['data'][sheets[0]], result['report'] );
      }
    }
    else { 
      toast.current.show({severity:'error', summary: 'Error!', detail:'Errors validating file!', life: 3000});
      setValidating(false);
      return;
    }
    
    setValidating(false);
  }

  const saveData = async (e) => {
      try {
        /*console.log (user);
        setUploading(true);
        const response = await UploadService.save(currentUpload);
        const data = await response.json()
        console.log(data)
        
        if (response.ok) { 
        */
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors sending data' , life: 3000});
        //toast.current.show({severity:'success', summary: 'Success!', detail: 'Data has been sent' , life: 3000});
        //router.push('/soildata/uploads')   
        /*
        else { 
          toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving data' , life: 3000});
        } 
        */
      } catch (error) {
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors sending data' , life: 3000}); 
      } finally {
        setUploading(false);
      }
  } 
  
  let reportHeaders = ['Element', 'Row', 'Column', 'Error'];

  const resetData = () => {
    setMap(null);
    setData(null);
    setReport(null);
    setValidated(0);
    setPointsGeoJSON(null);
    setFileId(null);
    xlsxFile.current?.clear();
  };

  useEffect(() => {
    if (!upload) {
      var today = new Date();
      setUpload ({
        date : today.toLocaleString(),
        title : 'Profiles'+today.getTime(),
        type: 'XLS_P',
        data: null,
        report: null,
        status: UploadService.STATUS.CREATED,
      }); 
    }  
  },[upload]);

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
          label: 'Profiles points',
        };
        setMap(uploadMap);
      }  
    }
    fetchMap();
  }, [pointsGeoJSON]);   

   
  if ( !upload  ) {
    return <></>;
  }

  

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <div className="card">
        <h5>XLSx Soil Profiles Upload</h5>
        <Panel header="Info" toggleable>
          <div><Message severity="info" text='This page permits to upload Soil Profiles using a XSLx SpreadSheet' /></div>
          <div><Message severity="warn" text='Choose the local file and please STAY ON THIS PAGE when pre-validating data.' /></div>
          <ul>
              <li><Message severity="success" text='If the pre-validation is performed successfully you will be able to upload profiles to the server.'/></li>
              <li><Message severity="error" text='If the data is not valid you can see a report that show errors.'/></li>
          </ul>
          <div className="flex flex-column sm:flex-row my-2 w-full gap-3">
            <a href="doc/xlsx_profiles_template.xlsx" target="_blank" rel="noopener noreferrer" className="p-button font-bold">
              Download template
            </a>
            <a href="doc/xlsx_profiles_instructions.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold">
              Instructions
            </a>   
          </div>
        </Panel>
        <h6>{ 'Name: ' + upload.title + ' Date:' + upload.date }</h6>
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
              className=''
              uploadHandler={(e) => validateFile(e.files)}
        /> 
        {(fileId) && ( 
          <Message severity="success" content={'File: ' + fileId} /> )}
        <div className="flex flex-column my-2 flex sm:flex-row gap-3 w-full"> 
          <Button
              label={t('RESET')}
              icon='pi pi-plus'
              type='button'
              loading={validating}
              disabled={validating}
              className='p-mr-2 p-mt-4 flex '
              onClick={() => {
                resetData();
              }}
          />
          <Button
              label={t('IMPORT_DATA')}
              icon='pi pi-save'
              type='button'
              loading={uploading}
              disabled={validated < 100 || uploading}
              className='p-mr-2 p-mt-4  flex'
              onClick={() => {
                saveData();
              }} 
          /> 
        </div> 
        {(validating) && ( 
          <Message severity="warning" text="PRE-VALIDATING, Please Stay On This Page!" />
        )}  
        {(map) && (    
          <div className="card">
            <h5>{ map ? map.label : 'Pre-Validation Map' }</h5>
            <MyMap data={map} />
          </div>

        )} 
        {(report && report['errors'] && report['errors'][UploadService.TYPES[upload.type].sheets[0]] ) && ( 
          <ReportTable
            elements={report['errors'][UploadService.TYPES[upload.type].sheets[0]]}
            headers={reportHeaders}
            title={'Sheet "' + UploadService.TYPES[upload.type].sheets[0] + '": ' + report['errors'][UploadService.TYPES[upload.type].sheets[0]]['total_errors'] + ' Errors'}
            className='p-mt-4 p-mb-4' />         
        )}
        {(report && report['errors'] && report['errors'][UploadService.TYPES[upload.type].sheets[1]]) && ( 
          <ReportTable
              elements={report['errors'][UploadService.TYPES[upload.type].sheets[1]]}
              headers={reportHeaders}
              title={'Sheet "' + UploadService.TYPES[upload.type].sheets[1] + '": ' + report['errors'][UploadService.TYPES[upload.type].sheets[1]]['total_errors'] + ' Errors'}
              className='p-mt-4 p-mb-4' />  
        )}
        {(report && report['errors'] && report['errors'][UploadService.TYPES[upload.type].sheets[2]]) && ( 
          <ReportTable
              elements={report['errors'][UploadService.TYPES[upload.type].sheets[2]]}
              headers={reportHeaders}
              title={'Sheet "' + UploadService.TYPES[upload.type].sheets[2] + '": ' + report['errors'][UploadService.TYPES[upload.type].sheets[2]]['total_errors'] + ' Errors'}
              className='p-mt-4 p-mb-4' />   
        )}
        {(report && report['errors'] && report['errors'][UploadService.TYPES[upload.type].sheets[3]]) && ( 
          <ReportTable
              elements={report['errors'][UploadService.TYPES[upload.type].sheets[3]]}
              headers={reportHeaders}
              title={'Sheet "' + UploadService.TYPES[upload.type].sheets[3] + '": ' + report['errors'][UploadService.TYPES[upload.type].sheets[3]]['total_errors'] + ' Errors'}
              className='p-mt-4 p-mb-4' />   
        )}
      </div>
    </div>
  );
}

export async function getStaticProps(context) {
  return {
    props: {       
      messages: (await import(`../../../translations/${context.locale}.json`)).default
     },
  }
}

export default Upload;