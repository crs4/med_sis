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

@admin.register(SampleLayer)
class SampleLayerAdmin(admin.ModelAdmin):
    list_display = ('sample', 'design', 'number', 'upper', 'lower', 'lower_bound')
    list_filter = ('sample', 'number', 'upper', 'lower')
    search_fields = ('profile__id', 'design','number')

@admin.register(SampleGeneral)
class SampleGeneralAdmin(admin.ModelAdmin):
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
    

@admin.register(SampleCultivated)
class SampleCultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(SampleNotCultivated)
class SampleNotCultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    

@admin.register(SampleLandUse)
class SampleLandUseAdmin(admin.ModelAdmin):
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
    

@admin.register(SampleCoarseFragments)
class SampleCoarseFragmentsAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    
      
@admin.register(SampleLandformTopography)
class SampleLandformTopographyAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    
    
@admin.register(SampleClimateAndWeather)
class SampleClimateAndWeatherAdmin(admin.ModelAdmin):
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
    

@admin.register(SampleSurface)
class SampleSurfaceAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
      

@admin.register(SampleSurfaceCracks)
class SampleSurfaceCracksAdmin(admin.ModelAdmin):
    search_fields = ('id',)
     

@admin.register(SampleLitterLayer)
class SampleLitterLayerAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    

@admin.register(SampleSurfaceUnevenness)
class SampleSurfaceUnevennessAdmin(admin.ModelAdmin):
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
    

@admin.register(SampleLabData)
class SampleLabDataAdmin(admin.ModelAdmin):
    search_fields = ('id', 'upper', 'lower', 'cls_sys', 'texture')

@admin.register(SampleLayerRemnants)
class SampleLayerRemnantsAdmin(admin.ModelAdmin):
    search_fields = ('id', )

@admin.register(SampleLayerCoarseFragments)
class SampleLayerCoarseFragmentsAdmin(admin.ModelAdmin):
    search_fields = ('id', )

@admin.register(SampleLayerArtefacts)
class SampleLayerArtefactsAdmin(admin.ModelAdmin):
    search_fields = ('id', )

@admin.register(SampleLayerCracks)
class SampleLayerCracksAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerStressFeatures)
class SampleLayerStressFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerMatrixColours)
class SampleLayerMatrixColoursAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerCoarserTextured)
class SampleLayerCoarserTexturedAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerLithogenicVariegates)
class SampleLayerLithogenicVariegatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerRedoximorphicFeatures)
class SampleLayerRedoximorphicFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerRedoximorphicColour)
class SampleLayerRedoximorphicColourAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerCoatingsBridges)
class SampleLayerCoatingsBridgesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerRibbonlikeAccumulations)
class SampleLayerRibbonlikeAccumulationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerCarbonates)
class SampleLayerCarbonatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerGypsum)
class SampleLayerGypsumAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerSecondarySilica)
class SampleLayerSecondarySilicaAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerConsistence)
class SampleLayerConsistenceAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleSurfaceCrusts)
class SampleLayerSurfaceCrustsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerPermafrostFeatures)
class SampleLayerPermafrostFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerOrganicCarbon)
class SampleLayerOrganicCarbonAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerRoots)
class SampleLayerRootsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerAnimalActivity)
class SampleLayerAnimalActivityAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerHumanAlterations)
class SampleLayerHumanAlterationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerDegreeDecomposition)
class SampleLayerDegreeDecompositionAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerNonMatrixPore)
class SampleLayerNonMatrixPoreAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    

@admin.register(SampleLayerStructure)
class SampleLayerStructureAdmin(admin.ModelAdmin):
    search_fields = ('layer__id', 'id','layer',)
    
