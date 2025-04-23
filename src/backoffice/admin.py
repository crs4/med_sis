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
    list_display = ('code', 'date', 'location_name', 'lat_wgs84', 'lon_wgs84')
    search_fields = ('code', 'location_name')
    list_filter = ('date',)
    readonly_fields = ('code',)

@admin.register(ProfileLayer)
class ProfileLayerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'designation', 'layer_number', 'upper', 'lower')
    list_filter = ('profile',)
    search_fields = ('profile__code', 'designation')

@admin.register(LandUse)
class LandUseAdmin(admin.ModelAdmin):
    list_display = ('land_use', 'corine')
    search_fields = ('land_use__name', 'corine__name')

@admin.register(LandformTopography)
class LandformTopographyAdmin(admin.ModelAdmin):
    list_display = ('gradient_upslope', 'gradient_downslope', 'slope_aspect')
    search_fields = ('landform1__name', 'landform2__name')

@admin.register(ClimateAndWeather)
class ClimateAndWeatherAdmin(admin.ModelAdmin):
    list_display = ('climate_koppen', 'ecozone_shultz', 'season')
    search_fields = ('climate_koppen__name', 'ecozone_shultz__name')

@admin.register(Surface)
class SurfaceAdmin(admin.ModelAdmin):
    list_display = ('surface_crusts_area', 'bedrock_formation_name')
    search_fields = ('bedrock_formation_name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')

@admin.register(Genealogy)
class GenealogyAdmin(admin.ModelAdmin):
    list_display = ('old_code', 'project_id', 'pub_year')
    search_fields = ('old_code', 'reference')

@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('name', 'taxonomy', 'super')
    search_fields = ('name', 'taxonomy')
    list_filter = ('taxonomy',)
