import ExcelJS from 'exceljs';
import Taxonomies from '../data/taxonomies';
import Mapping from '../data/mapping';

import { UploadService } from '../service/uploads';
import { point, featureCollection } from '@turf/turf';

export const validateXLSFile = async (files, uploadType) => {
  let perc;
  let workbook = new ExcelJS.Workbook();
  try {
    const blob = new Blob([files[0]], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8' });
    const buffer = await blob.arrayBuffer();
    await workbook.xlsx.load(buffer);
  } catch (e) {
    return null;
  }
  let vresult = { 'validated' : 0,'data' : [], report : { 'errors': [], 'tree': [] } };
  let total_rows = 0;
  let total_valid = 0;
  
  if ( uploadType && UploadService.TYPES[uploadType] && UploadService.TYPES[uploadType].sheets ) {
    let sheets = UploadService.TYPES[uploadType].sheets;
    for ( let s=0; s<sheets.length; s+=1 ) {
      try {
        let worksheet = null;
        for ( let si=0; si<workbook.worksheets.length; si+=1 ) {
          if ( sheets[s] === workbook.worksheets[si].name.trim())
            worksheet = workbook.worksheets[si];
        }
        if ( worksheet ) {
          vresult['data'][sheets[s]] = [];
          const sheet_mapping = Mapping[uploadType+':'+sheets[s]];
          if ( sheet_mapping ) {
            worksheet.eachRow({ includeEmpty: true }, function(row, rowNumber) {
              if ( rowNumber >= sheet_mapping['startRow'] )  {
                if ( row.values[1] ){
                  row.values[1] = row.values[1].toString().trim();
                  vresult['data'][sheets[s]][rowNumber] = row.values;
                  total_rows+=1;
                }
              }
            })  
          }
          total_valid += validateSheet(sheets[s], uploadType, sheet_mapping, vresult);
          perc = (total_valid/total_rows)*100;
          vresult['validated'] = ( Number(perc).toPrecision(2));
        }
        else  {
          console.log(sheets);
        }
      } catch (e) {
        console.log(e);
        return null
      }
    }  
  } 
  return vresult; 
}

export const validateSheet = (sheet_name, uploadType, sheet_mapping, results) => {
      let code = '';
      let n,i = 1;
      let keys = [];
      
      const isGenealogy = !(uploadType === 'XLS_P' || uploadType === 'XLS_S' );
      const isGeneral = (!isGenealogy && ( sheet_name === UploadService.TYPES['XLS_P'].sheets[0] || sheet_name === UploadService.TYPES['XLS_S'].sheets[0] )); 
      const isLayer =  (!isGenealogy && ( sheet_name === UploadService.TYPES['XLS_P'].sheets[1] || sheet_name === UploadService.TYPES['XLS_S'].sheets[1] ));  
      const isCls =  (!isGenealogy && ( sheet_name === UploadService.TYPES['XLS_P'].sheets[2] || sheet_name === UploadService.TYPES['XLS_S'].sheets[3] )); 
      const isLabData = (!isGenealogy && ( sheet_name === UploadService.TYPES['XLS_P'].sheets[3] || sheet_name === UploadService.TYPES['XLS_S'].sheets[2] )); 
      if ( !isGenealogy && !isGeneral && !isCls && !isLabData && !isLayer) 
        return 0; // sheet mapping file error 
      let j = 1;
      let raw_data = results['data'][sheet_name];
      results['report']['errors'][sheet_name] = [];
      let validated_row = 0;
      for ( ; j<raw_data.length ; j+=1 ){
        let wrong = 0;
        let filled = 0;
        const row = raw_data[j];
        if ( row ) {
          try {
            /// key for a profile or sample or project === row[1]
            /// key for a profile layer or profile labdata === row[1] + '@' + row[3]
            /// key for a sample labdata === row[1] + '@' + row[2] + '@' + row[3]
            /// 
            if ( row[1] ) { // no principal key -> skip row
              if (( !isLayer && !isLabData && keys[row[1]]) || 
                  ( uploadType === 'XLS_P' && ( isLayer || isLabData ) && ( !row[3] || keys[row[1]+'@'+row[3]] ) ) || 
                  ( uploadType === 'XLS_S' && isLabData && ( !row[3] || !row[2] || keys[row[1]+'@'+row[2]+'@'+row[3]] ) ) ){
                  results['report']['errors'][sheet_name].push(['?',j,1,'-k']);  /// wrong key or duplicate key
              }
              else {
                let key = row[1];
                if ( ( isLayer || isLabData ) && uploadType === 'XLS_P' )
                  key = row[1]+'@'+row[3];
                else if ( isLabData && uploadType === 'XLS_S' )
                  key = row[1]+'@'+row[2]+'@'+row[3];
                keys[key] = j;
                wrong = 0;
                filled = 0;
                let lmap = sheet_mapping['size'];
                for ( i=1; i<row.length && i<=lmap; i+=1 ){
                  code = '';
                  if ( row[i] && row[i].toString().trim() !== '' ){
                    switch ( sheet_mapping[i].check ){
                      case 'boolean':
                        let vb = row[i].toString().trim().toLowerCase();
                        if ( vb !== 't' && vb !== 'f' && vb !== 'yes' && vb !== 'no' && vb !== 'true' && vb !== 'false' && vb !== 'un')   
                            code = '-b'; //'Wrong boolean, allowed values yes/no, t/f, true/false or 'un'  for True/False or none, '                       
                        else {
                          if ( vb === 't' || vb === 'yes' || vb === 'true' )
                            row[i] = true;
                          else if ( vb === 'f' || vb === 'no' || vb === 'false' )
                             row[i] = false;
                          else row[i] = null; 
                        }
                        break;
                      case 'date':
                        if ( ( typeof row[i] === 'string' ||  row[i] instanceof String ) )  
                        {
                          if ( row[i].trim() === 'nd' )
                            row[i] = null;
                          else {
                            n = row[i].split('/');
                            if ( n[0] === '0' || n[0] === '00')
                              n[0] = '01';
                            if ( n.length === 3 && (n[1] === '0' || n[1] === '00'))
                              n[1] = '01';
                            if ( ( n.length === 3 && isNaN(new Date (n[2]+'-'+n[1]+'-'+n[0])) )  ||
                                 ( n.length === 2 && isNaN(new Date (n[1]+'-'+n[0]+'-01')) ) )
                              code = '-d'; // 'not valid date, allowed format is ISO YYYY-MM-DD ' 
                            else if ( n.length === 3 )  
                               row[i] = new Date (n[2]+'-'+n[1]+'-'+n[0]);   
                            else if ( n.length === 2 )
                               row[i] = new Date (n[1]+'-'+n[0]+'-01');
                          }    
                        }
                        break;
                      case 'numeric':
                        n = Number(row[i]);
                        if (isNaN(n))
                          code = '-n'; // 'not valid number' 
                        else row[i] = n;                       
                        break;
                      case 'numeric(%)':
                        n = Number(row[i]);
                        if (isNaN(n) || n < 0 || n > 100 )
                          code = '-%'; //'not valid percentage [0..100] ' 
                        else row[i] = n;                         
                        break;
                      case 'numeric(0)':
                        n = Number(row[i]);
                        if (isNaN(n) || n < 0 )
                          code = '-0'; //'not valid positive number'  
                        else row[i] = n;                        
                        break;
                      case 'latitude':
                        n = Number(row[i]);
                        if (isNaN(n) || n <= -90 || n >= 90 )
                          code = '-lat'; //'not valid latitude in decimal degree'                         
                        else row[i] = n; 
                        break;
                      case 'longitude':
                        n = Number(row[i]);
                        if (isNaN(n) || n <= -180 || n >= 180 )
                          code = '-lon'; //'not valid longitude in decimal degree'                         
                        else row[i] = n; 
                        break;
                      case 'taxonomy':
                        let no_t = true;
                        if ( typeof row[i] === 'string' ||  row[i] instanceof String )  {
                          if ( sheet_mapping[i]['t'] && Taxonomies[sheet_mapping[i]['t']] ) {
                            Object.keys(Taxonomies[sheet_mapping[i]['t']]).forEach( (element) => {
                              if ( element.trim().toLowerCase() === row[i].trim().toLowerCase() )
                                  no_t = false; 
                            });
                          }
                        }
                        if ( no_t ) {     
                          code = '-t';  
                        }
                        else row[i] = row[i].trim();   
                        break;
                      default:  //// case Richtext!!!!!!!!!!!!
                        if ( typeof row[i] !== 'string' && !( row[i] instanceof String ) ) {
                           // no Rich text!!!!!!!!!!!!
                          if ( row[i]['richText'] && row[i]['richText'][0] && row[i]['richText'][0]['text'] )  
                            row[i] = row[i]['richText'][0]['text'];
                          else code = '-?';                        
                        }
                      break;
                    }
                    filled +=1;
                    if ( code != '' ) {
                      results['report']['errors'][sheet_name].push([key,j,i,code]);
                      wrong += 1;
                    } 
                  }  
                }
                if ( !results['report']['tree'][row[1]] )
                  results['report']['tree'][row[1]] = [];
                if ( !results['report']['tree'][row[1]]['wrong'] )
                  results['report']['tree'][row[1]]['wrong'] = wrong;
                else results['report']['tree'][row[1]]['wrong'] += wrong;
                let perc = (filled/lmap)*100;
                perc = Number(perc).toPrecision(2);
                if ( isGeneral )
                  results['report']['tree'][row[1]]['Main'] = perc + ':' + wrong;
                else if ( isLayer )
                  results['report']['tree'][row[1]]['Layer '+ key] = perc + ':' + wrong;
                else if ( isLabData )
                  results['report']['tree'][row[1]]['Lab Data '+ key] = perc + ':' + wrong;
                else if ( isCls )
                  results['report']['tree'][row[1]]['Classification'] = perc + ':' + wrong;
                if ( results['report']['errors'][sheet_name]['total_errors'] )
                  results['report']['errors'][sheet_name]['total_errors'] += wrong;
                else results['report']['errors'][sheet_name]['total_errors'] = wrong
                if ( wrong === 0 )
                  validated_row += 1;
                if ( results['report']['total_errors'] )
                  results['report']['total_errors'] += wrong;
                else 
                  results['report']['total_errors'] = wrong;
              }
            }
          } catch (e) {
            console.log(e);
          }
        }    
      }
      return validated_row;
} 

export const createObjects = (data, uploadType) => {
  if ( uploadType === 'XLS_P')
    return createObjectsProfiles(data)
  else if ( uploadType === 'XLS_S')
    return createObjectsSamples(data)
  else if ( uploadType === 'XLS_PG' || uploadType === 'XLS_SG' )
    return createObjectsGenealogy(data)
  else return null; 
}   

export const createObjectsProfiles = (data) => {
//// XLS profile sheets
  let uploadType = 'XLS_P'
  const sheets = UploadService.TYPES[uploadType].sheets;
  let fixtures = {}
  // General  
  let model = null;
  let field = null;
  let level = null;
  let value = null; 
  let taxonomy = null;
  let sheet_mapping = Mapping[uploadType+':'+sheets[0]];
  let sheet = data[sheets[0]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1];
        let _id = row[1];
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;
            taxonomy = sheet_mapping[j].t;
            if ( !fixtures[model] )
              fixtures[model] = { };
            if ( model === 'NotCultivated' )
              _id = id + '@' + value;
            else _id = id;
            if ( !fixtures[model][_id] ){  
              fixtures[model][_id] = {};
              fixtures[model][_id]['id'] = _id;
            }
            fixtures[model][_id][field] = row[j];
            if ( model !== 'ProfileGeneral' && model !== 'NotCultivated' && model !== 'Cultivated' ) { 
              let m = model.toLowerCase().trim()
              fixtures['ProfileGeneral'][id][m] = id; 
            }
            if ( model === 'Cultivated' || model === 'NotCultivated' ) {
              if ( !fixtures['LandUse'] ) 
                fixtures['LandUse'] = { }
              if ( !fixtures['LandUse'][id] ) 
                fixtures['LandUse'][id] = { id: id }
              if ( model === 'Cultivated' ) 
                fixtures['LandUse'][_id]['cultivated'] = id; 
              if ( model === 'NotCultivated' ) 
                fixtures['NotCultivated'][_id]['land_use'] = id; 
            }
          }  
        }
      }
    } catch (e) {
      console.log(e);
    }
  } 
  
  // Layer  LayerRedoximorphicColour  LayerStructure
  sheet_mapping = Mapping[uploadType+':'+sheets[1]];
  sheet = data[sheets[1]]; 
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let l_id = row[1] + '@' + row[3];
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if (  row[j] === 0 || (row[j] && row[j].toString().trim() != '') ){ 
            let _id = l_id; 
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;           
            taxonomy = sheet_mapping[j].t;
            if ( !fixtures[model] )
              fixtures[model] = { };
            if ( model === 'LayerRedoximorphicColour' || model === 'LayerStructure' )
              _id = _id + '@' + value;
            if ( !fixtures[model][_id] )  
              fixtures[model][_id] = { id: _id };
            fixtures[model][_id][field] = row[j];
            if ( model !== 'ProfileLayer' && model !== 'LayerRedoximorphicColour' && model !== 'LayerStructure' ) { 
              let m = model.toLowerCase().trim();
              if ( !fixtures['ProfileLayer'] )
                fixtures['ProfileLayer'] = {};
              if ( !fixtures['ProfileLayer'][l_id] )
                fixtures['ProfileLayer'][l_id] = { };
              fixtures['ProfileLayer'][l_id][m] = _id; 
            }
            if ( model === 'LayerRedoximorphicColour' ) {
              if ( !fixtures['LayerRedoximorphicFeatures'] )
                fixtures['LayerRedoximorphicFeatures'] = { };
              if ( !fixtures['LayerRedoximorphicFeatures'][l_id] )
                fixtures['LayerRedoximorphicFeatures'][l_id] = { id : l_id };
              fixtures['LayerRedoximorphicColour'][_id]['features'] = l_id; 
            }
            if ( model === 'LayerStructure' ) {
              fixtures['LayerStructure'][_id]['layer'] = l_id;
              fixtures['LayerStructure'][_id][level] = value; 
            }
          }
        }
      }
      
    } catch (e) {
        console.log(e);
    } 
  } 
  // labdata  
  sheet_mapping = Mapping[uploadType+':'+sheets[3]];
  sheet = data[sheets[3]];
  fixtures['LabData'] = { };
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1] + '@' + row[3];
        if ( fixtures['ProfileLayer'][id] )
          fixtures['ProfileLayer'][id]['labdata'] = id;
        else console.log("Warning obj: " + id);
        if ( !fixtures['LabData'][id] ) 
          fixtures['LabData'][id] =  {};
        fixtures['LabData'][id]['id'] = id;
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] === 0 || (row[j] && row[j].toString().trim() != '') ){  
            field = sheet_mapping[j].f;
            fixtures['LabData'][id][field] = row[j];
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  } 
  // classification  
  sheet_mapping = Mapping[uploadType+':'+sheets[2]];
  sheet = data[sheets[2]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1];
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if (  row[j] === 0 || (row[j] && row[j].toString().trim() != '') ){  
            field = sheet_mapping[j].f;
            taxonomy = sheet_mapping[j].t;
            if ( fixtures['ProfileGeneral'][id] && field !== 'profile' ) 
              fixtures['ProfileGeneral'][id][field] = row[j]; 
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  }
  
  // re-organize data
  let result = {}
  let models = Object.keys(fixtures); 
  for ( let k = 0; k < models.length; k+=1 ){
    result[models[k]] = [];
    if ( fixtures[models[k]] ) {
      let objs = Object.keys(fixtures[models[k]]);
      for ( let c = 0; c < objs.length; c+=1 ){
        let obj = fixtures[models[k]][objs[c]];
        if ( obj ) 
          result[models[k]].push(obj);  
      }
    }
  }  
  let pointsdata = [];
  let depthdata = [];
  let datedata = [];
  let data_obj = {};

  /// geo points
  model = fixtures['ProfileGeneral'];
  let keys = Object.keys(model); 
  for ( let k = 0; k < keys.length; k+=1 ){
    let obj = model[keys[k]];
    if ( obj && obj['id'] )
      pointsdata[ obj['id'] ] = [ obj['lon_wgs84'], obj['lat_wgs84'] ]
      datedata[ obj['id'] ] = obj['date']
  }
  /// depth data for points
  model = fixtures['ProfileLayer'];
  keys = Object.keys(model); 
  for ( let k = 0; k < keys.length; k+=1 ){
    let obj = model[keys[k]];
    if ( obj && obj['id'] )
      depthdata[ obj['id'] ] = [ obj['upper'], obj['lower'] ]
  }
  /*
  models = Object.keys(fixtures); 
  for ( let k = 0; k < models.length; k+=1 ){
    let points = [];
    data_obj[models[k]] = [];
    if ( fixtures[models[k]] ) {
      let objs = Object.keys(fixtures[models[k]]);
      for ( let c = 0; c < objs.length; c+=1 ){
        let p_id = null;
        let obj = fixtures[models[k]][objs[c]];
        if ( obj ) {
          data_obj[models[k]].push(obj);
          if (obj['id'] )
            p_id = obj['id'].split('@')[0];
          if ( models[k] === 'LabData' && depthdata[ obj['id'] ] ){
            obj['upper'] = depthdata[ obj['id'] ][0];
            obj['lower'] = depthdata[ obj['id'] ][1];
          }
          if ( models[k] === 'LabData' && datedata[ p_id ] ){
            obj['date'] = datedata[ p_id ];
          }
          if ( pointsdata[p_id] )
            points.push( point ( pointsdata[p_id], obj, { id: objs[c] } ));
          else console.log ( p_id );    
        }
      }
       
    }
    
  } 
  */
  ////GeoJSON......30 layer
  return result
}

export const createObjectsSamples = (data) => {
//// XLS profile sheets
  let uploadType = 'XLS_S'
  const sheets = UploadService.TYPES[uploadType].sheets;
  let fixtures = {}
  // General  
  let model = null;
  let field = null;
  let level = null;
  let value = null; 
  let taxonomy = null;
  let sheet_mapping = Mapping[uploadType+':'+sheets[0]];
  let sheet = data[sheets[0]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1];
        let _id = row[1];
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;
            taxonomy = sheet_mapping[j].t;
            if ( !fixtures[model] )
              fixtures[model] = { };
            if ( model === 'SampleNotCultivated' )
              _id = id + '@' + value;
            else _id = id;
            if ( !fixtures[model][_id] ){  
              fixtures[model][_id] = {};
              fixtures[model][_id]['id'] = _id;
            }
            fixtures[model][_id][field] = row[j];
            if ( model !== 'SampleGeneral' && model !== 'SampleNotCultivated' && model !== 'SampleCultivated' ) { 
              let m = model.toLowerCase().trim()
              fixtures['SampleGeneral'][id][m] = id; 
            }
            if ( model === 'SampleCultivated' || model === 'SampleNotCultivated' ) {
              if ( !fixtures['SampleLandUse'] ) 
                fixtures['SampleLandUse'] = { }
              if ( !fixtures['SampleLandUse'][id] ) 
                fixtures['SampleLandUse'][id] = { id: id }
              if ( model === 'SampleCultivated' ) 
                fixtures['SampleLandUse'][_id]['cultivated'] = id; 
              if ( model === 'SampleNotCultivated' ) 
                fixtures['SampleNotCultivated'][_id]['land_use'] = id; 
            }
          }  
        }
      }
    } catch (e) {
      console.log(e);
    }
  } 
  // Layer  LayerRedoximorphicColour  LayerStructure
  sheet_mapping = Mapping[uploadType+':'+sheets[1]];
  sheet = data[sheets[1]]; 
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let l_id = row[1] + '@' + row[3];
        let s_id = row[1]
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( typeof row[j] !== "undefined" &&  row[j].toString().trim() != '' ){ 
            let _id = l_id; 
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;           
            taxonomy = sheet_mapping[j].t;
            if ( !fixtures[model] )
              fixtures[model] = { };
            if ( model === 'SampleLayerRedoximorphicColour' || model === 'SampleLayerStructure' )
              _id = _id + '@' + value;
            if ( !fixtures[model][_id] )  
              fixtures[model][_id] = { id: _id };
            fixtures[model][_id][field] = row[j];
            if ( model === 'SampleLayer' ){ 
              if ( !fixtures['SampleGeneral'] )
                fixtures['SampleGeneral'] = {};
              if ( !fixtures['SampleGeneral'][s_id] ){ 
                fixtures['SampleGeneral'][s_id] = { };
              };
            }
            if ( model !== 'SampleLayer' && model !== 'SampleLayerRedoximorphicColour' && model !== 'SampleLayerStructure' ) { 
              let m = model.toLowerCase().trim();
              if ( !fixtures['SampleLayer'] )
                fixtures['SampleLayer'] = {};
              if ( !fixtures['SampleLayer'][l_id] ){ 
                fixtures['SampleLayer'][l_id] = { };
              };
              fixtures['SampleLayer'][l_id][m] = _id; 
            }
            if ( model === 'LayerRedoximorphicColour' ) {
              if ( !fixtures['LayerRedoximorphicFeatures'] )
                fixtures['LayerRedoximorphicFeatures'] = { };
              if ( !fixtures['LayerRedoximorphicFeatures'][l_id] )
                fixtures['LayerRedoximorphicFeatures'][l_id] = { id : l_id };
              fixtures['LayerRedoximorphicColour'][_id]['features'] = l_id; 
            }
            if ( model === 'LayerStructure' ) {
              fixtures['LayerStructure'][_id]['layer'] = l_id;
              fixtures['LayerStructure'][_id][level] = value; 
            }
          }
        }
      }
      
    } catch (e) {
        console.log(e);
    } 
  } 
  // labdata  
  sheet_mapping = Mapping[uploadType+':'+sheets[3]];
  sheet = data[sheets[3]];
  fixtures['LabData'] = { };
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1] + '@' + row[3];
        if ( fixtures['ProfileLayer'][id] )
          fixtures['ProfileLayer'][id]['labdata'] = id;
        else console.log("Warning obj: " + id);
        if ( !fixtures['LabData'][id] ) 
          fixtures['LabData'][id] =  {};
        fixtures['LabData'][id]['id'] = id;
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] === 0 || (row[j] && row[j].toString().trim() != '') ){  
            field = sheet_mapping[j].f;
            fixtures['LabData'][id][field] = row[j];
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  } 
  // classification  
  sheet_mapping = Mapping[uploadType+':'+sheets[2]];
  sheet = data[sheets[2]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1];
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if (  row[j] === 0 || (row[j] && row[j].toString().trim() != '') ){  
            field = sheet_mapping[j].f;
            taxonomy = sheet_mapping[j].t;
            if ( fixtures['ProfileGeneral'][id] && field !== 'profile' ) 
              fixtures['ProfileGeneral'][id][field] = row[j]; 
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  }
  
  // re-organize data
  let result = {}
  let models = Object.keys(fixtures); 
  for ( let k = 0; k < models.length; k+=1 ){
    result[models[k]] = [];
    if ( fixtures[models[k]] ) {
      let objs = Object.keys(fixtures[models[k]]);
      for ( let c = 0; c < objs.length; c+=1 ){
        let obj = fixtures[models[k]][objs[c]];
        if ( obj ) 
          result[models[k]].push(obj);  
      }
    }
  }  
  let pointsdata = [];
  let depthdata = [];
  let datedata = [];
  let data_obj = {};

  /// geo points
  model = fixtures['ProfileGeneral'];
  let keys = Object.keys(model); 
  for ( let k = 0; k < keys.length; k+=1 ){
    let obj = model[keys[k]];
    if ( obj && obj['id'] )
      pointsdata[ obj['id'] ] = [ obj['lon_wgs84'], obj['lat_wgs84'] ]
      datedata[ obj['id'] ] = obj['date']
  }
  /// depth data for points
  model = fixtures['ProfileLayer'];
  keys = Object.keys(model); 
  for ( let k = 0; k < keys.length; k+=1 ){
    let obj = model[keys[k]];
    if ( obj && obj['id'] )
      depthdata[ obj['id'] ] = [ obj['upper'], obj['lower'] ]
  }
  /*
  models = Object.keys(fixtures); 
  for ( let k = 0; k < models.length; k+=1 ){
    let points = [];
    data_obj[models[k]] = [];
    if ( fixtures[models[k]] ) {
      let objs = Object.keys(fixtures[models[k]]);
      for ( let c = 0; c < objs.length; c+=1 ){
        let p_id = null;
        let obj = fixtures[models[k]][objs[c]];
        if ( obj ) {
          data_obj[models[k]].push(obj);
          if (obj['id'] )
            p_id = obj['id'].split('@')[0];
          if ( models[k] === 'LabData' && depthdata[ obj['id'] ] ){
            obj['upper'] = depthdata[ obj['id'] ][0];
            obj['lower'] = depthdata[ obj['id'] ][1];
          }
          if ( models[k] === 'LabData' && datedata[ p_id ] ){
            obj['date'] = datedata[ p_id ];
          }
          if ( pointsdata[p_id] )
            points.push( point ( pointsdata[p_id], obj, { id: objs[c] } ));
          else console.log ( p_id );    
        }
      }
       
    }
    
  } 
  */
  ////GeoJSON......30 layer
  return result
}

export const createObjectsGenealogy = (data,uploadType) => {
//// XLS profile sheets
  const sheets = UploadService.TYPES[uploadType].sheets;
  let fixtures = {}
  // General  
  let model = null;
  let field = null;
  let level = null;
  let value = null; 
  let taxonomy = null;
  let sheet_mapping = Mapping[uploadType+':'+sheets[0]];
  for ( let z = 0; z < 2; z+=1 ) {
    let sheet = data[sheets[z]];
    for ( let i = 0; i < sheet.length; i+=1 ) {
      try {
        let row = sheet[i];
        if ( row ) {
          let id =  row[1];
          for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
            if (  row[j] === 0 || ( row[j] && row[j].toString().trim() != '' )){  
              model = sheet_mapping[j].m;
              field = sheet_mapping[j].f;
              if ( !fixtures[model] )
                fixtures[model] = { };
              fixtures[model][_id][field] = row[j];
            }  
          }
        }
      } catch (e) {
        console.log(e);
      }
    }
  }
  // re-organize data
  let result = {}
  let models = Object.keys(fixtures); 
  for ( let k = 0; k < models.length; k+=1 ){
    result[models[k]] = [];
    if ( fixtures[models[k]] ) {
      let objs = Object.keys(fixtures[models[k]]);
      for ( let c = 0; c < objs.length; c+=1 ){
        let obj = fixtures[models[k]][objs[c]];
        if ( obj ) 
          result[models[k]].push(obj);  
      }
    }
  }  
  return result
}






 