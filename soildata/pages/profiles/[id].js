import React from 'react';
import Footer from '../../components/Footer';
import ToDo from '../../components/ToDo';
import {useTranslations} from 'next-intl';
import { useParams } from 'next/navigation'
import { Button } from 'primereact/button';
import { Panel } from 'primereact/panel';
import { Message } from 'primereact/message';
import { Toast } from 'primereact/toast';
import { useUser } from '../../context/user';
import Taxonomies from '../../data/taxonomies';
import Mapping from '../../data/mapping';
//import Test from '../../data/test';

export default function Page()  {
  const params = useParams(); 
  const t = useTranslations('default');

  return (
    <>
      <ToDo />
      <Footer />
    </>
  );
};

const createModelsGeoJSON = ( data ) => {
    /* First sheet: XLS_P:General and Surface*/
    const sheets = ['General and Surface','Layer descriptions','Soil classification','Lab data'];
    const id = params.id;
    const models_map = {};
    const models_names = [];
    const models_data = {};
    const models_points  = {};
    let i;
    for ( let s=0; s<4; s+=1 ) {
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
        if ( row && row[1] && row[1] === id ) {
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
      indicator: indicator,
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}



