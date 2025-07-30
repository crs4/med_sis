from django.contrib import admin
from .models import *

@admin.register(XLSxUpload)
class XLSxUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'title', 'editor', 'date', 'status')
    list_filter = ('id', 'type', 'title', 'editor', 'date', 'status')
    search_fields = ('id', 'type', 'title', 'editor', 'date', 'status',)
    

@admin.register(ProfileLayer)
class ProfileLayerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'design', 'number', 'upper', 'lower', 'lower_bound', )
    list_filter = ('profile',)
    search_fields = ('profile__id', 'design','number',)

@admin.register(ProfileGeneral)
class ProfileGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'surveyors', 'location', 'lat_wgs84', 'lon_wgs84', 'gps', 'elev_m_asl', 'elev_dem', 'survey_m' )
    list_filter = ('id', 'date', 'surveyors', 'location','gps', 'elev_m_asl', 'elev_dem', 'survey_m')
    search_fields = ('id', 'date',)

@admin.register(MonitoringLayer)
class MonitoringLayerAdmin(admin.ModelAdmin):
    list_display = ('site', 'design', 'number', 'upper', 'lower', 'lower_bound')
    list_filter = ('site', 'number', 'upper', 'lower')
    search_fields = ('site__id', 'design','number')

@admin.register(MonitoringGeneral)
class MonitoringGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'surveyors', 'location', 'lat_wgs84', 'lon_wgs84', 'gps', 'elev_m_asl', 'elev_dem', 'survey_m' )
    list_filter = ('id', 'date', 'surveyors', 'location','gps', 'elev_m_asl', 'elev_dem', 'survey_m')
    search_fields = ('id', 'date')

@admin.register(Cultivated)
class CultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(NotCultivated)
class NotCultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(MonitoringCultivated)
class MonitoringCultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(MonitoringNotCultivated)
class MonitoringNotCultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(MonitoringLandUse)
class MonitoringLandUseAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(CoarseFragments)
class CoarseFragmentsAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    
      
@admin.register(LandformTopography)
class LandformTopographyAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    
    
@admin.register(ClimateAndWeather)
class ClimateAndWeatherAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    

@admin.register(MonitoringCoarseFragments)
class MonitoringCoarseFragmentsAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    
      
@admin.register(MonitoringLandformTopography)
class MonitoringLandformTopographyAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    
    
@admin.register(MonitoringClimateAndWeather)
class MonitoringClimateAndWeatherAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    
    
@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
      

@admin.register(SurfaceCracks)
class SurfaceCracksAdmin(admin.ModelAdmin):
    search_fields = ('id',)
     

@admin.register(LitterLayer)
class LitterLayerAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    

@admin.register(SurfaceUnevenness)
class SurfaceUnevennessAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    

@admin.register(MonitoringSurface)
class MonitoringSurfaceAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
      

@admin.register(MonitoringSurfaceCracks)
class MonitoringSurfaceCracksAdmin(admin.ModelAdmin):
    search_fields = ('id',)
     

@admin.register(MonitoringLitterLayer)
class MonitoringLitterLayerAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    

@admin.register(MonitoringSurfaceUnevenness)
class MonitoringSurfaceUnevennessAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title')
    

@admin.register(Indicator)
class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'creation', 'description', 'type', 'keywords' )
    search_fields = ( 'name', 'creation', 'description', 'type', 'keywords' )

@admin.register(Request)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'username', 'useremail', 'creation', 'mgr', 'mgrname','mgremail', 'mgrmsg',
                     'type', 'dataid', 'cancelled', 'purpose', 'datefrom', 'dateto', 'depth', 'status', 'anchor', 'geonode' )
    search_fields = ( 'user', 'user_name', 'user_email', 'creation', 'mgr', 'mgrname','mgremail',
                      'cancelled', 'type', 'datefrom', 'dateto', 'depth' )
 
    
@admin.register(LabData)
class LabDataAdmin(admin.ModelAdmin):
    search_fields = ('id', 'cls_sys', 'texture')
    

@admin.register(LayerRemnants)
class LayerRemnantsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerCoarseFragments)
class LayerCoarseFragmentsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerArtefacts)
class LayerArtefactsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerCracks)
class LayerCracksAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerStressFeatures)
class LayerStressFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerMatrixColours)
class LayerMatrixColoursAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerCoarserTextured)
class LayerTextureColourAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerLithogenicVariegates)
class LayerLithogenicVariegatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerRedoximorphicFeatures)
class LayerRedoximorphicFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerRedoximorphicColour)
class LayerRedoximorphicColourAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerCoatingsBridges)
class LayerCoatingsBridgesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerRibbonlikeAccumulations)
class LayerRibbonlikeAccumulationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerCarbonates)
class LayerCarbonatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerGypsum)
class LayerGypsumAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerSecondarySilica)
class LayerSecondarySilicaAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerConsistence)
class LayerConsistenceAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerSurfaceCrusts)
class LayerSurfaceCrustsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerPermafrostFeatures)
class LayerPermafrostFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerOrganicCarbon)
class LayerOrganicCarbonAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerRoots)
class LayerRootsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerAnimalActivity)
class LayerAnimalActivityAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerHumanAlterations)
class LayerHumanAlterationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerDegreeDecomposition)
class LayerDegreeDecompositionAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerNonMatrixPore)
class LayerNonMatrixPoreAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(LayerStructure)
class LayerConsistenceAdmin(admin.ModelAdmin):
    search_fields = ('layer__id', 'id','layer',)
    

@admin.register(MonitoringLabData)
class MonitoringLabDataAdmin(admin.ModelAdmin):
    search_fields = ('id', 'upper', 'lower', 'cls_sys', 'texture')

@admin.register(MonitoringLayerRemnants)
class MonitoringLayerRemnantsAdmin(admin.ModelAdmin):
    search_fields = ('id', )

@admin.register(MonitoringLayerCoarseFragments)
class MonitoringLayerCoarseFragmentsAdmin(admin.ModelAdmin):
    search_fields = ('id', )

@admin.register(MonitoringLayerArtefacts)
class MonitoringLayerArtefactsAdmin(admin.ModelAdmin):
    search_fields = ('id', )

@admin.register(MonitoringLayerCracks)
class MonitoringLayerCracksAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerStressFeatures)
class MonitoringLayerStressFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerMatrixColours)
class MonitoringLayerMatrixColoursAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerCoarserTextured)
class MonitoringLayerCoarserTexturedAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerLithogenicVariegates)
class MonitoringLayerLithogenicVariegatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerRedoximorphicFeatures)
class MonitoringLayerRedoximorphicFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerRedoximorphicColour)
class MonitoringLayerRedoximorphicColourAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerCoatingsBridges)
class MonitoringLayerCoatingsBridgesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerRibbonlikeAccumulations)
class MonitoringLayerRibbonlikeAccumulationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerCarbonates)
class MonitoringLayerCarbonatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerGypsum)
class MonitoringLayerGypsumAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerSecondarySilica)
class MonitoringLayerSecondarySilicaAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerConsistence)
class MonitoringLayerConsistenceAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringSurfaceCrusts)
class MonitoringLayerSurfaceCrustsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerPermafrostFeatures)
class MonitoringLayerPermafrostFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerOrganicCarbon)
class MonitoringLayerOrganicCarbonAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerRoots)
class MonitoringLayerRootsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerAnimalActivity)
class MonitoringLayerAnimalActivityAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerHumanAlterations)
class MonitoringLayerHumanAlterationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerDegreeDecomposition)
class MonitoringLayerDegreeDecompositionAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerNonMatrixPore)
class MonitoringLayerNonMatrixPoreAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(MonitoringLayerStructure)
class MonitoringLayerStructureAdmin(admin.ModelAdmin):
    search_fields = ('layer__id', 'id','layer',)
    
