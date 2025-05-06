from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'profiles', ProfileGeneralViewSet)
router.register(r'taxonomies', TaxonomyViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'genealogies', GenealogyViewSet)
router.register(r'landform-topographies', LandformTopographyViewSet)
router.register(r'climate-weather', ClimateAndWeatherViewSet)
router.register(r'surfaces', SurfaceViewSet)
router.register(r'land-uses', LandUseViewSet)
router.register(r'cultivated', CultivatedViewSet)
router.register(r'not-cultivated', NotCultivatedViewSet)
router.register(r'surface-cracks', SurfaceCracksViewSet)
router.register(r'litter-layer', LitterLayerViewSet)
router.register(r'surface-unevenness', SurfaceUnevennessViewSet)
router.register(r'coarse-fragments', CoarseFragmentsViewSet)
router.register(r'xlsx-sheet-conf', XSLxSheetConfViewSet)
router.register(r'xlsx-uploads', XLSxUploadViewSet)
router.register(r'xlsx-mapping', XSLxMappingViewSet)
router.register(r'lab-method', LabMethodViewSet)
router.register(r'lab-measurement', LabMeasurementViewSet)
router.register(r'profile-layers', ProfileLayerViewSet)
router.register(r'labdata', LabDataViewSet)
router.register(r'labdata-measurement', LabDataMeasurementViewSet)
 
urlpatterns = [
    path('', include(router.urls)),
]