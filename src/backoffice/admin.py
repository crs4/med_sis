from django.contrib import admin
from .models import (
    ProfileGeneral,
    ProfileLayer,
    LandUse,
    LandformTopography,
    ClimateAndWeather,
    Surface,
    Project,
    Genealogy,
    Taxonomy
)
        
@admin.register(ProfileGeneral)
class ProfileGeneralAdmin(admin.ModelAdmin):
    list_display = ('code', 'location', 'lat_wgs84', 'lon_wgs84',
                    'date', 'gps', 'surveyors','elev_m_asl','elev_dem',
                    'survey_m','notes','project','cls_sys')
    list_filter = ('code',)
    search_fields = ('code',)
    readonly_fields = ('code',)

@admin.register(ProfileLayer)
class ProfileLayerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'design', 'number', 'upper', 'lower')
    list_filter = ('profile',)
    search_fields = ('profile__code', 'design','number')

@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('land_use', 'corine')
    
@admin.register(LandformTopography)
class LandformTopographyAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    
@admin.register(ClimateAndWeather)
class ClimateAndWeatherAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    

@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title')

@admin.register(Genealogy)
class GenealogyAdmin(admin.ModelAdmin):
    list_display = ('old_code', 'id', 'pub_year','avail')
    search_fields = ('old_code', 'id','avail')

@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('id', 'taxonomy', 'super')
    search_fields = ('id', 'taxonomy')
