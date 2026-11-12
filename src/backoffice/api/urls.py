from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import ldviews
from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class BackofficeAPIRootView(APIRootView):

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        data = dict(response.data)

        data['ldobservation'] = reverse(
            'ld-land-use-observation',
            kwargs={'profile_id': 'LOC724',},
            request=request,
        )

        data['ldplot'] = reverse(
            'ld-plot',
            kwargs={'plot_id': 'plot_lat40_26363_lon8_96142',},
            request=request,
        )

        data['ldprofile'] = reverse(
            'ld-profile',
            kwargs={'profile_id': 'LOC724'},
            request=request,
        )

        return Response(data)


router = DefaultRouter()
router.APIRootView = BackofficeAPIRootView
router.register(r'updatelayers', UpdateLayersViewSet, basename='updatelayers')
router.register(r'variogram', VariogramViewSet, basename='variogram')
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
router.register(r'extrameasures', ExtrameasureViewSet, basename='extrameasures' )
router.register(r'datasets', DatasetViewSet)
router.register(r'base-datasets', BaseDatasetViewSet)
router.register(r'photos', PhotoViewSet)
router.register(r'taxonomies', TaxonomyViewSet)
router.register(r'taxonomy-values', TaxonomyValueViewSet)
router.register(r'hydro-ptf-elaborations', HydroPtfElaborationViewSet)
router.register(r'hydro-ptf-prediction', HydroPtfPredictionViewSet, basename='hydro-ptf-prediction' )


urlpatterns = [
    path('ldobservation/<str:profile_id>/land-use/', ldviews.LandUseObservationView.as_view(), name='ld-land-use-observation',),
    path('ldplot/<str:plot_id>/', ldviews.LDPlotView.as_view(), name='ld-plot',),
    path('ldprofile/<str:profile_id>/', ldviews.LDProfileView.as_view(), name='ld-profile',),
    path('ldhorizon/<str:horizon_id>/', ldviews.LDHorizonView.as_view(), name="ldhorizon",),
    path('ldlayer/<str:layer_id>/', ldviews.LDLayerView.as_view(), name='ldlayer',),
    path('ldobservation/<str:labdata_id>/ph-h2o/', ldviews.LDPHObservationView.as_view(), name='ld-ph-h2o-observation',
),
    path('', include(router.urls)),
]