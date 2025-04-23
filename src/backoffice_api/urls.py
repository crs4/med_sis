from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileGeneralViewSet, TaxonomyViewSet, ProjectViewSet, GenealogyViewSet, LandformTopographyViewSet, ClimateAndWeatherViewSet, SurfaceViewSet, LandUseViewSet, CultivatedViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileGeneralViewSet)
router.register(r'taxonomies', TaxonomyViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'genealogies', GenealogyViewSet)
router.register(r'landform', LandformTopographyViewSet)
router.register(r'climate', ClimateAndWeatherViewSet)
router.register(r'surface', SurfaceViewSet)
router.register(r'landuse', LandUseViewSet)
router.register(r'cultivated', CultivatedViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 