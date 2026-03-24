from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'updatelayers', UpdateLayersViewSet, basename='updatelayers')
router.register(r'xlsx-uploads', XLSxUploadViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'point-generals', PointGeneralViewSet)
router.register(r'landform-topographies', LandformTopographyViewSet)
router.register(r'climate-and-weathers', ClimateAndWeatherViewSet)
router.register(r'land-uses', LandUseViewSet)
router.register(r'surfaces', SurfaceViewSet)
router.register(r'surface-unevenness', SurfaceUnevennessViewSet)
router.register(r'point-layers', PointLayerViewSet)
router.register(r'layer-remnants', LayerRemnantsViewSet )
router.register(r'layer-coarse-fragments', LayerCoarseFragmentsViewSet)
router.register(r'layer-artefacts', LayerArtefactsViewSet)
router.register(r'layer-cracks', LayerCracksViewSet)
router.register(r'layer-matrix-colours', LayerMatrixColoursViewSet)
router.register(r'layer-lithogenic-variegates', LayerLithogenicVariegatesViewSet)
router.register(r'layer-redoximorphic', LayerRedoximorphicViewSet)
router.register(r'layer-coatings-bridges', LayerCoatingsBridgesViewSet)
router.register(r'layer-carbonates', LayerCarbonatesViewSet)
router.register(r'layer-gypsum', LayerGypsumViewSet)
router.register(r'layer-secondary-silica', LayerSecondarySilicaViewSet)
router.register(r'layer-consistences', LayerConsistenceViewSet)
router.register(r'layer-permafrost', LayerPermafrostViewSet) 
router.register(r'layer-organic-carbon', LayerOrganicCarbonViewSet)
router.register(r'layer-roots', LayerRootsViewSet)
router.register(r'layer-animal-activities', LayerAnimalActivityViewSet)
router.register(r'layer-human-alterations', LayerHumanAlterationsViewSet)
router.register(r'layer-degree-decomposition', LayerDegreeDecompositionViewSet)
router.register(r'layer-non-matrix-pores', LayerNonMatrixPoreViewSet)
router.register(r'layer-structures', LayerStructureViewSet)
router.register(r'lab-data', LabDataViewSet)
router.register(r'lab-data-extra-measures', LabDataExtraMeasureViewSet )
router.register(r'requests', RequestViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'taxonomies', TaxonomyViewSet)
router.register(r'taxonomy-values', TaxonomyValueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]