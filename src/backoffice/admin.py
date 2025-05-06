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
    search_fields = ('code',)
    list_filter = ('date',)
    readonly_fields = ('code',)

@admin.register(ProfileLayer)
class ProfileLayerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'design', 'number', 'upper', 'lower')
    list_filter = ('profile',)
    search_fields = ('profile__code', 'design','number')

@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_display = ('land_use', 'corine')
    
@admin.register(LandformTopography)
class LandformTopographyAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    
@admin.register(ClimateAndWeather)
class ClimateAndWeatherAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    

@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('code', 'title')

@admin.register(Genealogy)
class GenealogyAdmin(admin.ModelAdmin):
    list_display = ('old_code', 'code', 'pub_year','avail')
    search_fields = ('old_code', 'code','avail')

@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('name', 'taxonomy', 'super_cat')
    search_fields = ('name', 'taxonomy')
    list_filter = ('taxonomy',)
