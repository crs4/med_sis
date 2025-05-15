import ExcelJS from 'exceljs';
import Taxonomies from '../data/taxonomies';
import Mapping from '../data/mapping';

export const validateXLSFile = async (files, isProfile, sheets) => {
    let perc;
    let workbook = new ExcelJS.Workbook();
    let uploadType = 'XLS_S';
    if ( isProfile )
         uploadType = 'XLS_P';
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
    if (sheets) {
      let s;
      for ( s=0; s<sheets.length; s+=1 ) {
        try {
          if ( workbook.getWorksheet(sheets[s]) ) {
            vresult['data'][sheets[s]] = [];
            const sheet_mapping = Mapping[uploadType+':'+sheets[s]];
            if ( sheet_mapping ) {
              workbook.getWorksheet(sheets[s]).eachRow({ includeEmpty: true }, function(row, rowNumber) {
                if ( rowNumber >= sheet_mapping['startRow'] )  {
                  if ( row.values[1] ){
                    vresult['data'][sheets[s]][rowNumber] = row.values;
                    total_rows+=1;
                  }
                }
              })  
            }
          }
        } catch (e) {
          console.log(e);
        }
      }  
      for ( s=0; s<sheets.length; s+=1 ) { 
        try {    
          const sheet_mapping = Mapping[uploadType+':'+sheets[s]];
          total_valid += validateSheet(s, sheets[s], isProfile, sheet_mapping, vresult);
          perc = (total_valid/total_rows)*100;
          vresult['validated'] = ( Number(perc).toPrecision(2));
          
        } catch (e) {
          console.log(e);
        }
      }
    } 
    return vresult; 
  }

export const validateSheet = (sheet_index,sheet_name, is_profile, sheet_mapping, results) => {
      let code = '';
      let n,i = 1;
      let keys = [];
      const isGeneral = (is_profile && sheet_index === 0); 
      const isLayer =  (sheet_index === 1) 
      const isCls =  (is_profile && sheet_index === 2); 
      const isLabData = ((is_profile && sheet_index === 3) || (!is_profile && sheet_index === 2)); 
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
            /// key for profile\sample === row[1]
            /// key for profile\sample layer and profile labdata === row[1] + row[3]
            /// key for sample labdata === row[1] + row[2] + row[3]
            if ( row[1] ) { // no key skip row
              if (( !isLayer && !isLabData && keys[row[1]]) || ( is_profile && ( isLayer || isLabData ) && ( !row[3] || keys[row[1]+'_'+row[3]] ) ) || 
                  ( !is_profile && isLabData && ( !row[3] || !row[2] || keys[row[1]+'['+row[2]+'..'+row[3]+']'] ) ) ){
                  results['report']['errors'][sheet_name].push(['?',j,1,'-k']);  /// wrong or duplicate key or not valid row
              }
              else {
                let key = row[1];
                if ( ( isLayer || isLabData ) && is_profile )
                  key = row[1]+'_'+row[3];
                else if ( isLabData && !is_sample )
                  key = row[1]+'['+row[2]+'..'+row[3]+']';
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
                        if ( vb !== 't' && vb !== 'f' && vb !== 'si' && vb !== 'no' && vb !== 'true' && vb !== 'false' )   
                          code = '-b'; //'Wrong boolean, allowed values T for True, F for False'                         
                        break;
                      case 'date':
                        if ( ( typeof row[i] === 'string' ||  row[i] instanceof String ) )  
                        {
                          if ( row[i].trim() === 'nd' )
                            row[i] = '';
                          else {
                            n = row[i].split('/');
                            if ( n[0] === '0' || n[0] === '00')
                              n[0] = '01';
                            if ( n.length === 3 && (n[1] === '0' || n[1] === '00'))
                              n[1] = '01';
                            if ( ( n.length === 3 && isNaN(new Date (n[2]+'-'+n[1]+'-'+n[0])) )  ||
                                 ( n.length === 2 && isNaN(new Date (n[1]+'-'+n[0]+'-01')) ) )
                              code = '-d'; // 'not valid date, allowed format is ISO YYYY-MM-DD '                         
                          }    
                        }
                        break;
                      case 'numeric':
                        n = Number(row[i]);
                        if (isNaN(n))
                          code = '-n'; // 'not valid number'                         
                        break;
                      case 'numeric(%)':
                        n = Number(row[i]);
                        if (isNaN(n) || n < 0 || n > 100 )
                          code = '-%'; //'not valid percentage [0..100] '                         
                        break;
                      case 'numeric(0)':
                        n = Number(row[i]);
                        if (isNaN(n) || n < 0 )
                          code = '-0'; //'not valid positive number'                         
                        break;
                      case 'latitude':
                        n = Number(row[i]);
                        if (isNaN(n) || n <= -90 || n >= 90 )
                          code = '-lat'; //'not valid latitude in decimal degree'                         
                        break;
                      case 'longitude':
                        n = Number(row[i]);
                        if (isNaN(n) || n <= -180 || n >= 180 )
                          code = '-lon'; //'not valid longitude in decimal degree'                         
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
                else if ( isLayer && is_profile )
                  results['report']['tree'][row[1]]['Layer_'+row[3]] = perc + ':' + wrong;
                else if ( isLayer && !is_profile )
                  results['report']['tree'][row[1]]['layer'] = perc + ':' + wrong;
                else if ( isLabData && is_profile )
                  results['report']['tree'][row[1]]['Lab_layer_'+row[3]] = perc + ':' + wrong;
                else if ( isLabData && !is_profile )
                  results['report']['tree'][row[1]]['Lab['+row[2]+'..'+row[3]+']'] = perc + ':' + wrong;
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

/*
- ProfileGeneral fields
    landuse =  LandUse fields
    surface = Surface fields
    surf_cracks = SurfaceCracks fields
    land_topo = LandformTopography fields
    clim_weath = ClimateAndWeather fields
    genealogy =  Genealogy fields
    
    layers = ProfileLayer[]

-ProfileLayer fields
    remnants = LayerRemnants fields
    coarsefragments = LayerCoarseFragments  fields
    artefacts = LayerArtefacts  fields
    cracks = LayerCracks  fields
    stressfeatures = LayerStressFeatures fields
    coatingsbridges = LayerCoatingsBridges
    ribbonlikeaccumulations = LayerRibbonlikeAccumulations
    carbonates = LayerCarbonates
    gypsum = LayerGypsum
    secondarysilica = LayerSecondarySilica
    consistence = LayerConsistence
    surfacecrusts = LayerSurfaceCrusts  
    permafrost = LayerPermafrostFeatures  
    organiccarbon = LayerOrganicCarbon  
    roots = LayerRoots   
    animalactivity =  LayerAnimalActivity
    humanalterations = LayerHumanAlterations
    degreedecomposition = LayerDegreeDecomposition   
    nonmatrixpore = LayerNonMatrixPore   
    labdata =  LabData
    matrixcolours = LayerMatrixColours   
    texturecolour = LayerTextureColour 
    lithogenicvariegates = LayerLithogenicVariegates
    redoximorphicfeatures = LayerRedoximorphicFeatures
    structures = LayerStructure[] 
*/

export const createProfiles = (data) => {
//// XLS profile sheets
  const sheets = UploadService.TYPES[upload.type].sheets;
  const uploadType = 'XLS_P';
  const profiles = {} ;
  const layers = {} ;
  const labdata = {} ;
  const structures = {} ;
  
  // General  
  let sheet_mapping = Mapping[uploadType+':'+sheets[0]];
  let sheet = data[sheets[0]];
  let model = null;
  let field = null;
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let id =  row[0];
      profiles[id] = {  
        landuse : null, 
        surface : null,
        surfacecracks : null,
        landformtopography : null,
        climateandweather : null, 
        genealogy : null,
        layers : []
      }
      if ( row ) {
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            if ( model === 'ProfileGeneral' ) 
              profiles[id][field] = row[j];
            else {
              if ( !profiles[id][model.toLowerCase()] )
                profiles[id][model.toLowerCase()] = {};
              profiles[id][model.toLowerCase()][field] = row[j];
            }
          }
        }
        profiles[ profile["code"] ] = profile;
      }
    } catch (e) {
        console.log(e);
    }
  } 
  // Layer  
  sheet_mapping = Mapping[uploadType+':'+sheets[1]];
  sheet = data[sheets[1]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let layer_id =  row[0] + '@' + row[2];
      layers[layer_id] = {
        remnants : null,
        coarsefragments : null,
        artefacts : null,
        cracks : null,
        stressfeatures : null,
        coatingsbridges : null,
        ribbonlikeaccumulations : null,
        carbonates : null,
        gypsum : null,
        secondarysilica : null,
        consistence : null,
        surfacecrusts : null,  
        permafrost : null,  
        organiccarbon : null,  
        roots : null,   
        animalactivity :  null,
        humanalterations : null,
        degreedecomposition : null,   
        nonmatrixpore : null,   
        labdata :  null,
        matrixcolours : null,   
        texturecolour : null, 
        lithogenicvariegates : null,
        redoximorphicfeatures : null,
        structures : []
      }  
      structures[layer_id] = {
      }
      if ( row ) {
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;
            if ( model === 'ProfileLayer' ) 
              layers[layer_id][field] = row[j];
            else if ( model === 'LayerStructure' )  {
              if ( level && value ) {
                let s_id = layer_id + '@' + value;
                if ( !structures [s_id] )
                   structures [s_id] = { level : value };  
                structures[s_id][field] = row[j];
              }
            }
            else  {
              let onetoone = model.toLowerCase().substring(5)
              if ( !layers[layer_id][onetoone] )
                layers[layer_id][onetoone] = {};
              layers[layer_id][onetoone][field] = row[j];
            }
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  } 
  // labdata  
  sheet_mapping = Mapping[uploadType+':'+sheets[2]];
  sheet = data[sheets[2]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let layer_id =  row[0] + '@' + row[2];
      labdata[layer_id] = {
      }  
      if ( row ) {
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            field = sheet_mapping[j].f;
            labdata[layer_id][field] = row[j];
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  } 
  // classification  
  sheet_mapping = Mapping[uploadType+':'+sheets[3]];
  sheet = data[sheets[3]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let id =  row[0];
      labdata[layer_id] = {
      }  
      if ( row ) {
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            field = sheet_mapping[j].f;
            profiles[id][field] = row[j];
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  }  
  let pkeys = Object.keys(profiles);
  let lkeys = Object.keys(layers);
  let labkeys = Object.keys(labdata);
  let stkeys = Object.keys(structures);
  for ( let s = 0; s < stkeys.length; s+=1 ) {
    let split = stkeys[s].split('@')
    layers[split[0]+'@'+split[1]]['structures'].push(structures[stkeys[s]])
  }
  for ( let lb = 0; lb < labkeys.length; lb+=1 ) {
    layers[lb]['labdata'] = labdata[lb];
  }
  for ( let l = 0; l < lkeys.length; l+=1 ) {
    let split = lkeys[s].split('@')
    profiles[split[0]]['layers'].push(layers[lkeys[l]])
  }
  result = [];
  for ( let p = 0; p < pkeys.length; p+=1 ) {
    result.push(profiles[p]);
  }
  console.log ( JSON.stringify(result) );
  ////GeoJSON......30 layer
  
} 