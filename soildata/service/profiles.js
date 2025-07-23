
import Profiles from '../data/profiles';
import Layers from '../data/layers';
import Labdata from '../data/labdata';

export const ProfileService = {
  
  
  GENERAL_SECTIONS : {
    ProfileGeneral : {  section: 1,  label : 'General Description', layer: 'profiles', api: '/api/backoffice/profiles/' },
    LandformTopography: {  section: 2, label : 'Landform and Topography', layer : 'landform-topographies', api : '/api/backoffice/landform-topographies/' },
    ClimateAndWeather: {  section: 3,  label : 'Climate and Weather', layer : 'climate-and-weathers', api : '/api/backoffice/climate-and-weathers/'},
    LandUse : {  section: 4, label : 'Land Use', layer : 'land-uses', api : '/api/backoffice/land-uses/', main : true},
    Cultivated: {  section: 4,  label : 'Land Use - Cultivated', layer : 'cultivated', api : '/api/backoffice/cultivated/'},
    NotCultivated: {  section: 4,  field : 'landuse', multi: true, label : 'Land Use - Not Cultivated', layer : 'not-cultivated', api : '/api/backoffice/not-cultivated/'},
    LitterLayer: {  section: 5,  label : 'Litter Layer', layer : 'litter-layers', api : '/api/backoffice/litter-layers/'},
    Surface: {  section: 5,  label : 'Surface', layer : 'surfaces', api : '/api/backoffice/surfaces/', main : true},
    SurfaceCracks: {  section: 5,  label : 'SurfaceCracks', layer : 'surface-cracks', api : '/api/backoffice/surface-cracks/'},
    CoarseFragments: {  section: 5,  label : 'CoarseFragments', layer : 'coarse-fragments', api : '/api/backoffice/coarse-fragments/'},
    SurfaceUnevenness : {  section: 5,  label : 'Surface Unevenness', layer : 'surface-unevenness', api : '/api/backoffice/surface-unevenness/'},
  },

  LAYER_SECTIONS : {
    ProfileLayer: {  section: 1, field : 'profile', multi: true,  label : 'Layer Description', layer : 'profile-layers', api : '/api/backoffice/profile-layers/'},
    LayerCoarseFragments: {  section: 2, label : 'Coarse fragments', layer : 'layer-coarse-fragments', api : '/api/backoffice/layer-coarse-fragments/'},
    LayerRemants: {  section: 2, label : 'Remnants of broken-up cemented layers', layer : 'layer-remnants', api : '/api/backoffice/layer-remnants/'},
    LayerArtefacts: {  section: 3, label : 'Artefacts', layer : 'layer-artefacts', api : '/api/backoffice/layer-artefacts/'},
    LayerStructure: {  section: 4, field : 'layer', multi: true, label : "Structures", layer : 'layer-structures', api : '/api/backoffice/layer-structures/'},
    LayerNonMatrixPore: {  section: 5, label : "Non-matrix pores", layer : 'layer-non-matrix-pore', api : '/api/backoffice/layer-non-matrix-pore/'},
    LayerCracks: {  section: 5, label : "Cracks", layer : 'layer-cracks', api : '/api/backoffice/layer-cracks/'},
    LayerStressFeatures: {  section: 5, label : "Stress features", layer : 'layer-stress-features', api : '/api/backoffice/layer-stress-features/'},
    LayerMatrixColours: {  section: 6, label : "Matrix Colours", layer : 'layer-matrix-colours', api : '/api/backoffice/layer-matrix-colours/'},
    LayerTextureColour: {  section: 6, label : "Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts", layer:'layer-texture-colours', api : '/api/backoffice/layer-texture-colours/'},
    LayerLithogenicVariegates: {  section: 6, label : 'Lithogenic variegates', layer : 'layer-lithogenic-variegates', api : '/api/backoffice/layer-lithogenic-variegates/'},  
    LayerRedoximorphicFeatures: {  section: 7, main: true, label : 'Redoximorphic features', layer : 'layer-redoximorphic-features', api : '/api/backoffice/layer-redoximorphic-features/'},  
    LayerRedoximorphicColour: {  section: 7, multi: true, label : 'Redoximorphic colours', layer : 'layer-redoximorphic-colours', api : '/api/backoffice/layer-redoximorphic-colours/'},  
    LayerCoatingsBridges: {  section: 8, label : "Coatings and Bridges", layer : 'layer-coatings-bridges', api : '/api/backoffice/layer-coatings-bridges/'},
    LayerRibbonlikeAccumulations: {  section: 8, label : "Ribbonlike Accumulations",layer : 'layer-ribbonlike-accumulations', api : '/api/backoffice/layer-ribbonlike-accumulations/'},
    LayerCarbonates: {  section: 8, label : "Carbonates", layer : 'layer-carbonates', api : '/api/backoffice/layer-carbonates/'},
    LayerGypsum: {  section: 8, label : "Gypsum", layer : 'layer-gypsum', api : '/api/backoffice/layer-gypsum/'},
    LayerSecondarySilica: {  section: 8, label : "Secondary Silica", layer : 'layer-secondary-silica', api : '/api/backoffice/layer-secondary-silica/'},
    LayerConsistence: {  section: 9, label : "Consistence", layer : 'layer-consistences', api : '/api/backoffice/layer-consistences/'},
    LayerSurfaceCrusts: {  section: 9, label : "Surface crusts", layer : 'layer-surface-crusts', api : '/api/backoffice/layer-surface-crusts/'},
    LayerPermafrostFeatures: {  section: 9, label : 'Permafrost features', layer : 'layer-permafrost-features', api : '/api/backoffice/layer-permafrost-features/' },
    LayerOrganicCarbon: {  section: 10, label : "Soil Organic Carbon", layer : 'layer-organic-carbon', api : '/api/backoffice/layer-organic-carbon/' },
    LayerRoots: {  section: 10, label : "Roots", layer : 'layer-roots', api : '/api/backoffice/layer-roots/'},
    LayerAnimalActivity: {  section: 10, label : "Animal Activity", layer : 'layer-animal-activities', api : '/api/backoffice/layer-animal-activities/'},
    LayerHumanAlterations: {  section: 10, label : "Human Alterations", layer : 'layer-human-alterations', api : '/api/backoffice/layer-human-alterations/'},
    LayerDegreeDecomposition: {  section: 10, label : "Degree of decomposition", layer : 'layer-degree-decomposition', api : '/api/backoffice/layer-degree-decomposition/'},
  },

  async get(id) { 
    let data = null;
    try { 
      
    } catch (e) { 
    } 
    return data;
  },

  async get(model, id) { 
    let data = null;
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
  async save(model,formdata) {
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

  async remove(model, id) {
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

  async update(model, formdata) {
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