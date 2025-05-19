from django.contrib import admin
from .models import *

@admin.register(XLSxUpload)
class XLSxUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'title', 'editor', 'date', 'status')
    list_filter = ('id', 'type', 'title', 'editor', 'date', 'status')
    search_fields = ('id', 'type', 'title', 'editor', 'date', 'status',)
    readonly_fields = ('id',)

@admin.register(XSLxSheetConf)
class XSLxSheetConfAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'size', 'first','note',)
    list_filter = ('id', 'type', 'name', )
    search_fields = ('id', 'type', 'name', )
    readonly_fields = ('id',)

@admin.register(XSLxMapping)
class XSLxMappingConfAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'sheet', 'col', 'mod','fld','taxonomy',)
    list_filter =  ('id', 'type', 'sheet', 'col', 'mod','fld','taxonomy',)
    search_fields =  ('id', 'type', 'sheet', 'col', 'mod','fld','taxonomy',)
    readonly_fields = ('id',)

@admin.register(ProfileLayer)
class ProfileLayerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'design', 'number', 'upper', 'lower', 'lower_bound', )
    list_filter = ('profile',)
    search_fields = ('profile__code', 'design','number',)

@admin.register(ProfileGeneral)
class ProfileLayerAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'surveyors', 'location', 'lat_wgs84', 'lon_wgs84', 'gps', 'elev_m_asl', 'elev_dem', 'survey_m' )
    list_filter = ('code', 'date', 'surveyors', 'location','gps', 'elev_m_asl', 'elev_dem', 'survey_m')
    search_fields = ('code', 'date',)

@admin.register(CoarseFragments)
class CoarseFragmentsAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    readonly_fields = ('id',)

@admin.register(Cultivated)
class CultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    readonly_fields = ('id',)

@admin.register(NotCultivated)
class NotCultivatedAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    readonly_fields = ('id',)

@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    readonly_fields = ('id',)
       
@admin.register(LandformTopography)
class LandformTopographyAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)
    readonly_fields = ('id',)
    
@admin.register(ClimateAndWeather)
class ClimateAndWeatherAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    readonly_fields = ('id',)
    
@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    readonly_fields = ('id',)  

@admin.register(SurfaceCracks)
class SurfaceCracksAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    readonly_fields = ('id',) 

@admin.register(LitterLayer)
class LitterLayerAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    readonly_fields = ('id',)

@admin.register(SurfaceUnevenness)
class SurfaceUnevennessAdmin(admin.ModelAdmin):
    search_fields = ('id',) 
    readonly_fields = ('id',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title')
    readonly_fields = ('id',)

@admin.register(Genealogy)
class GenealogyAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'old_code', 'pub_year','avail')
    search_fields = ( 'id', 'old_code', 'avail')
    readonly_fields = ('id',)

@admin.register(GeoDataset)
class GeoDatasetAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'creation', 'update', 'type', 'geonode_id', 'note' )
    search_fields = ('name', 'creation', 'update', 'type', 'geonode_id')

@admin.register(Indicators)
class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'creation', 'type', 'note' )
    search_fields = ('name', 'creation', 'type' )

@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('id', 'taxonomy', 'super')
    search_fields = ('id', 'taxonomy')

@admin.register(LabData)
class TaxonomyAdmin(admin.ModelAdmin):
    search_fields = ('id', 'cls_sys', 'texture')
    readonly_fields = ('id',)

@admin.register(LayerRemnants)
class LayerRemnantsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerCoarseFragments)
class LayerCoarseFragmentsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerArtefacts)
class LayerArtefactsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerCracks)
class LayerCracksAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerStressFeatures)
class LayerStressFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerMatrixColours)
class LayerMatrixColoursAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerTextureColour)
class LayerTextureColourAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerLithogenicVariegates)
class LayerLithogenicVariegatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerRedoximorphicFeatures)
class LayerRedoximorphicFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerRedoximorphicColour)
class LayerRedoximorphicColourAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerCoatingsBridges)
class LayerCoatingsBridgesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerRibbonlikeAccumulations)
class LayerRibbonlikeAccumulationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerCarbonates)
class LayerCarbonatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerGypsum)
class LayerGypsumAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerSecondarySilica)
class LayerSecondarySilicaAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerConsistence)
class LayerConsistenceAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerSurfaceCrusts)
class LayerSurfaceCrustsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerPermafrostFeatures)
class LayerPermafrostFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerOrganicCarbon)
class LayerOrganicCarbonAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerRoots)
class LayerRootsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerAnimalActivity)
class LayerAnimalActivityAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerHumanAlterations)
class LayerHumanAlterationsAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerDegreeDecomposition)
class LayerDegreeDecompositionAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerNonMatrixPore)
class LayerNonMatrixPoreAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    readonly_fields = ('id',)

@admin.register(LayerStructure)
class LayerConsistenceAdmin(admin.ModelAdmin):
    readonly_fields = ('id','layer')
    search_fields = ('layer__id', 'id','layer',)
    readonly_fields = ('id',)
