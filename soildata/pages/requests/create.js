import React, { useEffect, useRef, useState, useCallback  } from 'react';
import { IndicatorService } from '../../service/indicators';
import { RequestService } from '../../service/requests';
import { useTranslations } from 'next-intl';
import { useUser } from '../../context/user';
import { useRouter } from 'next/router';
import { Steps } from 'primereact/steps';
import { Toast } from 'primereact/toast';
import { Button } from 'primereact/button';
import { RadioButton } from 'primereact/radiobutton';
import { Dropdown } from 'primereact/dropdown';
import dynamic from "next/dynamic"
import Mapping from '../../data/mapping';
import { Tree } from 'primereact/tree';

const MyMap = dynamic(() => import("../../components/RequestMakerMap"), { ssr:false })

export default function Page({ children })  {
  const t = useTranslations('default');
  const router = useRouter();
  const toast = useRef(null);
  const user = useUser();
  
  const [step, setStep] = useState(0);
  const wizardItems = [
    { label: 'who', command: () =>  toast.current.show({ severity: 'info', summary: 'Who section', detail: 'User or group selection.' }) },
    { label: 'what', command: () =>  toast.current.show({ severity: 'info', summary: 'What section', detail: 'Data type selection' })  },
    { label: 'where', command: () =>  toast.current.show({ severity: 'info', summary: 'Where section', detail: 'Area of Interest (AOI) and Depth selection' })  },
    { label: 'when', command: () =>  toast.current.show({ severity: 'info', summary: 'When section', detail: 'Data reference period selection.' })  },
  ];

  const [name, setName] =  useState(null); 
  const [who , setWho] =  useState(null); 
  const [whoList, setWhoList] =  useState([]); 

  const [indTypesNodes, setIndTypesNodes] =  useState([]);  
  const [indicators, setIndicators] =  useState([]);
  const [indicator, setIndicator] =  useState(null);  
  
  
  const [mapProps, setMapProps] =  useState(null);
  const [gsLayers, setGsLayers] =  useState(null); 
  const [aoi, setAoi] =  useState(null); 
  const [depth, setDepth] =  useState(null);
  const [data_from, setDate_from] =  useState(null); 
  const [data_to, setDate_to] =  useState(null); 
  const [gsLayer, setGsLayer] = useState(null); 
  const [avail, setAvail] = useState(null); 

  const createIndicatorTree = (_indicators) =>  {
    const tree = {};
    const nodes = [];
    if (_indicators )  {
      for ( let i = 0; i< _indicators.length; i+=1 ) {
        const ind = _indicators[i];
        if ( !tree[ind.domain] )
          tree[ind.domain] =  {}
        if ( !tree[ind.domain][ind.indicator] )
          tree[ind.domain][ind.indicator] =  {}
        tree[ind.domain][ind.indicator][ind.measure] =  ind.unit   
      }
      const xkeys = Object.keys(tree);
      for ( let x=0; x < xkeys.length; x+=1 )  {
        console.log(xkeys[x]);    
        let nodex = {
          "key": x.toString(),
          "label": xkeys[x],
          "data": xkeys[x],
          "icon": "pi pi-fw pi-folder",
          "children": []
        }
        const ykeys = Object.keys(tree[xkeys[x]]);
        for ( let y=0; y < ykeys.length; y+=1 )  {
          console.log(ykeys[y]);    
          let nodey = {
            "key": x.toString()+'-'+y.toString(),
            "label": ykeys[y],
            "data": xkeys[x] + '/' + ykeys[y],
            "icon": "pi pi-fw pi-folder",
            "children": []
          }
          const zkeys = Object.keys(tree[xkeys[x]][ykeys[y]]);
          for ( let z=0; z < zkeys.length; z+=1 )  {
            console.log(zkeys[z]);    
            let nodez = {
              "key": x.toString()+'-'+y.toString()+'-'+z.toString(),
              "label": zkeys[z],
              "data": xkeys[x] + '/' + ykeys[y] + '/' + zkeys[z],
              "icon": "pi pi-fw pi-folder",
              "children": []
            }
            nodey.children.push(nodez); 
          }
          nodex.children.push(nodey); 
        }
        nodes.push(nodex); 
      } 
      setIndTypesNodes(nodes);
    } 
  }

  useEffect(() => {
      const fetchMap = async () => {
        const reqMap = {
          layers : { 
            aoi: null,
            gsLayers: gsLayers,
            points: avail,
          },
          label: 'AOI selection',
          token: user.userData.access_token,
        };
        setMapProps(reqMap);  
      }
      if ( avail && gsLayers ) 
        fetchMap();
    }, [gsLayers,avail]);  // eslint-disable-line 

  useEffect(() => {
    const fetchIndicators = async () => {
      const indicators = await IndicatorService.getTypes()
      setIndicators(indicators);
      createIndicatorTree(indicators);
    }
    fetchIndicators();  
  },[]);  

  useEffect(() => {
    if ( user.userData && user.userData.forbidden2 !== null && user.userData.forbidden2 )
        router.push(`/401`);
    let _whoList = [];
    _whoList.push({ email: user.userData.email, name: user.userData.preferred_username, id: user.userData.id });
    for( let g=0; g < user.userData.groups.length; g+=1 )
      if ( user.userData.groups [g] !== "anonymous" )
        _whoList.push( { name: user.userData.groups [g] , id: user.userData.groups [g] } );
    setWhoList(_whoList);
    setWho(_whoList[0]);
    const fetchAvail = async () => {
      const _avail = await IndicatorService.getAvail()
      setAvail(_avail);
    }
    fetchAvail(); 
    setGsLayers( [{ name: 'GADM Spain level1', value:'geonode:gadm41_esp_1'},
                  {name: 'GADM Spain level2', value:'geonode:gadm41_esp_2'},
                  {name: 'GADM Spain level3', value:'geonode:gadm41_esp_3'},
                  {name: 'GADM Jordan level1', value:'geonode:gadm41_jor_1'}] ); 
  },[user]);  // eslint-disable-line
  
  if  ( !user || !whoList || !indicators )
    return <></>
  else
    return (
    <div className="layout-dashboard">
      <Toast ref={toast} />
      <div className="card">
        <h4>Data Request Creation</h4>
        <div>BLAH BLAH BLAH</div>

        <Steps model={wizardItems} activeIndex={step} onSelect={(e) => setStep(e.index)} readOnly={false} />
        
        <div className="shadow-4 m-4" >
          {step === 0 && (
              <div class="flex h-4rem bg-primary font-bold justify-content-center p-4 border-round">
                  <i className="pi pi-fw pi-user mr-2 text-2xl" />
                  <p className="m-0 text-lg">Who is the applicant?</p>
              </div>)}
          {step === 0 && whoList && whoList.map((whoItem) => {
            return (
              <div key={whoItem.id} className="block p-5">
                  <RadioButton inputId={whoItem.id} name="who" value={whoItem.id} onChange={(e) => setWho(e.value)} checked={who === whoItem.id} />
                  <label htmlFor={whoItem.id} className="ml-2">{whoItem.email? 'USER: ' + whoItem.name : 'GROUP: ' + whoItem.name }</label>
              </div> 
            );
          })}
          {step === 1 && (
            <>
            <div class="flex h-4rem bg-primary font-bold justify-content-center p-4 border-round">
                <i className="pi pi-fw pi-user mr-2 text-2xl" />
                <p className="m-0 text-lg">What is the required data?</p>
            </div>
            <div className="grid">
              <div className="col-12">
                <div className="card">
                  <h5>Select Indicators </h5>
                    <Tree value={indTypesNodes} selectionMode="checkbox" selectionKeys={indicator} onSelectionChange={(e) => setIndicator(e.value)}  />
                </div>
              </div>
            </div> 
            </>   
          )}
          {step === 2 && (
            <div className="flex h-4rem bg-primary font-bold justify-content-center p-4 border-round">
                <i className="pi pi-fw pi-user mr-2 text-2xl" />
                <p className="m-0 text-lg">Select the Area of Interest (AOI) and depth</p>
            </div>
          )}
          {step === 2 && mapProps && (
            <div className="card">
              <h5>{ mapProps ? mapProps.label : 'AOI Selection' }</h5>
              <MyMap toast={toast} setAoi={setAoi}  data={mapProps} />
            </div>
          )} 
          {step === 2 && !mapProps && (
            <div className="card">
              <div className="p-text-center">
                <h2>Loading</h2>
                <i className="pi pi-spin pi-spinner" style={{ fontSize: '2em' }} />
              </div>
            </div>
          )} 
          {step === 3 && (
            <div className="flex h-4rem bg-primary font-bold justify-content-center p-4 border-round">
                <i className="pi pi-fw pi-user mr-2 text-2xl" />
                <p className="m-0 text-lg">When</p>
            </div>  
          )}
          <div className="flex justify-content-center align-items-center py-5 px-3  ">
            <Button type="button" label="Send" disabled icon="pi pi-save" style={{ width: 'auto' }} />
          </div>
        </div>
      </div>
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

/*
<!--- 
        Kriging is a geostatistical interpolation method used to predict values at unsampled locations based on values from known locations. It's widely used in fields such as geology, environmental science, mining, hydrology, and more. Kriging not only estimates unknown values but also provides a measure of the estimation uncertainty.

Key Concepts of Kriging:
1. Spatial Autocorrelation
Kriging assumes that things that are close in space are more similar than things that are far apart. This spatial dependence is quantified using a variogram or covariance function.

2. Variogram
A variogram models how data similarity decreases with distance:

Nugget: Variability at very small scales (or measurement error).

Sill: The plateau representing the total variance.

Range: The distance beyond which data points are no longer correlated.

3. Types of Kriging
There are several flavors of Kriging, depending on assumptions and data properties:

Simple Kriging: Assumes known and constant mean.

Ordinary Kriging: Assumes an unknown but constant mean over the area.

Universal Kriging: Allows the mean to vary spatially (modeled as a trend).

Indicator Kriging: For categorical or binary data.

Co-Kriging: Uses secondary variables in addition to the primary variable.
*/

