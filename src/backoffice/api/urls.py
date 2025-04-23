from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileGeneralViewSet, TaxonomyViewSet, ProjectViewSet,
    GenealogyViewSet, LandformTopographyViewSet, ClimateAndWeatherViewSet,
    SurfaceViewSet, LandUseViewSet, CultivatedViewSet
)

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

urlpatterns = [
    path('', include(router.urls)),
]