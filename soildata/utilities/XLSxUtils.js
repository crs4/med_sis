import ExcelJS from 'exceljs';
import Mapping from '../data/mapping';

import { UploadService } from '../service/uploads';

export const validateXLSFile = async (files, uploadType, taxonomies) => {
  let perc;
  let workbook = new ExcelJS.Workbook();
  try {
    const blob = new Blob([files[0]], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8' });
    const buffer = await blob.arrayBuffer();
    await workbook.xlsx.load(buffer);
  } catch (e) {
    console('Error reading file')
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
          if ( sheets[s].trim() === workbook.worksheets[si].name.trim())
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
          if ( uploadType === 'XLS_P')
            total_valid += validatePointSheet(taxonomies, sheets[s], sheet_mapping, vresult);
          else if ( uploadType === 'XLS_PJ' || uploadType === 'XLS_PH' )
            total_valid += await validateSingleSheet(taxonomies, sheets[s], sheet_mapping, vresult);
          perc = (total_valid/total_rows)*100;
          vresult['validated'] =  Math.trunc(Number(perc).toPrecision(4));
        }
        else  {
          console.log('Error worksheet'+sheets[s]);
        }
      } catch (e) {
        console.log(e);
      }
    }  
  } 
  return vresult; 
}

const validate_row = (taxonomies, row, j, key, sheet_name, sheet_mapping, results) => {
  let i = 1;
  let n;
  let wrong = 0;
  let filled = 0;           
  let l = sheet_mapping['size'];
  for ( i=1; i<row.length && i<=l; i+=1 ){
    let code = '';
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
          let tax = null;
          if ( typeof row[i] === 'string' ||  row[i] instanceof String || Number.isInteger( row[i]))  
          {
            if ( sheet_mapping[i]['t'] && taxonomies[sheet_mapping[i]['t']] ) {
              Object.keys(taxonomies[sheet_mapping[i]['t']]).forEach( (element) => {
                if ( element.trim().toLowerCase() === row[i].toString().trim().toLowerCase() )
                    tax = sheet_mapping[i]['t'] + ":" + element;
              });
            }
          }
          if ( tax ) {     
            row[i] = tax;  
          }
          else code = '-t';
          break;
        default: /// others ('text') 
          //// case Richtext!!!!!!!!!!!!
          if ( typeof row[i] !== 'string' && !( row[i] instanceof String ) ) {
            if (row[i].text)
              row[i] = row[i].text;
            else if ( row[i]['richText'] && row[i]['richText'][0] && row[i]['richText'][0]['text'] )  
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
  return { wrong, filled };
}
              
export const validateSingleSheet = async (taxonomies, sheet_name, sheet_mapping, results) => {
      let keys = [];
      let raw_data = results['data'][sheet_name];
      results['report']['errors'][sheet_name] = [];
      let validated_row = 0;
      for ( let j = sheet_mapping['startRow']; j<raw_data.length ; j+=1 ){
        let wrong = 0;
        let filled = 0;
        const row = raw_data[j];
        if ( row ) {
          try {
            /// key for a profile or sample or project === row[1]
            /// key for a profile layer or profile labdata === row[1] + '@' + row[3]
            /// key for a sample labdata === row[1] + '@' + row[2] + '@' + row[3]
            /// 
            if ( !row[1] ) 
              results['report']['errors'][sheet_name].push(['?',j,1,'-k']);  /// wrong key
            else { // no primary key -> skip row
              if ( !row[1] || keys[row[1]] )  {
                  results['report']['errors'][sheet_name].push(['?',j,1,'-k']);  /// wrong key or duplicate key
              }
              else {
                let key = row[1];
                keys[key] = j;
                wrong = 0;
                filled = 0;
                let lmap = sheet_mapping['size'];
                let res = validate_row(taxonomies, row, j, key, sheet_name, sheet_mapping, results);
                if (res) {
                  wrong = res.wrong;
                  filled = res.filled;
                }
                if ( !results['report']['tree'][row[1]] )
                  results['report']['tree'][row[1]] = [];
                if ( !results['report']['tree'][row[1]]['wrong'] )
                  results['report']['tree'][row[1]]['wrong'] = wrong;
                else results['report']['tree'][row[1]]['wrong'] += wrong;
                let perc = (filled/lmap)*100;
                perc = Number(perc).toPrecision(2);
                results['report']['tree'][row[1]]['Main'] = perc + ':' + wrong;
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

export const validatePointSheet = (taxonomies, sheet_name, sheet_mapping, results) => {
      let keys = [];
      
      const isGeneral = ( sheet_name === UploadService.TYPES['XLS_P'].sheets[0] ); 
      const isLayer =  ( sheet_name === UploadService.TYPES['XLS_P'].sheets[1] );  
      const isLabData =  ( sheet_name === UploadService.TYPES['XLS_P'].sheets[2] ); 
      const isLabData_sampling = (sheet_name === UploadService.TYPES['XLS_P'].sheets[3]); 
      if ( !isGeneral && !isLabData && !isLabData_sampling && !isLayer) {
        return 0; // sheet mapping file error 
      }  
      if ( !results || !results['data'] || !results['data'][sheet_name] ){
        return 0 ; // sheet mapping file error 
      }  

      let raw_data = results['data'][sheet_name];
      results['report']['errors'][sheet_name] = [];
      let validated_row = 0;
      
      for ( let j = sheet_mapping['startRow']; j<raw_data.length ; j+=1 ){
        let wrong = 0;
        let filled = 0;
        const row = raw_data[j];
        if ( row ) {
          try {
            /// key for a profile or sample or project === row[1]
            /// key for a profile layer or profile labdata === row[1] + '@' + row[3]
            /// key for a sample labdata === row[1] + '@' + row[2] + '@' + row[3]
            /// 
            if ( !row[1] ) 
              results['report']['errors'][sheet_name].push(['?',j,1,'-k']);  /// wrong key
            else { // no primary key -> skip row
              if (( !isLayer && !isLabData && !isLabData_sampling && keys[row[1]]) || 
                  ( isLayer || isLabData ) && ( !row[3] || keys[row[1]+'@'+row[3]] )  || 
                  ( isLabData_sampling && ( 
                    !( row[2] >= 0 ) || ( ( row[3] > 0 ) && ( row[2] > row[3] ) ) || 
                    ( ( row[3] > 0 ) && keys[row[1]+'@'+row[2]+'@'+row[3]] ) || 
                    ( !row[3] && keys[row[1]+'@'+row[2]+'@+'] )  
                  ))) 
              {
                  results['report']['errors'][sheet_name].push(['?',j,1,'-k']);  /// wrong key or duplicate key
                  results['report']['total_errors'] += 1; 
                  console.log(' no res' + j );   
              }
              else {
                let key = row[1];
                if ( isLayer || isLabData )
                  key = row[1]+'@'+row[3];
                else if ( isLabData_sampling)
                  if ( row[3] )
                    key = row[1]+'@'+row[2]+'@'+row[3];
                  else key = row[1]+'@'+row[2]+'@+';
                keys[key] = j;
                wrong = 0;
                filled = 0;
                let lmap = sheet_mapping['size'];
                let res = validate_row(taxonomies, row, j, key, sheet_name, sheet_mapping, results);
                if (res) {
                  wrong = res.wrong;
                  filled = res.filled;
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
                else if ( isLabData_sampling )
                  results['report']['tree'][row[1]]['Lab Data Sampling'] = perc + ':' + wrong;
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
        else console.log(j)    
      }
      return validated_row;
}  

export const createObjects = async (data, uploadType, cookie) => {
  if ( uploadType === 'XLS_P')
    return await createObjectsPoints(data)
  else if ( uploadType === 'XLS_PJ' )
    return await createObjectsProjects(data)
  else if ( uploadType === 'XLS_PH' )
    return await createObjectsPhotos(data, cookie)
  else return null; 
} 

export const createObjectsPoints = async (res) => {
//// XLS profile sheets
  const data = res.data;
  const sheets = UploadService.TYPES['XLS_P'].sheets;
  let fixtures = {}
  // General  
  let model = null;
  let field = null;
  let level = null;
  let value = null; 
  let taxonomy = null;
  let sheet_mapping = Mapping[ 'XLS_P:'+sheets[0]];
  let sheet = data[sheets[0]];
  
  if ( sheet )
    for ( let i = 0; i < sheet.length; i+=1 ) {
      let row = sheet[i];
      if ( row ) {
        let id =  row[1];
        let _id = row[1];
        for ( let j = 1; j < sheet_mapping.size + 1; j+=1 ) 
          if ( sheet_mapping[j] && typeof row[j] !== "undefined" && row[j].toString().trim() != '' ){ 
            try { 
              model = sheet_mapping[j].m;
              field = sheet_mapping[j].f;
              level = sheet_mapping[j].lf;
              value = sheet_mapping[j].lv;
              taxonomy = sheet_mapping[j].t;
              if ( !fixtures[model] )
                fixtures[model] = { };
              _id = id;
              if ( !fixtures[model][_id] ){  
                fixtures[model][_id] = {};
                fixtures[model][_id]['id'] = _id;
              }
              fixtures[model][_id][field] = row[j];
              if ( model !== 'PointGeneral' ) { 
                let m = model.toLowerCase().trim()
                fixtures['PointGeneral'][id][m] = id; 
              }
            } catch (e) {
              console.log(e);
            }  
          }
      } 
    }
  else console.log ('No sheet 1')
    
  // Layer  LayerRedoximorphicColour  LayerStructure
  sheet_mapping = Mapping['XLS_P:'+sheets[1]];
  sheet = data[sheets[1]];
  
  if ( sheet ) 
    for ( let i = 0; i < sheet.length+1; i+=1 ) {
      let row = sheet[i];
      if ( row ) {
        let l_id = row[1] + '@' + row[3];
        for ( let j = 1; j < sheet_mapping.size+1; j+=1 ) 
          if ( typeof row[j] !== "undefined" && row[j].toString().trim() != '') { 
            try {
              let _id = l_id; 
              model = sheet_mapping[j].m;
              field = sheet_mapping[j].f;
              level = sheet_mapping[j].lf;
              value = sheet_mapping[j].lv;           
              taxonomy = sheet_mapping[j].t;
              if ( !fixtures[model] )
                fixtures[model] = { };
              if ( model === 'LayerStructure' )
                _id = _id + '@' + value;
              if ( !fixtures[model][_id] )  
                fixtures[model][_id] = { id: _id };
              fixtures[model][_id][field] = row[j];
              if ( model !== 'PointLayer' && model !== 'LayerStructure' ) { 
                let m = model.toLowerCase().trim();
                if ( !fixtures['PointLayer'] )
                  fixtures['PointLayer'] = {};
                if ( !fixtures['PointLayer'][l_id] )
                  fixtures['PointLayer'][l_id] = { };
                fixtures['PointLayer'][l_id][m] = _id; 
              }
              if ( model === 'LayerStructure' ) {
                fixtures['LayerStructure'][_id]['layer'] = l_id; 
                if ( level && value)
                  fixtures[model][_id][level] =  value;
                console.log(level+':'+value)
              }
            } catch (e) {
              console.log(e);
            } 
          }
      }
    }
  else console.log ('No sheet 2')
  
  // labdata  
  sheet_mapping = Mapping['XLS_P:'+sheets[2]];
  sheet = data[sheets[2]];
  fixtures['LabData'] = { };
  if ( sheet )
    for ( let i = 0; i < sheet.length; i+=1 ) {
      try {
        let row = sheet[i];
        let id =  row[1] + '@' + row[3];
        if ( fixtures['PointLayer'][id] )
          fixtures['PointLayer'][id]['labdata'] = id;
        else console.log("Warning obj: " + id);
        if ( !fixtures['LabData'][id] ) 
          fixtures['LabData'][id] =  {};
        fixtures['LabData'][id]['id'] = id;
        for ( let j = 1; j < sheet_mapping.size+1; j+=1 ) 
          if ( typeof row[j] !== "undefined" && row[j].toString().trim() != ''){  
            field = sheet_mapping[j].f;
            fixtures['LabData'][id][field] = row[j];
          }
        
      } catch (e) {
        console.log(e);
      }  
    }
  else console.log ('No sheet 3')
  
  
  // labdata mapping 
  sheet_mapping = Mapping['XLS_P:'+sheets[3]];
  sheet = data[sheets[3]];
  fixtures['LabDataSampling'] = { };
  
  if ( sheet )
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let id =  row[1];
      if ( row[3] )
        id += '@' + row[2] + '@' + row[3];
      else id += '@' + row[2] + '@+'; 
      if ( !fixtures['LabData'][id] ) 
        fixtures['LabData'][id] = {};
      fixtures['LabData'][id]['id'] = id;
      for ( let j = 1; j < sheet_mapping.size+1; j+=1 ) 
        if ( typeof row[j] !== "undefined" && row[j].toString().trim() != '' ){  
          field = sheet_mapping[j].f;
          fixtures['LabData'][id][field] = row[j];
        } 
    } catch (e) {
      console.log(e);
    }  
  }
  else console.log ('No sheet 4')
  
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

export const createObjectsProjects = async (res) => {
//// XLS profile sheets
  const data = res.data;
  let fixtures = {}
  let model = null;
  let field = null;
  let sheet_mapping = Mapping['XLS_PJ:Project'];
  let sheet = data['Project'];
  if ( sheet )
    for ( let i = 0; i < sheet.length; i+=1 ) {
      try {
        let row = sheet[i];
        if ( row ) {
          let _id = row[1];
          for ( let j = 1; j < sheet_mapping.size+1; j+=1 ) {
            if (  typeof row[j] !== "undefined" && row[j].toString().trim() != '' ){  
              model = sheet_mapping[j].m;
              field = sheet_mapping[j].f;
              if ( !fixtures[model] )
                fixtures[model] = { };
              if ( !fixtures[model][_id] ){  
                fixtures[model][_id] = {};
                fixtures[model][_id]['id'] = _id;
              }
              
              fixtures[model][_id][field] = row[j];
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
  return result
}

export const createObjectsPhotos = async (res, cookie) => {
//// XLS profile sheets
  const data = res.data;
  res.report = {  total_errors: 0, 'errors': { 'Photos': [] }, 'tree': [] }
  res.validated = 0;
  let fixtures = {}
  let model = null;
  let field = null;
  let sheet_mapping = Mapping['XLS_PH:Photos'];
  let sheet = data['Photos'];
  if ( sheet ) {
    for ( let i = 0; i < sheet.length; i+=1 ) {
      try {
        let row = sheet[i];
        if ( row ) {
          let _id = row[1];
          _id = _id.replace(".", "_");
          let  { data: photos } = await UploadService.getGnDocument(row[1], cookie);
          if ( photos.resources && photos.resources[0] ) {
            let photo = photos.resources[0]
            for ( let j = 1; j < sheet_mapping.size+1; j+=1 ) {
              if (  typeof row[j] !== "undefined" && row[j].toString().trim() != '' ){  
                model = sheet_mapping[j].m;
                field = sheet_mapping[j].f;
                if ( !fixtures[model] )
                  fixtures[model] = { };
                if ( !fixtures[model][_id] ){  
                  fixtures[model][_id] = {};
                  fixtures[model][_id]['id'] = _id;
                }
                fixtures[model][_id][field] = row[j];
              }  
            }
            fixtures[model][_id]["name"] =  row[1];
            fixtures[model][_id]["gn_thumb"] =  photo.thumbnail_url;
            fixtures[model][_id]["gn_link"] =  photo.embed_url;
            fixtures[model][_id]["gn_id"] = photo.pk;
            res.validated += 1;          
          }  
          else {
            res['report']['total_errors'] += 1 
            res['report']['errors']['Photos'].push([_id,i,1,'-photo']) ;
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
