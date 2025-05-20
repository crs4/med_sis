import ExcelJS from 'exceljs';
import Taxonomies from '../data/taxonomies';
import Mapping from '../data/mapping';
import { point, featureCollection } from '@turf/turf';


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

export const createObjects = (data) => {
//// XLS profile sheets
  const sheets = UploadService.TYPES[upload.type].sheets;
  const uploadType = 'XLS_P';
  let fixtures = {}
  // General  
  let sheet_mapping = Mapping[uploadType+':'+sheets[0]];
  let sheet = data[sheets[0]];
  let model = null;
  let field = null;
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let id =  row[0];
      if ( row ) 
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;
            
            if ( !fixtures[model] )
              fixtures[model] = [];
            if ( model === 'NotCultivated' )
              _id = id + '@' + value;
            else _id = id;
            if ( !fixtures[model][_id] ){  
              fixtures[model][_id] = {};
              fixtures[model][_id]['id'] = _id;
            }
            fixtures[model][_id][field] = row[j];
            if ( model !== 'ProfileGeneral' && model !== 'NotCultivated' ) { 
              let m = model.toLowerCase().trim()
              fixtures['ProfileGeneral'][id][m] = id; 
            }
            if ( model === 'NotCultivated' ) {
              fixtures['NotCultivated'][_id]['land_use'] = id; 
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
      let id =  row[0] + '@' + row[2];
      if ( row ) 
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            model = sheet_mapping[j].m;
            field = sheet_mapping[j].f;
            level = sheet_mapping[j].lf;
            value = sheet_mapping[j].lv;

            if ( !fixtures[model] )
              fixtures[model] = [];
            if ( model === 'LayerRedoximorphicColour' || model === 'LayerStructure' )
              _id = id + '@' + value;
            else _id = id;
            if ( !fixtures[model][_id] ){  
              fixtures[model][_id] = {};
              fixtures[model][_id]['id'] = _id;
            }
            fixtures[model][_id][field] = row[j];
            if ( model !== 'ProfileLayer' && model !== 'LayerRedoximorphicColour' && model !== 'LayerStructure' ) { 
              let m = model.toLowerCase().trim()
              fixtures['ProfileLayer'][id][m] = id; 
            }
            if ( model === 'LayerRedoximorphicColour' ) {
              fixtures['LayerRedoximorphicColour'][_id]['features'] = id; 
            }
            if ( model === 'LayerStructure' ) {
              fixtures['LayerStructure'][_id]['layer'] = id; 
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
      let id =  row[0] + '@' + row[2];
      if ( fixtures['ProileLayer'][id] )
        fixtures['ProileLayer'][id]['labdata'] = id;
      if ( row ) {
        for ( let j = 4; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
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
  sheet_mapping = Mapping[uploadType+':'+sheets[3]];
  sheet = data[sheets[3]];
  for ( let i = 0; i < sheet.length; i+=1 ) {
    try {
      let row = sheet[i];
      let id =  row[0];
      if ( row ) {
        for ( let j = 1; j < sheet_mapping.size; j+=1 ) {
          if ( row[j] && row[j].toString().trim() != '' ){  
            field = sheet_mapping[j].f;
            fixtures['ProfileGeneral'][id][field] = row[j];
          }
        }
      }
    } catch (e) {
        console.log(e);
    } 
  }
  /*
  let keys = Object.keys(fixtures);
  let layer = fixtures['ProfileGeneral'];
  let pointsdata = [];
  for ( let k = 0; k < layer.length; k+=1 ){
    if ( layer[k] ){
      pointsdata[layer[k]['code']] = [pointsdata[layer[k]['lon_wgs84']],pointsdata[layer[k]['lat_wgs84']]]
    }
  }
  layer = fixtures['ProfileLayer'];
  for ( let k = 0; k < layer.length; k+=1 ){
    if ( layer[k] && layer[k]['profile'] ){
      pointsdata[layer[k]['id']] = pointsdata[layer[k]['profile']]
    }
  }

  for ( let k; k < keys.length; k+=1 ){
    console.log ( keys[k] );
    let points = [];
    if (  fixtures[keys[k]] ) {
      for ( let c; c < fixtures[keys[k]].length; c+=1 ){
        let point = null;
        let key = null;
        if ( keys[k][c] )
          if ( k != 'ProfileGeneral' ){
            point = pointsdata[layer[k][c]['id']];
            key = layer[k][c]['id']; 
          }
          else {
            point = pointsdata[layer[k][c]['code']];
            key = layer[k][c]['code']; 
          }
        points.push( point, 
                      keys[k][c],
                      { id: key } );
        console.log ( JSON.stringify(fixtures[keys[k]]) );
  }  
  */
  
  console.log ( JSON.stringify(fixtures) );
} 
  ////GeoJSON......30 layer
 