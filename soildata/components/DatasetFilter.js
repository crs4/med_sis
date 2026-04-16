import { Button } from 'primereact/button';
import React, { useState, useRef } from 'react';
import {useTranslations} from 'next-intl';
import { userContext, useUser } from '../context/user';
import Loading from './Loading';
import { Card } from 'primereact/card';
import { Toast } from 'primereact/toast';

const MapFilter = dynamic(() => import('./MapFilter'), {ssr: false})

const initialFilter = {
  aoi : null,
  period : [null,null] ,
  depth: [0,null],
  project: null,
  type: null,
  method: null
};
/*
    <Fieldset legend="Depth">
        <div className="grid m-2">
          <div classname="col-6">
            <h5 className="font-bold text-cyan-800">Upper: {depth[0]}</h5>
            <h5 className="font-bold text-cyan-800">Lower: {depth[1]}</h5>
          </div>
          <div classname="col-6 flex flex-column align-item-center">
            <div className="font-bold text-blue-800">0 cm</div>
            <Slider max={maxDepth} value={depth} onChange={(e) => setDepth(e.value)} orientation="vertical" className="h-14rem" range />
            <div className="font-bold text-blue-800">100 cm</div>
            <span className="p-float-label">
              <InputNumber id="maxdepth" maxFractionDigits='0' value={maxDepth} onValueChange={(e) => setMaxDepth(e.value)} />
              <label htmlFor="maxdepth">Max Depth (default 100)</label>
            </span>
          </div>
        </div>
        </Fieldset>
      </div>
      <div className="flex flex-row gap-3 align-items-center">
        <Button icon="pi pi-arrow-circle-left" label="Previous" onClick={() => resetData() } severity="success" raised />
        <Button icon="pi pi-arrow-circle-right" iconPos="right" label="Next" disabled={!filteredPoints} onClick={ () => setActiveIndex(2)} severity="success" raised />
      </div>
*/    
const DatasetFilter = ( { dataset, setDataset } ) => {
  const user = useUser(); 
  const [ layersList, setLayersList] = useState([]);
  const [ selectedLayer, setSelectedLayer] = useState(null);
  const [ isLoading, setIsLoading] = useState(false);
  const [ filter, setFilter] = useState(initialFilter);
  const toast = useRef(null);

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden) )
      router.push(`/401`);
  },[user]);  // eslint-disable-line

  useEffect(() => {
    filterData
  },[filter]);  // eslint-disable-line

  if (isLoading) {
    return <Loading />;
  }

  const inRange = ( a, b ) => {
    let min = (a[0] < b[0]  ? a : b)
    let max = (min == a ? b : a)
    if ( min[1] < max[0] )
      return false;
    return true
  }

  const uploadRoiFile = async (file) => {
    try {
      // validate geometry first feature
      // Add bbox, area to new geojson
      if ( file ) 
      {
        const readFilePromise = (path) => new Promise((resolve, reject) => {
          const readFile = new FileReader();
          readFile.onload = (event) =>  { 
            const contents = event.target.result;
            try { 
            /// only one feature!!!
              const geojson = JSON.parse(contents.replaceAll('/n',''));
              let ftCl = null
              let oneFeature = null;
              // verify data
              if ( geojson && area( geojson ) ) {
                if ( geojson.type === 'Feature' ) 
                  ftCl = featureCollection([geojson])
                else { 
                  geojson.features.forEach( (ft) => {
                    if ( area(ft) ) 
                      if ( oneFeature ) {
                        oneFeature = union( oneFeature, ft )
                      }  
                      else oneFeature = ft 
                  })
                  if ( oneFeature )
                    ftCl = featureCollection([oneFeature])
                }
              }
              else {
                reject('wrong json file');
              }
              ftCl.bbox = bbox(ftCl);
              resolve(ftCl);
            } catch (error) {
              reject('errors reading json file');
            }
          };
          readFile.onerror = (error) => {
            reject(error);
          };
          readFile.readAsText(file);
        });     
        const result = await readFilePromise(file)
        if ( result ) {    
          filter.aoi = result
          toast.current.show({ severity: 'success', summary: 'Done!', detail: 'Your area of interest has been uploaded.'});
          return;
        }
        else toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Errors uploading file.'});
      }
    } catch (error) {
      console.log(error)
    }
    toast.current.show({ severity: 'error', summary: 'Error!', detail: 'Errors uploading file'}); 
  };

  const handleMapOutput = async (polygon) => {
    if ( !polygon ) 
      return null;
    filter.aoi = polygon
    setFilter(filter)
    return polygon;
  }
    
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} position="top-right" />
      <Card>
          
      </Card>
    </div>
  );

};

export async function getStaticProps(context) {
  return {
    props: {     
      messages: (await import(`../translations/${context.locale}.json`)).default
     },
  }
}

export default DatasetFilter;
