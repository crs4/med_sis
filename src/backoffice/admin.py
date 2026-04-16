from django.contrib import admin
from .models import *

@admin.register(XLSxUpload)
class XLSxUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'title', 'editor', 'date', 'status')
    list_filter = ('id', 'type', 'title', 'editor', 'date', 'status')
    search_fields = ('id', 'type', 'title', 'editor', 'date', 'status',)
@admin.register(PointLayer)
class PointLayerAdmin(admin.ModelAdmin):
    list_display = ('point', 'horizon', 'number', 'upper', 'lower', 'lower_bound', )
    list_filter = ('point',)
    search_fields = ('point__id', 'horizon','number',)
@admin.register(PointGeneral)
class PointGeneralAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'surveyors', 'location', 'lat_wgs84', 'lon_wgs84', 'gps', 'elev_m_asl', 'elev_dem', 'survey_m', )
    list_filter = ('id', 'date', 'surveyors', 'location','gps', 'elev_m_asl', 'elev_dem', 'survey_m', )
    search_fields = ('id', 'date',)  
@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)       
@admin.register(LandformTopography)
class LandformTopographyAdmin(admin.ModelAdmin):
    list_filter = ('id',)
    search_fields = ('id',)   
@admin.register(ClimateAndWeather)
class ClimateAndWeatherAdmin(admin.ModelAdmin):
    search_fields = ('id',)       
@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    search_fields = ('id',)    
@admin.register(SurfaceUnevenness)
class SurfaceUnevennessAdmin(admin.ModelAdmin):
    search_fields = ('id',)     
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title')
@admin.register(LabData)
class LabDataAdmin(admin.ModelAdmin):
    search_fields = ('id', 'l_number')
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
@admin.register(LayerMatrixColours)
class LayerMatrixColoursAdmin(admin.ModelAdmin):
    search_fields = ('id', )
@admin.register(LayerLithogenicVariegates)
class LayerLithogenicVariegatesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
@admin.register(LayerRedoximorphic)
class LayerRedoximorphicFeaturesAdmin(admin.ModelAdmin):
    search_fields = ('id', )
@admin.register(LayerCoatingsBridges)
class LayerCoatingsBridgesAdmin(admin.ModelAdmin):
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
@admin.register(LayerPermafrost)
class LayerPermafrostAdmin(admin.ModelAdmin):
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
class LayerStructureAdmin(admin.ModelAdmin):
    search_fields = ('id', 'layer__id',  )
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('id', )
@admin.register(LabDataExtraMeasure)
class LabDataExtraMeasureAdmin(admin.ModelAdmin):
    search_fields = ('id', 'labdata__id'  )
@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    search_fields = ('id',  )
@admin.register(TaxonomyValue)
class TaxonomyValueAdmin(admin.ModelAdmin):
    search_fields = ('id', 'taxonomy', 'value',  )
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'user', 'user_email', 'date', 'source', 'src_typename', 'status' )
    search_fields = ( 'name', 'user', 'user_email', 'src_typename', 'date', 'status' )   
