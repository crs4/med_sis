import { point, featureCollection } from '@turf/turf';
import React, { useState, useContext, useEffect, useRef } from 'react';
import { useParams } from 'next/navigation'
import { Button } from 'primereact/button';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { useUser } from '../../context/user';
import Taxonomies from '../../data/taxonomies';
import Mapping from '../../data/mapping';
//import Test from '../../data/test';
import {useTranslations} from 'next-intl';
import {UploadService} from '../../service/uploads';
import {useRouter} from 'next/router';
import dynamic from "next/dynamic"
import ReportTable from '../../components/XLSxTable';
 
const MyMap = dynamic(() => import("../../components/XLSxDataMap"), { ssr:false })
 
function Page () {
  const params = useParams(); 
  const [upload, setUpload] = useState(null);
  const [map, setMap] = useState(null);
  const [loading, Loading] = useState(false);
  const [modelGeoJSON, setModelGeoJSON] = useState(null);
  const [modelsPoints, setModelsPoints] = useState(null);
  const [modelsName, setModelsName] = useState(null);
  const [basePoints, setBasePoints] = useState(null);
  const user = useUser();
  const toast = useRef(null);
  const t = useTranslations('default');
  const router = useRouter();

  function createPopupContent (point) {
      let panel = '<div><span>No data</span></div>';
      if ( !point.id )
        return panel;
      try {
        panel = '<div><span class="t-900 text-green">Profile '+point.id+'</span></div>';
        if ( !point.properties )
          return panel;
        let keys = Object.keys(point.properties);
        keys.forEach( (key) => {
          if ( point.properties[key] ) {
            panel += '<div><span class="t-900 text-blue">'+key+'</span>:';
            panel += '<span class="t-900 text-green">' +  point.properties[key] + '</span></div>';
          }  
        });
      } catch (e) {
        console.log(e);
      }
      return panel;  
  }
  
  const createBasePoints = ( general_sheet ) => {
    if (!general_sheet ) 
      return; 
    let j;
    let points = [];
    for ( j=1; j<general_sheet.length; j+=1 ){
/// skip row with null or errors in lat,lon or key
      try {
        const key = general_sheet[j][1];
        points.push( point( [data_sheet[j][7] , data_sheet[j][6]], 
                    { key: key },
                    { id: key }));
      } catch (e) {
        console.log(e);
      }
    }
    console.log(points);
    setBasePoints(points)
  } 
  
  const createModelsGeoJSON = ( data ) => {
    /* First sheet: XLS_P:General and Surface*/
    const sheets = ['General and Surface','Layer descriptions','Soil classification','Lab data'];
    const models_map = {};
    const models_names = [];
    const models_data = {};
    const models_points  = {};
    let i;
    for ( let s=0; s<4; s+=1 ) {
      const data_sheet = data[sheets[j]];
      const mapping = Mapping['XLS_P:'+sheets[s]];
      for ( let j=1; j<mapping.size+1; j+=1 ) {
        const el = mapping[j.toString()];
        if ( !models_map[el.m] ) {
          models_map[el.m] = {};
          models_names.push(el.m);
        }
        models_map[el.m][el.f] = j;
      }
      for ( let i=3; i<data_sheet.length; i+=1 ) {
        const row = data_sheet[i.toString()];
        if ( row ) {
          models_names.forEach((name) => {
            let okeys = Object.keys(models_map[name]);
            let properties =  {  };
            okeys.forEach ( (key) => {
              col = models_map[name][key];
              if ( row[col] )
                properties[key] = row[col]
            })
            if ( !models_data[name] )
              models_data[name] = {} ;
            models_data[name][row[1]] = properties;
          })
        }
      }
      models_names.forEach((name) => {
        if (basePoints){
          const points = basePoints.clone();
          for ( let p=0; p < points.length; p+=1) {
            if ( models_data[name][point.id] )
              points[p].properties = models_data[name][point.id];
          } 
          models_points[name] = points;

        }
      }) 
    }
    setModelsPoints(models_points)
    toast.current.show({severity:'success', summary: 'Data geo points created!', detail:'Data geo points created!', life: 3000});  
  } 

  

  useEffect(() => {
    if (!upload) {
      let today = new Date();
      setUpload ({
        date : today.toLocaleString(),
        title : 'Profiles'+today.getTime(),
        type: 'XLS_P',
        data: Test,
        report: null,
        status: UploadService.SUCCESFULLY_IMPORTED,
      }); 
    }  
  },[upload]);

  useEffect(() => {
    const fetchMap = async () => {
      if ( modelGeoJSON ) {
        const uploadMap = {
          layer : {
            points: modelGeoJSON,
          },
          label: 'Profiles points',
        };
        setMap(uploadMap);
      }  
    }
    fetchMap();
  }, [modelGeoJSON]);   
  /*  date : upload.date.toLocaleString(),
          title : upload.title,
          type: 'XLS profiles upload',
          data: Test,
          report: null,
          status: UploadService.SUCCESFULLY_IMPORTED,
        */
   
  if ( !upload  ) {
    return <></>;
  }

  

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <div className="card">
        <h4>{ 'Name: ' + upload.title  }</h4>
        <Panel header="Info" toggleable>
        
        </Panel>
        {(map) && (    
          <div className="card">
            <h5>{ map ? map.label : 'Models Map' }</h5>
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

export async function getStaticPaths() {
  return {
    paths: [], //indicates that no page needs be created at build time
    fallback: 'blocking' //indicates the type of fallback
  }
}

export async function getStaticProps(context) {
  return {
    props: {       
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}

export default Page;