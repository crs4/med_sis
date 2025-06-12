from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *


router = DefaultRouter()
router.register(r'profiles', ProfileGeneralViewSet)
router.register(r'taxonomies', TaxonomyViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'genealogies', GenealogyViewSet)
router.register(r'landform-topographies', LandformTopographyViewSet)
router.register(r'coarse-fragments', CoarseFragmentsViewSet)
router.register(r'climate-and-weathers', ClimateAndWeatherViewSet)
router.register(r'cultivated', CultivatedViewSet)
router.register(r'land-uses', LandUseViewSet)
router.register(r'not-cultivated', NotCultivatedViewSet)
router.register(r'surfaces', SurfaceViewSet)
router.register(r'surface-cracks', SurfaceCracksViewSet)
router.register(r'litter-layer', LitterLayerViewSet)
router.register(r'surface-unevenness', SurfaceUnevennessViewSet)
router.register(r'xlsx-sheet-conf', XSLxSheetConfViewSet)
router.register(r'xlsx-uploads', XLSxUploadViewSet)
router.register(r'xlsx-mapping', XSLxMappingViewSet)
router.register(r'profile-layers', ProfileLayerViewSet)
router.register(r'lab-data', LabDataViewSet)
router.register(r'layer-remnants', LayerRemnantsViewSet )
router.register(r'layer-coarse-fragments', LayerCoarseFragmentsViewSet)
router.register(r'layer-artefacts', LayerArtefactsViewSet)
router.register(r'layer-cracks', LayerCracksViewSet)
router.register(r'layer-stress-features', LayerStressFeaturesViewSet)
router.register(r'layer-matrix-colours', LayerMatrixColoursViewSet)
router.register(r'layer-texture-colours', LayerTextureColourViewSet)
router.register(r'layer-lithogenic-variegates', LayerLithogenicVariegatesViewSet)
router.register(r'layer-redoximorphic-features', LayerRedoximorphicFeaturesViewSet)
router.register(r'layer-redoximorphic-colours', LayerRedoximorphicColourViewSet)
router.register(r'layer-coatings-bridges', LayerCoatingsBridgesViewSet)
router.register(r'layer-ribbonlike-accumulations', LayerRibbonlikeAccumulationsViewSet)
router.register(r'layer-carbonates', LayerCarbonatesViewSet)
router.register(r'layer-gypsum', LayerGypsumViewSet)
router.register(r'layer-secondary-silica', LayerSecondarySilicaViewSet)
router.register(r'layer-consistences', LayerConsistenceViewSet)
router.register(r'layer-surface-crusts', LayerSurfaceCrustsViewSet)
router.register(r'layer-permafrost-features', LayerPermafrostFeaturesViewSet)
router.register(r'layer-organic-carbon', LayerOrganicCarbonViewSet)
router.register(r'layer-roots', LayerRootsViewSet)
router.register(r'layer-animal-activities', LayerAnimalActivityViewSet)
router.register(r'layer-human-alterations', LayerHumanAlterationsViewSet)
router.register(r'layer-degree-decomposition', LayerDegreeDecompositionViewSet)
router.register(r'layer-non-matrix-pores', LayerNonMatrixPoreViewSet)
router.register(r'layer-structures', LayerStructureViewSet)
router.register(r'indicators', IndicatorsViewSet)
router.register(r'geo-datasets', GeoDatasetViewSet)

 
urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^taxonomies/(?P<pk>[^/]+)/$', 
            views.TaxonomyViewSet.as_view({
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            }), 
            name='taxonomy-detail-with-dots'),
]