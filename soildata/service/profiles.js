export const ProfileService = {
  MONITORING_GENERAL_SECTIONS : ['General Description','Location','Landform and Topography','Geomorphic features','Climate and Weather',
    'Land Use','Not Cultivated Land','Ground stratum','Upper stratum','Middle stratum','Cultivated Land',
    'Litter Layer','Bedrock','Rock outcrops','Coarse surface fragments','Desert features','Patterned ground','Surface crusts','Surface Cracks',
    'Water','Natural surface unevenness', 'Human Made surface unevenness', 'Surface Unevenness Profile Position','Technical Surface Alteration',
    //'Land preparation','Use of inputs','Irrigation Type','Conservation Measure type','Worm casts','Disturbed soil sample','Indisturbed soil sample',
    'Notes'
  ],

  MONITORING_LAYER_SECTIONS : [  
    'Layer Description','Homogeneity of the layer','Water','Organic, organo-technic or mineral layer','Layer boundaries',
    'Wind deposition','Coarse fragments','Remnants of broken-up cemented layers','Artefacts','Texture class',
    'Structures First Level Type 1','Structures First Level Type 2','Structures First Level Type 3',
    'Structures Second Level Type 1.1','Structures Second Level Type 1.2','Structures Second Level Type 2.1',
    'Structures Second Level Type 2.2','Structures Second Level Type 3.1', 'Structures Second Level Type 3.2',
    'Structures Third Level Type 1.1.1','Structures Third Level Type 1.2.1','Structures Third Level Type 2.1.1',
    'Structures Third Level Type 2.2.1','Structures Third Level Type 3.1.1','Structures Third Level Type 3.2.1',
    'Wedge-shaped aggregates', 'Non-matrix pores','Cracks','Stress features','Matrix Colours',
    'Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts',
    'Lithogenic variegates','Redoximorphic features','---------','Rh value','Initial weathering','Coatings and Bridges',
    'Ribbonlike Accumulations','Carbonates','Gypsum','Secondary Silica','Readily soluble salts','Field Ph','Consistence','Surface crusts',
    'Continuity of hard materials and cemented layers','Volcanic glasses and andic characteristics','Permafrost features', 
    'Bulk density','Soil Organic Carbon','Roots','Results of animal activity','Human Alterations','Parent material','Degree of decomposition','Notes'
  ],

  MONITORING_MODELS : {
    MonitoringGeneral : {  layer: 'monitoring-sites', api: 'monitoring-generals' },
    MonitoringLandformTopography: { layer : 'monitoring-landform-topographies', api: 'monitoring-landform-topographies' },
    MonitoringClimateAndWeather: {  layer : 'monitoring-climate-and-weathers', api: 'monitoring-climate-and-weathers'},
    MonitoringLandUse : {  layer : 'monitoring-land-uses', api: 'monitoring-land-uses'},
    MonitoringCultivated: { layer : 'monitoring-cultivated', api: 'monitoring-cultivated'},
    MonitoringNotCultivated: {  layer : 'monitoring-not-cultivated', api: 'monitoring-not-cultivated'},
    MonitoringLitterLayer: {  layer : 'monitoring-litter-layers', api: 'monitoring-litter-layers'},
    MonitoringSurface: {  layer: 'monitoring-surfaces', api: 'monitoring-surfaces'},
    MonitoringSurfaceCracks: {  layer : 'monitoring-surface-cracks', api: 'monitoring-surface-cracks'},
    MonitoringCoarseFragments: {  layer : 'monitoring-monitoring-coarse-fragments', api: 'monitoring-coarse-fragments'},
    MonitoringSurfaceUnevenness : { layer : 'monitoring-surface-unevenness', api: 'monitoring-surface-unevenness'},
    MonitoringLayer: {  layer : 'monitoring-layers', api: 'monitoring-layers'},
    MonitoringLayerCoarseFragments: {  layer : 'monitoring-layer-coarse-fragments', api: 'monitoring-layer-coarse-fragments'},
    MonitoringLayerRemants: {  layer : 'monitoring-layer-remnants', api: 'monitoring-layer-remnants'},
    MonitoringLayerArtefacts: {  layer : 'monitoring-layer-artefacts', api: 'monitoring-layer-artefacts'},
    MonitoringLayerStructure: {  layer : 'monitoring-layer-structures', api: 'monitoring-layer-structures'},
    MonitoringLayerNonMatrixPore: {  layer : 'monitoring-layer-non-matrix-pore', api: 'monitoring-layer-non-matrix-pores'},
    MonitoringLayerCracks: {  layer : 'monitoring-layer-cracks', api: 'monitoring-layer-cracks'},
    MonitoringLayerStressFeatures: {  layer : 'monitoring-layer-stress-features', api: 'monitoring-layer-stress-features'},
    MonitoringLayerMatrixColours: {  layer : 'monitoring-layer-matrix-colours', api: 'monitoring-layer-matrix-colours'},
    MonitoringLayerTextureColour: {  layer:'monitoring-layer-texture-colours', api: 'monitoring-layer-texture-colours'},
    MonitoringLayerLithogenicVariegates: {  layer : 'monitoring-layer-lithogenic-variegates', api: 'monitoring-layer-lithogenic-variegates'},  
    MonitoringLayerRedoximorphicFeatures: { layer : 'monitoring-layer-redoximorphic-features', api: 'monitoring-layer-redoximorphic-features'},  
    MonitoringLayerRedoximorphicColour: {  layer : 'monitoring-layer-redoximorphic-colours', api: 'monitoring-layer-redoximorphic-colours'},  
    MonitoringLayerCoatingsBridges: { layer : 'monitoring-layer-coatings-bridges', api: 'monitoring-layer-coatings-bridges'},
    MonitoringLayerRibbonlikeAccumulations: {  layer : 'monitoring-layer-ribbonlike-accumulations', api: 'monitoring-layer-ribbonlike-accumulations'},
    MonitoringLayerCarbonates: {  layer : 'monitoring-layer-carbonates', api: 'monitoring-layer-carbonates'},
    MonitoringLayerGypsum: {  layer : 'monitoring-layer-gypsum', api: 'monitoring-layer-gypsum'},
    MonitoringLayerSecondarySilica: { layer : 'monitoring-layer-secondary-silica', api: 'monitoring-layer-secondary-silica'},
    MonitoringLayerConsistence: {  layer : 'monitoring-layer-consistences', api: 'monitoring-layer-consistences'},
    MonitoringLayerSurfaceCrusts: {  layer : 'monitoring-layer-surface-crusts', api: 'monitoring-layer-surface-crusts'},
    MonitoringLayerPermafrostFeatures: {  layer : 'monitoring-layer-permafrost-features', api: 'monitoring-layer-permafrost-features/' },
    MonitoringLayerOrganicCarbon: {  layer : 'monitoring-layer-organic-carbon', api: 'monitoring-layer-organic-carbon/' },
    MonitoringLayerRoots: {  layer : 'monitoring-layer-roots', api: 'monitoring-layer-roots'},
    MonitoringLayerAnimalActivity: {  layer : 'monitoring-layer-animal-activities', api: 'monitoring-layer-animal-activities'},
    MonitoringLayerHumanAlterations: {  layer : 'monitoring-layer-human-alterations', api: 'monitoring-layer-human-alterations'},
    MonitoringLayerDegreeDecomposition: {  layer : 'monitoring-layer-degree-decomposition', api: 'monitoring-layer-degree-decomposition'},
    MonitoringLabData: {  layer : "monitoring-lab-data", api: "monitoring-lab-data"}
    
  },

  LEGACY_GENERAL_SECTIONS : ['General Description','Location','Landform and Topography','Geomorphic features','Climate and Weather',
    'Land Use','Not Cultivated Land','Ground stratum','Upper stratum','Middle stratum','Cultivated Land',
    'Litter Layer','Bedrock','Rock outcrops','Coarse surface fragments','Desert features','Patterned ground','Surface crusts','Surface Cracks',
    'Water','Natural surface unevenness', 'Human Made surface unevenness', 'Surface Unevenness Profile Position','Technical Surface Alteration','Notes'],

  LEGACY_LAYER_SECTIONS : [  
    'Layer Description','Homogeneity of the layer','Water','Organic, organo-technic or mineral layer','Layer boundaries',
    'Wind deposition','Coarse fragments','Remnants of broken-up cemented layers','Artefacts','Texture class',
    'Structures First Level Type 1','Structures First Level Type 2','Structures First Level Type 3',
    'Structures Second Level Type 1.1','Structures Second Level Type 1.2','Structures Second Level Type 2.1',
    'Structures Second Level Type 2.2','Structures Second Level Type 3.1', 'Structures Second Level Type 3.2',
    'Structures Third Level Type 1.1.1','Structures Third Level Type 1.2.1','Structures Third Level Type 2.1.1',
    'Structures Third Level Type 2.2.1','Structures Third Level Type 3.1.1','Structures Third Level Type 3.2.1',
    'Wedge-shaped aggregates', 'Non-matrix pores','Cracks','Stress features','Matrix Colours',
    'Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts',
    'Lithogenic variegates','Redoximorphic features','---------','Rh value','Initial weathering','Coatings and Bridges',
    'Ribbonlike Accumulations','Carbonates','Gypsum','Secondary Silica','Readily soluble salts','Field Ph','Consistence','Surface crusts',
    'Continuity of hard materials and cemented layers','Volcanic glasses and andic characteristics','Permafrost features', 
    'Bulk density','Soil Organic Carbon','Roots','Results of animal activity','Human Alterations','Parent material','Degree of decomposition','Notes'
  ],
  
  LEGACY_MODELS : {
    ProfileGeneral : {  layer: 'profiles', api: 'profile-generals' },
    LandformTopography: { layer : 'landform-topographies', api: 'landform-topographies' },
    ClimateAndWeather: {  layer : 'climate-and-weathers', api: 'climate-and-weathers'},
    LandUse : {  layer : 'land-uses', api: 'land-uses'},
    Cultivated: { layer : 'cultivated', api: 'cultivated'},
    NotCultivated: {  layer : 'not-cultivated', api: 'not-cultivated'},
    LitterLayer: {  layer : 'litter-layers', api: 'litter-layers'},
    Surface: {  layer: 'surfaces', api: 'surfaces'},
    SurfaceCracks: {  layer : 'surface-cracks', api: 'surface-cracks'},
    CoarseFragments: {  layer : 'coarse-fragments', api: 'coarse-fragments'},
    SurfaceUnevenness : { layer : 'surface-unevenness', api: 'surface-unevenness'},
    ProfileLayer: {  layer : 'profile-layers', api: 'profile-layers'},
    LayerCoarseFragments: {  layer : 'layer-coarse-fragments', api: 'layer-coarse-fragments'},
    LayerRemants: {  layer : 'layer-remnants', api: 'layer-remnants'},
    LayerArtefacts: {  layer : 'layer-artefacts', api: 'layer-artefacts'},
    LayerStructure: {  layer : 'layer-structures', api: 'layer-structures'},
    LayerNonMatrixPore: {  layer : 'layer-non-matrix-pore', api: 'layer-non-matrix-pores'},
    LayerCracks: {  layer : 'layer-cracks', api: 'layer-cracks'},
    LayerStressFeatures: {  layer : 'layer-stress-features', api: 'layer-stress-features'},
    LayerMatrixColours: {  layer : 'layer-matrix-colours', api: 'layer-matrix-colours'},
    LayerTextureColour: {  layer:'layer-texture-colours', api: 'layer-texture-colours'},
    LayerLithogenicVariegates: {  layer : 'layer-lithogenic-variegates', api: 'layer-lithogenic-variegates'},  
    LayerRedoximorphicFeatures: { layer : 'layer-redoximorphic-features', api: 'layer-redoximorphic-features'},  
    LayerRedoximorphicColour: {  layer : 'layer-redoximorphic-colours', api: 'layer-redoximorphic-colours'},  
    LayerCoatingsBridges: { layer : 'layer-coatings-bridges', api: 'layer-coatings-bridges'},
    LayerRibbonlikeAccumulations: {  layer : 'layer-ribbonlike-accumulations', api: 'layer-ribbonlike-accumulations'},
    LayerCarbonates: {  layer : 'layer-carbonates', api: 'layer-carbonates'},
    LayerGypsum: {  layer : 'layer-gypsum', api: 'layer-gypsum'},
    LayerSecondarySilica: { layer : 'layer-secondary-silica', api: 'layer-secondary-silica'},
    LayerConsistence: {  layer : 'layer-consistences', api: 'layer-consistences'},
    LayerSurfaceCrusts: {  layer : 'layer-surface-crusts', api: 'layer-surface-crusts'},
    LayerPermafrostFeatures: {  layer : 'layer-permafrost-features', api: 'layer-permafrost-features/' },
    LayerOrganicCarbon: {  layer : 'layer-organic-carbon', api: 'layer-organic-carbon/' },
    LayerRoots: {  layer : 'layer-roots', api: 'layer-roots'},
    LayerAnimalActivity: {  layer : 'layer-animal-activities', api: 'layer-animal-activities'},
    LayerHumanAlterations: {  layer : 'layer-human-alterations', api: 'layer-human-alterations'},
    LayerDegreeDecomposition: {  layer : 'layer-degree-decomposition', api: 'layer-degree-decomposition'},
    LabData: {  layer : "lab-data", api: "lab-data"}
    
  },

  async get(model, id) { 
    let data = null;
    try { 
      let model_api = this.MODELS[model].api 
      let res = fetch( `/api/backoffice/${model_api}/${id}`)
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) { 
      console.log(e)
    } 
    return data;
  },

  async listLegacyProfiles() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/profile-generals')
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) { 
      console.log(e)
    } 
    return data;
  },  

  async listMonitoringSites() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/monitoring-generals')
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) { 
      console.log(e)
    } 
    return data;
  },  

  async listLabData() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/lab-data')
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) {
       console.log(e)
    }   
    return data;
  },  

// formData: 
  async create(model,formdata) {
    let data = null;
    try { 
      let model_api = this.MODELS[model].api 
      let res = fetch( `/api/backoffice/${model_api}/${id}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formdata),
      });
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async remove(model, id) {
    let data = null;
    try { 
      let model_api = this.MODELS[model].api 
      let res = fetch( `/api/backoffice/${model_api}/${id}`, {
        method: "DELETE",
      });
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async update(model, formdata) {
    let data = null;
    try { 
      let model_api = this.MODELS[model].api 
      let res = fetch( `/api/backoffice/${model_api}/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formdata),
      });
      if ( res && res.ok ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  }
}
export default ProfileService