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

  MONITORING_RELATIONS : {
    MonitoringGeneral : [
      { model : 'MonitoringLandformTopography', field : 'landformtopography',  api: 'monitoring-landform-topographies' },
      { model : 'MonitoringClimateAndWeather', field : 'climateandweather',  api: 'monitoring-climate-and-weathers'},
      { model : 'MonitoringLandUse', field : 'landuse',  api: 'monitoring-land-uses', relations: true},
      { model : 'MonitoringLitterLayer', field : 'litterlayer', api: 'monitoring-litter-layers'},
      { model : 'MonitoringSurface', field: 'surface', api: 'monitoring-surfaces'},
      { model : 'MonitoringSurfaceCracks', field : 'surfacecracks', api: 'monitoring-surface-cracks'},
      { model : 'MonitoringCoarseFragments', field : 'coarsefragments', api: 'monitoring-coarse-fragments'},
      { model : 'MonitoringSurfaceUnevenness', field : 'surfaceunevenness', api: 'monitoring-surface-unevenness'},
    ],
   
    LandUse : [
      { model: 'MonitoringCultivated', field : 'cultivated',  api: 'monitoring-cultivated'},
      { model: 'MonitoringNotCultivated', list : 'landuse',  field : 'not_cultivated',  api: 'monitoring-not-cultivated'}, 
    ],

    MonitoringLayer : {
      MonitoringLayerCoarseFragments: {  field : 'coarsefragments',  api: 'monitoring-layer-coarse-fragments'},
      MonitoringLayerRemants: {  field : 'remnants', api: 'monitoring-layer-remnants'},
      MonitoringLayerArtefacts: {  field : 'artefacts',  api: 'monitoring-layer-artefacts'},
      MonitoringLayerStructure: {  field : 'layer', reverse: true, api: 'monitoring-layer-structures'},
      MonitoringLayerNonMatrixPore: {  field : 'nonmatrixpore',  api: 'monitoring-layer-non-matrix-pores'},
      MonitoringLayerCracks: {  field : 'cracks', api: 'monitoring-layer-cracks'},
      MonitoringLayerStressFeatures: {  field : 'stressfeatures',  api: 'monitoring-layer-stress-features'},
      MonitoringLayerMatrixColours: {  field : 'matrixcolours',  api: 'monitoring-layer-matrix-colours'},
      MonitoringLayerTextureColour: {  field : 'texturecolour',  api: 'monitoring-layer-texture-colours'},
      MonitoringLayerLithogenicVariegates: {  field : 'lithogenicvariegates',  api: 'monitoring-layer-lithogenic-variegates'},  
      MonitoringLayerRedoximorphicFeatures: { relations: true, field: 'redoximorphicfeatures',  api: 'monitoring-layer-redoximorphic-features'},  
      MonitoringLayerCoatingsBridges: { field : 'coatingsbridges',  api: 'monitoring-layer-coatings-bridges'},
      MonitoringLayerRibbonlikeAccumulations: {  field : 'ribbonlikeaccumulations',  api: 'monitoring-layer-ribbonlike-accumulations'},
      MonitoringLayerCarbonates: {  field : 'carbonates', api: 'monitoring-layer-carbonates'},
      MonitoringLayerGypsum: {  field : 'gypsum',  api: 'monitoring-layer-gypsum'},
      MonitoringLayerSecondarySilica: { field : 'secondarysilica',  api: 'monitoring-layer-secondary-silica'},
      MonitoringLayerConsistence: {  field : 'consistence',  api: 'monitoring-layer-consistences'},
      MonitoringLayerSurfaceCrusts: {  field : 'surfacecrusts',  api: 'monitoring-layer-surface-crusts'},
      MonitoringLayerPermafrostFeatures: {  field : 'permafrost',  api: 'monitoring-layer-permafrost-features/' },
      MonitoringLayerOrganicCarbon: {  field : 'organiccarbon', api: 'monitoring-layer-organic-carbon/' },
      MonitoringLayerRoots: { field : 'roots', api: 'monitoring-layer-roots'},
      MonitoringLayerAnimalActivity: {  field : 'animalactivity',  api: 'monitoring-layer-animal-activities'},
      MonitoringLayerHumanAlterations: {  field : 'humanalterations',  api: 'monitoring-layer-human-alterations'},
      MonitoringLayerDegreeDecomposition: {  field : 'degreedecomposition',  api: 'monitoring-layer-degree-decomposition'},
    },

    MonitoringLayerRedoximorphicFeatures : {
      MonitoringLayerRedoximorphicColour: { list : 'features', field: 'redoximorphiccolours', api: 'monitoring-layer-redoximorphic-colours'},  
    }
  },

  LEGACY_GENERAL_TREE_NODES : {
    "data": [  
      { "key": "0", 
            "data": {  "name":"Identifier", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "1", 
        "data": {  "name":"Location", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "2", 
        "data": {  "name":"Landform and Topography", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "2", 
        "data": {  "name":"Geomorphic features", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "3", 
        "data": {  "name":"Climate and Weather", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "4", 
        "data": {  "name":"Land Use", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "5", 
        "data": {  "name":"Land Use", "value": '', "type":"Folder"  },
        "children": [
          { "key": "5-0", 
            "data": {  "name":"Land Use", "value": '', "type":"Field"  },
            "children": []
          },
          { "key": "5-1", 
            "data": {  "name":"Corine Land Cover Class", "value": '', "type":"Field"  },
            "children": []
          },
          { "key": "5-2", 
            "data": {  "name":"Vegetation and land use", "value": '', "type":"Folder"  },
            "children": [
              { "key": "5-2-0", 
                "data": {  "name":"Non-cultivated land: Ground stratum", "value": '', "type":"Folder"  },
                "children": []
              },
              { "key": "5-2-1", 
                "data": {  "name":"Non-cultivated land: Upper stratum", "value": '', "type":"Folder"  },
                "children": []
              },
              { "key": "5-2-2", 
                "data": {  "name":"Non-cultivated land: Mid-stratum", "value": '', "type":"Folder"  },
                "children": []
              },
              { "key": "5-2-3", 
                "data": {  "name":"Cultivated land", "value": '', "type":"Folder"  },
                "children": []
              },
            ]
          },
        ]
      }, 
      { "key": "6", 
        "data": {  "name":"Litter Layer", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "7", 
        "data": {  "name":"Bedrock", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "8", 
        "data": {  "name":"Rock outcrops", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "9", 
        "data": {  "name":"Coarse surface fragments", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "10", 
        "data": {  "name":"Desert features", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "11", 
        "data": {  "name":"Patterned ground form class", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "12", 
        "data": {  "name":"Surface crusts area covered [%]", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "13", 
        "data": {  "name":"Surface cracks", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "14", 
        "data": {  "name":"Water", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "15", 
        "data": {  "name":"Surface unevenness", "value": '', "type":"Folder"  },
        "children": [
          { "key": "15-0", 
            "data": {  "name":"Natural surface unevenness", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "15-1", 
            "data": {  "name":"Human-made surface unevenness", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "15-2", 
            "data": {  "name":"Surface unevenness caused by erosion", "value": '', "type":"Folder"  },
            "children": []
          }
        ]
      },
      { "key": "16", 
        "data": {  "name":"Position of the soil profile", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "17", 
        "data": {  "name":"Technical surface alterations", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "18", 
        "data": {  "name":"Horizons sequence", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "19", 
        "data": {  "name":"Old classification", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "20", 
        "data": {  "name":"Old classification system", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "21", 
        "data": {  "name":"New classification", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "22", 
        "data": {  "name":"Notes", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23", 
        "data": {  "name":"Layers", "value": '', "type":"Folder"  },
        "children": []
      }
    ]
  },

  LEGACY_LAYER_TREE_NODES : {
    "data": [  
      { "key": "23-x-0", 
            "data": {  "name":"Identifier", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-1", 
        "data": {  "name":"Homogeneity of the layer", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-2", 
        "data": {  "name":"Water", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-3", 
        "data": {  "name":"Organic, organo-technic or mineral layer", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23-x-4", 
        "data": {  "name":"Layer boundaries", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-5", 
        "data": {  "name":"Wind deposition", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23-x-6", 
        "data": {  "name":"Coarse fragments", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-7", 
        "data": {  "name":"Remnants of broken-up cemented layers", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-8", 
        "data": {  "name":"Artefacts", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-9", 
        "data": {  "name":"Texture", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-10", 
        "data": {  "name":"Structures", "value": '', "type":"Folder"  },
        "children": [
          { "key": "10-0", 
            "data": {  "name":"First-level structure", "value": '', "type":"Field"  },
            "children": [
              { "key": "10-0-0", 
                "data": {  "name":"Type1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-0-1", 
                "data": {  "name":"Type2", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-0-2", 
                "data": {  "name":"Type3", "value": '', "type":"Field"  },
                "children": []
              },
            ]
          },
          { "key": "10-1", 
            "data": {  "name":"Second-level structure", "value": '', "type":"Field"  },
            "children": [
              { "key": "10-1-0", 
                "data": {  "name":"Type 1.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-1-1", 
                "data": {  "name":"Type 1.2", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-1-2", 
                "data": {  "name":"Type 2.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-1-3", 
                "data": {  "name":"Type 2.2", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-1-4", 
                "data": {  "name":"Type 3.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-1-5", 
                "data": {  "name":"Type 3.2", "value": '', "type":"Field"  },
                "children": []
              }
            ]
          },
          { "key": "10-2", 
            "data": {  "name":"Third-level structure", "value": '', "type":"Field"  },
            "children": [
              { "key": "10-2-0", 
                "data": {  "name":"Type 1.1.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-2-1", 
                "data": {  "name":"Type 1.2.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-2-2", 
                "data": {  "name":"Type 2.1.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-2-3", 
                "data": {  "name":"Type 2.2.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-2-4", 
                "data": {  "name":"Type 3.1.1", "value": '', "type":"Field"  },
                "children": []
              },
              { "key": "10-2-5", 
                "data": {  "name":"Type 3.2.1", "value": '', "type":"Field"  },
                "children": []
              }
            ]
          },
          { "key": "10-4", 
            "data": {  "name":"Wedge-shaped aggregates", "value": '', "type":"Field"  },
            "children": []
          }
        ]  
      }, 
      { "key": "23-x-11", 
        "data": {  "name":"Non-matrix pores", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-12", 
        "data": {  "name":"Cracks", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-13", 
        "data": {  "name":"Stress features", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-14", 
        "data": {  "name":"Matrix colours", "value": '', "type":"Folder"  },
        "children": [
          { "key": "14-0", 
            "data": {  "name":"Colour 1 (dominant)", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "14-1", 
            "data": {  "name":"Colour 2", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "14-2", 
            "data": {  "name":"Colour 3", "value": '', "type":"Folder"  },
            "children": []
          }
        ]
      },
      { "key": "23-x-15", 
        "data": {  "name":"Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-16", 
        "data": {  "name":"Lithogenic variegates", "value": '', "type":"Folder"  },
        "children": [
          { "key": "16-0", 
            "data": {  "name":"Colour 1 (dominant)", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "16-1", 
            "data": {  "name":"Colour 2", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "16-2", 
            "data": {  "name":"Colour 3", "value": '', "type":"Folder"  },
            "children": []
          }
        ]
      },
      { "key": "23-x-17", 
        "data": {  "name":"Redoximorphic features", "value": '', "type":"Folder"  },
        "children": [
          { "key": "17-0", 
            "data": {  "name":"Colour 1 (dominant)", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "17-1", 
            "data": {  "name":"Colour 2", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "17-2", 
            "data": {  "name":"Colour 3", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "17-3", 
            "data": {  "name":"Total abundance, by exposed area [%]", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "17-4", 
            "data": {  "name":"Abundance of cemented oximorphic features, by volume [%]", "value": '', "type":"Field"  },
            "children": []
          },
        ]
      },
      { "key": "23-x-18", 
        "data": {  "name":"rH value", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23-x-19", 
        "data": {  "name":"Initial weathering", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23-x-20", 
        "data": {  "name":"Coatings and bridges", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-21", 
        "data": {  "name":"Ribbon-like accumulations", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-22", 
        "data": {  "name":"Carbonates", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-23", 
        "data": {  "name":"Gypsum", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-24", 
        "data": {  "name":"Secondary silica", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-25", 
        "data": {  "name":"Readily soluble salts", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23-x-26", 
        "data": {  "name":"Field pH", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-27", 
        "data": {  "name":"Consistence", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-28", 
        "data": {  "name":"Surface crusts", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-29", 
        "data": {  "name":"Continuity of hard materials and cemented layers", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-30", 
        "data": {  "name":"Volcanic glasses and andic characteristics", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-31", 
        "data": {  "name":"Permafrost features", "value": '', "type":"Folder"  },
        "children": [
          { "key": "31-0", 
            "data": {  "name":"Cryogenic alteration", "value": '', "type":"Folder"  },
            "children": []
          },
          { "key": "31-1", 
            "data": {  "name":"Layers with permafrost", "value": '', "type":"Field"  },
            "children": []
          }
        ]
      },
      { "key": "23-x-32", 
        "data": {  "name":"Bulk density", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-33", 
        "data": {  "name":"Soil organic carbon", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-34", 
        "data": {  "name":"Roots", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-35", 
        "data": {  "name":"Results of animal activity", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-36", 
        "data": {  "name":"Human alterations", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-37", 
        "data": {  "name":"Parent material", "value": '', "type":"Field"  },
        "children": []
      },
      { "key": "23-x-38", 
        "data": {  "name":"Degree of decomposition in organic layers and presence of dead natural plant residues ", "value": '', "type":"Folder"  },
        "children": []
      },
      { "key": "23-x-39", 
        "data": {  "name":"Notes", "value": '', "type":"Field"  },
        "children": []
      },
    ]
  },
  
  LEGACY_LABDATA_TREE_NODES : {
    "data": [  
      { "key": "23-x-40-0", 
            "data": {  "name":"Identifier", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-1", 
            "data": {  "name":"Gravel content (%)", "value": '', "type":"Field"  },
            "children": []
      },
      { "key": "23-x-40-2", 
            "data": {  "name":"Classification system used for texture of fine earth", "value": '', "type":"Field"  },
            "children": []
      },
      { "key": "23-x-40-3", 
            "data": {  "name":"Sand (% of the fine earth)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-4", 
            "data": {  "name":"Silt (% of the fine earth)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-5", 
            "data": {  "name":"Clay  (% of the fine earth)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-6", 
            "data": {  "name":"Texture Class", "value": '', "type":"Field"  },
            "children": []
      },
      { "key": "23-x-40-7", 
            "data": {  "name":"Bulk density (g/cm3)", "value": '', "type":"Field"  },
            "children": []
      },
      { "key": "23-x-40-8", 
            "data": {  "name":"Electric conductivity (dS/m)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-9", 
            "data": {  "name":"Hydraulic conductivity at saturation (mm/h)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-10", 
            "data": {  "name":"Saturation (%)", "value": '', "type":"Field"  },
            "children": []
      },
      { "key": "23-x-40-11", 
            "data": {  "name":"Wilting point and Field capacity", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-12", 
            "data": {  "name":"Soil acidity: Exchangeable Al (meq/100g)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-13", 
            "data": {  "name":"pH (H2O)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-14", 
            "data": {  "name":"pH (KCl)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-15", 
            "data": {  "name":"pH (CaCl2)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-16", 
            "data": {  "name":"Organic Carbon content (g/kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-17", 
            "data": {  "name":"Organic matter content (%)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-18", 
            "data": {  "name":"CaCO3 content (%)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-19", 
            "data": {  "name":"Gypsum content (%)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-20", 
            "data": {  "name":"CEC (cmol/Kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-21", 
            "data": {  "name":"Ca++ (cmol/Kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-22", 
            "data": {  "name":"Mg++ (cmol/Kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-23", 
            "data": {  "name":"Na+ (cmol/Kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-24", 
            "data": {  "name":"K+ (cmol/Kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-25", 
            "data": {  "name":"N tot content (g/Kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-26", 
            "data": {  "name":"Available P content (mg/kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-27", 
            "data": {  "name":"Fe (g/kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-28", 
            "data": {  "name":"Mn (mg/kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-29", 
            "data": {  "name":"Zn (mg/kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-30", 
            "data": {  "name":"Cu (mg/kg)", "value": '', "type":"Folder"  },
            "children": []
      },
      { "key": "23-x-40-31", 
            "data": {  "name":"Active CaCO3 (%)", "value": '', "type":"Folder"  },
            "children": []
      },
      
    ]
  },

  LEGACY_RELATIONS : {
    ProfileGeneral : [
      { model : 'LandformTopography', field : 'landformtopography',  api: 'landform-topographies' },
      { model : 'ClimateAndWeather', field : 'climateandweather',  api: 'climate-and-weathers'},
      { model : 'LandUse', field : 'landuse',  api: 'land-uses', relations: true},
      { model : 'LitterLayer', field : 'litterlayer', api: 'litter-layers'},
      { model : 'Surface', field: 'surface', api: 'surfaces'},
      { model : 'SurfaceCracks', field : 'surfacecracks', api: 'surface-cracks'},
      { model : 'CoarseFragments', field : 'coarsefragments', api: 'coarse-fragments'},
      { model : 'SurfaceUnevenness', field : 'surfaceunevenness', api: 'surface-unevenness'},
    //{ model : ' ProfileLayer: {  relations: true, field: 'profile', reverse: true, api: 'profile-layers'},
     ],
   
    LandUse : [
      { model: 'MonitoringCultivated', field : 'cultivated',  api: 'monitoring-cultivated'},
      { model: 'MonitoringNotCultivated', list : 'landuse',  field : 'not_cultivated',  api: 'monitoring-not-cultivated'}, 
    ],

    ProfileLayer_relations : {
      LayerCoarseFragments: {  field : 'coarsefragments',  api: 'layer-coarse-fragments'},
      LayerRemants: {  field : 'remnants', api: 'layer-remnants'},
      LayerArtefacts: {  field : 'artefacts',  api: 'layer-artefacts'},
      LayerStructure: {  field : 'layer', reverse: true, api: 'layer-structures'},
      LayerNonMatrixPore: {  field : 'nonmatrixpore',  api: 'layer-non-matrix-pores'},
      LayerCracks: {  field : 'cracks', api: 'layer-cracks'},
      LayerStressFeatures: {  field : 'stressfeatures',  api: 'layer-stress-features'},
      LayerMatrixColours: {  field : 'matrixcolours',  api: 'layer-matrix-colours'},
      LayerTextureColour: {  field : 'texturecolour',  api: 'layer-texture-colours'},
      LayerLithogenicVariegates: {  field : 'lithogenicvariegates',  api: 'layer-lithogenic-variegates'},  
      LayerRedoximorphicFeatures: { relations: true, field: 'redoximorphicfeatures',  api: 'layer-redoximorphic-features'},  
      LayerCoatingsBridges: { field : 'coatingsbridges',  api: 'layer-coatings-bridges'},
      LayerRibbonlikeAccumulations: {  field : 'ribbonlikeaccumulations',  api: 'layer-ribbonlike-accumulations'},
      LayerCarbonates: {  field : 'carbonates', api: 'layer-carbonates'},
      LayerGypsum: {  field : 'gypsum',  api: 'layer-gypsum'},
      LayerSecondarySilica: { field : 'secondarysilica',  api: 'layer-secondary-silica'},
      LayerConsistence: {  field : 'consistence',  api: 'layer-consistences'},
      LayerSurfaceCrusts: {  field : 'surfacecrusts',  api: 'layer-surface-crusts'},
      LayerPermafrostFeatures: {  field : 'permafrost',  api: 'layer-permafrost-features/' },
      LayerOrganicCarbon: {  field : 'organiccarbon', api: 'layer-organic-carbon/' },
      LayerRoots: { field : 'roots', api: 'layer-roots'},
      LayerAnimalActivity: {  field : 'animalactivity',  api: 'layer-animal-activities'},
      LayerHumanAlterations: {  field : 'humanalterations',  api: 'layer-human-alterations'},
      LayerDegreeDecomposition: {  field : 'degreedecomposition',  api: 'layer-degree-decomposition'},
      LabData: {  field : 'labdata', layer : 'legacy-layer-lab-data', api: 'lab-data'}
    },

    LayerRedoximorphicFeatures_relations : {
      LayerRedoximorphicColour: { list : 'features', field: 'redoximorphiccolours', layer : 'legacy-layer-redoximorphic-colours', api: 'layer-redoximorphic-colours'},  
    }
  },

  async resolveRelations( ck, model, source, relations) {
    let result = {}
    let data = null
    if ( relations[model] )
      for ( let i = 0; i < relations[model].length; i +=1 ) 
      { 
        let rel = relations[model];
        if ( source[rel.field] ) {
          let filter = '';
          //relation 1:M
          if ( rel.reverse ){
            filter = '?' + rel.field + "=" + source[rel.field]
            data = await this.get( ck, rel.model_api, null, filter )
          }
          else data = await this.get( ck, rel.model_api, source[rel.field], null )
          if ( data !== nul ) {
            result[rel.model] = data
            //relation level 2
            if ( rel.relations )
              for ( let j = 0; j < LEGACY_MODELS[rel.model].length; j +=1 ) 
              {
                let data2 = null 
                let rel2 = LEGACY_MODELS[rel.model];
                if ( data[rel2.field] ) {
                  data2 = await this.get( ck, rel.model_api, data[rel2.field], null )
                  if ( data2 !== nul ) 
                    result[rel2.model] = data
                }
              }  
          }
        }
      }
  },

  async getModelData( ck, model_api, id, filter) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken ){ 
      try { 
        if ( !model_api || ( !id && !filter) )
          return null
        let _filter = '';
        let _id = '';
        if ( filter )
          _filter = '?' + filter
        else _id = id

        let response = await fetch( `/api/backoffice/${model_api}/${_id}${_filter}`, { 
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken" : csrftoken
          },
        })
        if ( !response || !response.ok) {
          // get error message from body or default to response status
          return null
        }
        const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = isJson && await response.json();
        return data
      }
      catch( error )  {
        console.log(error)
        return null
      }
    }
  },

  async getLegacy( ck, id) { 
    result = {}
    let model = "ProfileGeneral"
    let model_api = "profile_generals"
    let profile = null 
    profile = await this.get( ck, model_api, id, '')
    if ( !profile )
      return null;
    result[model] = profile
    let data = await resolveRelations( ck, model, profile, LEGACY_RELATIONS) 
    result = { ...result, ...data}
    //// get Layers
    model = "ProfileLayer"
    model_api = "profile_layers"
    filter = '?profile=' + profile.id
    let layers = await this.get( ck, model_api, null, filter )
    if ( layers !== nul && layers.length )  {
      result[model] = []
      for ( let i = 0; i < layers.length; i +=1 ) 
      { 
        const layer = layers[i];
        let result_layer = { "ProfileLayer" : layer }
        data = await resolveRelations( ck, model, layer, LEGACY_RELATIONS) 
        result_layer = { ...result_layer, ...data}
        result[model].push(result_layer)
      }
    }
    return result
  },

  async getMonitoring( ck, id) {
    result = {}
    let model = "MonitoringGeneral"
    let model_api = "monitoring_generals"
    let monitoring = null 
    monitoring = await this.get( ck, model_api, id, '')
    if ( !monitoring )
      return null;
    result[model] = monitoring
    let data = await resolveRelations( ck, model, monitoring, MONITORING_RELATIONS) 
    result = { ...result, ...data}
    //// get Layers
    model = "MonitoringLayer"
    model_api = "monitoring-layers"
    filter = '?site=' + monitoring.id
    let layers = await this.get( ck, model_api, null, filter )
    if ( layers !== nul && layers.length )  {
      result[model] = []
      for ( let i = 0; i < layers.length; i +=1 ) 
      { 
        const layer = layers[i];
        let result_layer = { "MonitoringLayer" : layer }
        data = await resolveRelations( ck, model, layer, MONITORING_RELATIONS) 
        result_layer = { ...result_layer, ...data}
        result[model].push(result_layer)
      }
    }
    //// get LabData
    model = "MonitoringLabData"
    model_api = "monitoring-lab-data"
    filter = '?site=' + monitoring.id
    let labdata = await this.get( ck, model_api, null, filter )
    if ( labdata !== nul && labdata.length )  {
      result[model] = []
      for ( let i = 0; i < labdata.length; i +=1 ) 
      { 
        const labdata = labdata[i];
        let result_labdata = { "MonitoringLabData" : labdata }
        result[model].push(result_labdata)
      }
    }
    return result
  }, 

  async listLegacy() {  
    let data = [];
    try {  
      let res = await fetch('/api/backoffice/profile-generals')
      if ( res && res.status === 200 ) 
        data = await res.json();
    } catch (e) { 
      console.log(e)
    } 
    return data;
  },  

  async listMonitoring() {  
    let data = [];
    try {  
      let res = await fetch('/api/backoffice/monitoring-generals')
      if ( res && res.status === 200 ) 
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

// create POST method: 
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

// remove DELETE method: 
  async remove(model, id) {
    let ok = false;
    try { 
      let model_api = this.MODELS[model].api 
      let res = fetch( `/api/backoffice/${model_api}/${id}`, {
        method: "DELETE",
      });
      if ( res && res.ok ) 
       ok = true;
    } catch (e) { 
    } 
    return ok;
  },

// update PUT method 
  async put(model, formdata) {
    let data = null;
    if ( formdata.id )
    try { 
      let model_api = this.MODELS[model].api 
      let res = fetch( `/api/backoffice/${model_api}/${id}`, {
        method: "PUT",
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

// update PATCH method 
  async update(model, formdata) {
    let data = null;
    if ( formdata.id )
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
  },

  async generateLegacyTreeNode(data) {
    let trees = {}
    trees['main'] = this.LEGACY_GENERAL_TREE_NODES
    trees['Layer1'] = this.LEGACY_LAYER_TREE_NODES
    trees['LabData1'] = this.LEGACY_LABDATA_TREE_NODES 
    return trees
  },

  async generateMonitoringTreeNode(data) {
    return null
  }
}

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};

export default ProfileService