
import Profiles from '../data/profiles';
import Layers from '../data/layers';
import Labdata from '../data/labdata';

export const ProfileService = {
  
  
  GENERAL_SECTIONS : [
    {  model:'ProfileGeneral', label : 'General', parts: ['8.2.1','8.2.2','Notes'],},
    {  model:'LandformTopography', label : 'Landform&Topography', parts: ['8.2.3'],},
    {  model:'ClimateAndWeather', label : 'Climate&Weather', parts: ['8.2.4'],},
    {  model:'LandUse', label : "Land Use", parts: ['8.2.5',], others:[]},
    {  model:'Cultivated', label : "Land Use - Cultivated", parts: ['8.2.5',],},
    {  model:'NotCultivated', label : "Land Use - Not Cultivated", parts: ['8.2.5',], others:[]},
    {  model:'Surface', label : "Surface", parts: ['8.3.2','8.3.3','8.3.4','8.3.5','8.3.6','8.3.7','8.3.8','8.3.9','8.3.10','8.3.12'],},
    {  model:'SurfaceCracks', label : "SurfaceCracks", parts: ['8.3.2','8.3.3','8.3.4','8.3.5','8.3.6','8.3.7','8.3.8','8.3.9','8.3.10','8.3.12'],},
    {  model:'CoarseFragments', label : "CoarseFragments", parts: ['8.3.2','8.3.3','8.3.4','8.3.5','8.3.6','8.3.7','8.3.8','8.3.9','8.3.10','8.3.12'],},
    {  model:'SurfaceUnevenness', label : "Surface Unevenness", parts: ['8.3.11'],}
  ],

  LAYER_SECTIONS : [
    {  model:'ProfileLayer', label : 'Layer Identification', parts: ['8.4.1','8.4.2','8.4.3','8.4.4','8.4.5','8.4.6','8.4.9','8.4.21','8.4.22','8.4.28','8.4.29','8.4.32','8.4.33','8.4.40','Notes'],},
    {  model:'LayerCoarseFragments', label : 'Layer Coarse Fragments', parts: ['8.4.7'],},
    {  model:'LayerArtefacts', label : 'Layer Artefacts', parts: ['8.4.8'],},
    {  model:'LayerStructure', label : "Layer Land Structure", parts: ['8.4.10','8.4.12','8.4.13','8.4.14',],},
    {  model:'Layer Colours', label : "Layer Colours", parts: ['8.4.17','8.4.18','8.4.19','8.4.20',],},
    {  model:'LayerCoatingsBridges', label : "Layer Coatings and Bridges", parts: ['8.4.23'],},
    {  model:'LayerRibbonlikeAccumulations', label : "Layer Ribbonlike Accumulations", parts: ['8.4.24'],},
    {  model:'LayerCarbonates', label : "Layer Carbonates", parts: ['8.4.25'],},
    {  model:'LayerGypsum', label : "Layer Gypsum", parts: ['8.4.26'],},
    {  model:'LayerSecondarySilica', label : "Layer Secondary Silica", parts: ['8.4.27'],},
    {  model:'LayerConsistence', label : "Layer Consistence", parts: ['8.4.30'],},
    {  model:'LayerSurfaceCrusts', label : "Layer Surface Crust", parts: ['8.4.31'],},
    {  model:'LayerPermafrostFeatures', label : "Layer Permafrost", parts: ['8.4.34'],},
    {  model:'LayerOrganicCarbon', label : "Layer Soil Organic Carbon", parts: ['8.4.36'],},
    {  model:'LayerRoots', label : "Layer Roots", parts: ['8.4.37'],},
    {  model:'LayerAnimalActivity', label : "Layer Animal Activity", parts: ['8.4.38'],},
    {  model:'LayerHumanAlterations', label : "Layer Human Alterations", parts: ['8.4.39'],},
    {  model:'LayerDegreeDecomposition', label : "Layer Degree of decomposition", parts: ['8.4.41'],},
  ],

  async get(id) { 
    data = null;
    try { 
      let res = fetch( `/api/backoffice/profiles/${id}`)
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async list() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/profiles')
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },  

// formData: 
  async save(profile) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/profiles`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profile),
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async remove(id) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/profiles/${id}`, {
        method: "DELETE",
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async update(profile) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/profiles/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profile),
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  }
}

export default ProfileService