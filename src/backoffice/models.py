from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import transaction


def validate_percentage(value):
    if value is not None and (value < 0 or value > 100):
        raise ValidationError(_('Il valore deve essere compreso tra 0 e 100'))

def validate_positive(value):
    if value is not None and value < 0:
        raise ValidationError(_('Il valore deve essere positivo'))

def validate_latitude(value):
    if value is not None and (value < -90 or value > 90):
        raise ValidationError(_('La latitudine deve essere compresa tra -90 e 90'))

def validate_longitude(value):
    if value is not None and (value < -180 or value > 180):
        raise ValidationError(_('La longitudine deve essere compresa tra -180 e 180'))

class Taxonomy(models.Model):
    id = models.TextField(primary_key=True, db_comment='Taxonomy name')
    descr = models.TextField( db_comment='Taxonomy\'s description', null=True, blank=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'taxonomy'
        db_table_comment = 'Taxonomy data'
        permissions = (
            ('view', 'can view data'),
            ('add', 'can add data'),
            ('change', 'can change data'),
            ('delete', 'can delete data'),
        )
class TaxonomyValue(models.Model):
    id = models.TextField(primary_key=True, db_comment='Taxonomy value identifier in the form [taxonomy_id]:[value]  ')
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='values_taxonomy_set', db_comment='Taxonomy id') 
    value = models.TextField(db_comment='Taxonomy value')
    descr = models.TextField( db_comment='Taxonomy value\'s description', null=True, blank=True)
    
    objects = models.Manager().using('backoffice')
    class Meta:
        managed = True
        db_table = 'taxonomy_value'
        db_table_comment = 'Taxonomy\'s values '
        permissions = (
            ('view', 'can view data'),
            ('add', 'can add data'),
            ('change', 'can change data'),
            ('delete', 'can delete data'),
        )
###########################
## XLSx Uploads
###########################
UPLOAD_RESULTS = [
    ("UPLOADED" , "UPLOADED"),
    ("IN_PROCESS" , "IN_PROCESS"),
    ("IMPORT_SUCCESS" , "IMPORT_SUCCESS"),
    ("IMPORT_WITH_ERROR" , "IMPORT_WITH_ERROR"),
    ("CRITICAL_ERROR" , "CRITICAL_ERROR"),
]  
UPLOAD_TYPES = [
    ("XLS_P" , "XLSx Point Soil Data upload"),
    ("XLS_PJ" , "XLSx Profiles Genealogy upload"),
    ("XLS_PH" , "XLSx Photo metadata upload"),
    ("XLS_EM", "XLSx Laboratory Extra data"),                    
]
UPLOAD_OPERATION = [
    ("POST" , "Create new"),
    ("PUT" , "Create or Update all fields"),
    ("PATCH" , "If exist update some fields")
]

class XLSxUpload(models.Model):
    type = models.TextField(choices=UPLOAD_TYPES, db_comment='Type of the upload')
    title = models.TextField(db_comment='sheet name')
    report = models.JSONField( db_comment='Report of the upload')
    data = models.JSONField( db_comment='Data uploaded')
    editor = models.TextField( db_comment='Owner of the upload', null=True, blank=True)
    date = models.DateTimeField( db_comment='Date of the upload')
    status = models.TextField( choices=UPLOAD_RESULTS, db_comment='Status of the upload' )
    operation = models.TextField( choices=UPLOAD_OPERATION, db_comment='http method POST/PUT/PATCH ' )

    objects = models.Manager().using('backoffice')

    def start_processing(self):
        """Avvia il processo di importazione dei dati"""
        from .tasks import process_xlsx_upload
        if self.status == "UPLOADED":
            self.status = "IN_PROCESS"
            self.save(using='backoffice')
            # Questo garantisce che il task parta SOLO quando il dato è realmente scritto su DB.
            transaction.on_commit(
                lambda: process_xlsx_upload.delay(self.id),
                using='backoffice')
            return True
        return False

    class Meta:
        managed = True
        db_table = 'xlsx_upload'
        db_table_comment = 'XLSx Data Uploads'
        permissions = (
            ('view', 'can view data'),
            ('add', 'can add data'),
            ('change', 'can change data'),
            ('delete', 'can delete data'),
        )

###########################
# Projects - "Projects" sheet
###########################
class Project(models.Model):
    id = models.TextField(primary_key=True, db_comment='Project identifier ')
    title = models.TextField(blank=True, null=True, db_comment='project name')
    descr = models.TextField(blank=True, null=True, db_comment='project description')
    refer = models.TextField(blank=True, null=True, db_comment='reference')
    pub_year = models.IntegerField(blank=True, null=True, db_comment='year of pubblication')
    web_link = models.TextField(blank=True, null=True)
    avail = models.TextField(blank=True, null=True, db_comment='Data availability and/or use restrictions')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'projects'
        db_table_comment = 'projects descriptor'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

###########################
# Soil Point Data 
###########################

### Point General - "General and Surface" sheet
class LandformTopography(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    grad_ups = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface upslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    grad_downs = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface downslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    slope_asp = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If the profile lies on a slope, report the compass direction that the slope faces, viewed downslope; e.g., 225°')
    slope_shp = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landformtopography_slope_shp_set',  blank=True, null=True, db_comment='If the profile lies on a slope, report the slope shape in 2 directions: up-/downslope (perpendicular to the elevation contour, i.e. the vertical curvature) and across slope (along the elevation contour, i.e. the horizontal curvature); e.g., Linear (L), Convex (V) or Concave (C).')
    position = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landformtopography_position_set',  blank=True, null=True, db_comment='If the profile lies in an uneven terrain, report the profile position.')
    landform1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landformtopography_landform1_set',  blank=True, null=True, db_comment='Landform1 type.')
    landform2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landformtopography_landform2_set',  blank=True, null=True, db_comment='Landform2 type.')
    activity1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landformtopography_activity1_set',  blank=True, null=True, db_comment='Activity.')
    activity2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landformtopography_activity2_set',  blank=True, null=True, db_comment='Activity.')
    geo_descr = models.TextField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'landform_topography'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
class ClimateAndWeather(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    clim_koppen = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_clim_koppen_set',  blank=True, null=True)
    eco_shultz = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_eco_shultz_set',    blank=True, null=True)
    season = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_season_set',    blank=True, null=True)
    curr_weath = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_curr_weath_set',   blank=True, null=True)
    past_weath = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_past_weath_set',    blank=True, null=True)
    soil_temp = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_soil_temp_set',   blank=True, null=True)
    soil_moist = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='climateandweather_soil_moist_set',    blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'climate_weather'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        ) 
class LandUse(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    use = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_use_set',  blank=True, null=True)
    corine = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_corine_set',  blank=True, null=True)
    nc_gs_veget1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_gs_veget1_set',  blank=True, null=True)
    nc_gs_veget2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_gs_veget2_set',  blank=True, null=True)
    nc_gs_veget3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_gs_veget3_set',  blank=True, null=True)
    nc_gs_avg_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_gs_max_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_gs_area = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_gs_species1 = models.TextField(blank=True, null=True)
    nc_gs_species2 = models.TextField(blank=True, null=True)
    nc_gs_species3 = models.TextField(blank=True, null=True)
    nc_us_veget1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_us_veget1_set',  blank=True, null=True)
    nc_us_veget2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_us_veget2_set',  blank=True, null=True)
    nc_us_veget3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_us_veget3_set',  blank=True, null=True)
    nc_us_avg_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_us_max_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_us_area = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_us_species1 = models.TextField(blank=True, null=True)
    nc_us_species2 = models.TextField(blank=True, null=True)
    nc_us_species3 = models.TextField(blank=True, null=True)
    nc_ms_veget1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_ms_veget1_set',  blank=True, null=True)
    nc_ms_veget2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_ms_veget2_set',  blank=True, null=True)
    nc_ms_veget3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_nc_ms_veget3_set',  blank=True, null=True)
    nc_ms_avg_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_ms_max_height = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_ms_area = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nc_ms_species1 = models.TextField(blank=True, null=True)
    nc_ms_species2 = models.TextField(blank=True, null=True)
    nc_ms_species3 = models.TextField(blank=True, null=True)
    cult_type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_cult_type_set',  blank=True, null=True, db_comment='value from p_cultivation_type ')
    cult_actual1 = models.TextField(blank=True, null=True, db_comment='actual dominant specie')
    cult_actual2 = models.TextField(blank=True, null=True, db_comment='actual second specie')
    cult_actual3 = models.TextField(blank=True, null=True, db_comment='actual third specie')
    cult_cessation = models.DateField(blank=True, null=True, db_comment='editable if last dominant specie is NOT NULL')
    cult_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cult_prod1_tech = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_cult_prod1_tech_set',  blank=True, null=True, db_comment='Report the techniques that refer to the surrounding area of the soil profile. If more than one type of technique is present, report in the array up to three, the dominant one first. Value from p_productivity_techniques')
    cult_prod2_tech = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_cult_prod2_tech_set',  blank=True, null=True)
    cult_prod3_tech = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='landuse_cult_prod3_tech_set',  blank=True, null=True)
    cult_last1 = models.TextField(blank=True, null=True, db_comment="last dominant specie, editable if actual_species1 is NULL")
    cult_last2 = models.TextField(blank=True, null=True, db_comment="Second last specie, editable if actual_species2 is NULL ")
    cult_last3 = models.TextField(blank=True, null=True, db_comment="Third last specie, editable if actual_species3 is NULL ")
    cult_rotation1 = models.TextField(blank=True, null=True, db_comment='Report the dominant specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the most frequent)')
    cult_rotation2 = models.TextField(blank=True, null=True, db_comment='Report the second specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    cult_rotation3 = models.TextField(blank=True, null=True, db_comment='Report the third specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'land_use'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
class Surface(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    crust_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    ground_form = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_ground_form_set',  blank=True, null=True, db_comment='Patterned ground form field')
    tech_alter = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_tech_alter_set',  blank=True, null=True)
    bedr_form = models.TextField(blank=True, null=True)
    bedr_lith = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_bedr_lith_set',  blank=True, null=True)
    outc_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    outc_dist = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    outc_size = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    ground_wat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True)
    wat_above = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_wat_above_set',  blank=True, null=True)
    wat_drain = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_wat_drain_set',  blank=True, null=True)
    wat_repell = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_wat_repell_set',  blank=True, null=True)
    desert_ven = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    desert_var = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    debris_type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_debris_type_set',  blank=True, null=True)
    debris_cover = models.TextField(blank=True, null=True)
    natural_alterations = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_natural_alterations_set',  blank=True, null=True)
    pat_comp_type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_pat_comp_type_set',  blank=True, null=True)
    pat_comp_cover = models.TextField(blank=True, null=True)
    saline_efflorescence = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_saline_efflorescence_set', blank=True, null=True)
    worm_cast = models.TextField(blank=True, null=True)
    lp_signs_ploughing = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_lp_signs_ploughing_set', blank=True, null=True)
    lp_direction_ploughing = models.TextField(blank=True, null=True)
    lp_tillage_mode = models.TextField(blank=True, null=True)
    use_of_inputs = models.TextField(blank=True, null=True)
    irrigation = models.TextField(blank=True, null=True)
    conservation = models.TextField(blank=True, null=True)
    cs_total_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cs_class1size = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cs_class1size_set',  blank=True, null=True)
    cs_class2size = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cs_class2size_set',   blank=True, null=True)
    cs_class3size = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cs_class3size_set',   blank=True, null=True)
    cs_class1area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cs_class2area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cs_class3area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    litter_avg_thick = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    litter_area = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    litter_max_thick = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    cracks_width1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_width1_set',  blank=True, null=True)
    cracks_dist1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_dist1_set',  blank=True, null=True)
    cracks_spat_arr1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_spat_arr1_set',  blank=True, null=True)
    cracks_persist1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_persist1_set',  blank=True, null=True)
    cracks_width2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_width2_set',  blank=True, null=True)
    cracks_dist2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_dist2_set',  blank=True, null=True)
    cracks_spat_arr2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_spat_arr2_set',  blank=True, null=True)
    cracks_persist2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surface_cracks_persist2_set',  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'surface'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
class SurfaceUnevenness(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    position = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surfaceunevenness_position_set',  blank=True, null=True)
    nat_avg_h = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_elev = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_dist = models.DecimalField(max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    hum_type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surfaceunevenness_hum_type1_set',  blank=True, null=True)
    hum_type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surfaceunevenness_hum_type2_set',  blank=True, null=True)
    hum_ter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_w = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_d = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    ero_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    ero_type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surfaceunevenness_ero_type_set',  blank=True, null=True)
    ero_degree = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surfaceunevenness_ero_degree_set',  blank=True, null=True)
    ero_activ = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='surfaceunevenness_ero_activ_set',  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'surface_unevenness'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )    
class PointGeneral(models.Model):
    id = models.TextField(primary_key=True, db_comment='point identifier')
    type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointgeneral_type_set', blank=True, null=True, db_comment='point data type')
    date = models.DateField(blank=True, null=True, db_comment='date of the description')
    surveyors = models.TextField(blank=True, null=True, db_comment='surveyors names comma separated')
    location = models.TextField(blank=True, null=True, db_comment='Name of the point location')
    lat_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Latitude in decimal degree')
    lon_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Longitude in decimal degree')
    gps = models.BooleanField(blank=True, null=True, db_comment='is a gps acquisition?')
    elev_m_asl = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude above the sea level in meter')
    elev_dem = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude in meters retrived from a dem in meter')
    survey_m = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointgeneral_survey_m_set',   blank=True, null=True, db_comment='The code of the survey method')
    notes = models.TextField(blank=True, null=True)
    project = models.TextField(blank=True, null=True)

    cls_sys = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointgeneral_cls_sys_set',  blank=True, null=True, db_comment='Original classification system')
    old_cls = models.TextField(blank=True, null=True, db_comment='Original classification of the point ')
    old_id = models.TextField(blank=True, null=True, db_comment='Original point code')
    new_cls = models.TextField(blank=True, null=True, db_comment='New classification of the point based on the WRB 4TH EDITION. ')
    
    landuse =  models.OneToOneField(LandUse, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Land Use ')
    surface =  models.OneToOneField(Surface, on_delete=models.SET_DEFAULT,default=None, blank=True, null=True, db_comment='Surface ')
    landformtopography = models.OneToOneField(LandformTopography, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='landform_topography')
    climateandweather = models.OneToOneField(ClimateAndWeather, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Climate weather')
    surfaceunevenness =  models.OneToOneField(SurfaceUnevenness, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Surface Unevenness')
    
    
    ## pointlayer_point_set PointLayer

    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'point_general'
        db_table_comment = 'The Soil point main table'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
### Lab Data - "Lab data" and "Lab data by sampling depth" sheets
class LabData(models.Model):
    id = models.TextField(primary_key=True, db_comment='labdata identifier')
    point = models.ForeignKey(PointGeneral, on_delete=models.CASCADE, related_name='labdata_point_set', db_comment='Foreign Key field: point') 
    upper = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_positive],  db_comment='Sampling upper boundary' , blank=True, null=True)
    lower = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_positive],  db_comment='Sampling lower boundary' , blank=True, null=True)
    horizon = models.TextField( db_comment='Horizon sequence code', blank=True, null=True)
    l_number = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_positive],  db_comment='Layer Number' , blank=True, null=True)
    gravel = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_percentage],  db_comment='Gravel content (%)' , blank=True, null=True)
    cls_sys =  models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_cls_sys_set',  db_comment='Classification system used for texture of fine earth', blank=True, null=True)
    texture = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_texture_set',  db_comment='texture class', blank=True, null=True)      
    sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Sand  (percentage of the fine earth)', blank=True, null=True)
    v_c_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Very coarse sand (percentage of the fine earth)', blank=True, null=True)
    c_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Coarse sand (percentage of the fine earth)', blank=True, null=True)
    m_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Medium sand (percentage of the fine earth)', blank=True, null=True)
    f_sand = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Fine sand (percentage of the fine earth)', blank=True, null=True)
    v_f_sand  = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Very Fine sand (percentage of the fine earth)', blank=True, null=True)
    met_sand = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_sand_set',  blank=True, null=True)
    silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Silt (percentage of the fine earth)', blank=True, null=True)
    c_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Coarse silt (percentage of the fine earth)', blank=True, null=True)
    f_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Fine silt  (percentage of the fine earth)', blank=True, null=True)
    met_silt = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_silt_set',   blank=True, null=True)
    clay = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Clay  (percentage of the fine earth)', blank=True, null=True)
    met_clay = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_clay_set_set',  blank=True, null=True)
    bulk_dens = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Bulk density (g/cm3)'	, blank=True, null=True)
    met_bulk_dens = models.TextField(blank=True, null=True)
    slake_test = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Bulk density (g/cm3)'	, blank=True, null=True)
    met_slake_test = models.TextField(blank=True, null=True)
    el_cond = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Electric conductivity (dS/m)', blank=True, null=True)
    met_el_cond = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_clay_set',  db_comment='Method used for Electric conductivity', blank=True, null=True)
    hy_cond = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Hydraulic conductivity at saturation (mm/h)', blank=True, null=True)
    met_hy_cond = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_hy_cond_set',  db_comment='Method used for Hydraulic conductivity at saturation', blank=True, null=True)
    satur = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Saturation (percentage)', blank=True, null=True)
    field_cap = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Field capacity (percentage)', blank=True, null=True)
    wilting_p = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Wilting point (percentage)', blank=True, null=True)
    awc = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Wilting point (percentage)', blank=True, null=True)
    met_s_f_w = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_s_f_w_set',  db_comment='Method used for saturation, field capacity, wilting point', blank=True, null=True)
    acidity = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    met_acidity = models.TextField(db_comment='Method used for Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    ph_h2o = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (H2O)', blank=True, null=True)
    met_ph_h20 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_ph_h20_set',  db_comment='Method used for pH (H2O)', blank=True, null=True)
    ph_kcl = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (KCl)', blank=True, null=True)
    met_ph_kcl = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_ph_kcl_set',  db_comment='Method used for pH (KCl)', blank=True, null=True)
    ph_ccl = models.DecimalField( max_digits=30, decimal_places=10, db_comment='pH (CaCl2)', blank=True, null=True)
    met_ph_ccl = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_ph_ccl_set',  db_comment='Method used for pH (CaCl2)',  blank=True, null=True)
    org_car = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Organic Carbon content (g/kg)', blank=True, null=True)
    met_org_car = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_org_car_set',  db_comment='Method used for Organic Carbon content', blank=True, null=True)
    org_mat = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Organic matter content (percentage)', blank=True, null=True)
    met_org_mat = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_org_mat_set',  db_comment='Method used for organic matter content', blank=True, null=True)
    caco3_content = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CaCO3 content (percentage)', blank=True, null=True)
    met_content_caco3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_content_caco3_set',  db_comment='Method used for CaCO3 content',  blank=True, null=True)
    active_caco3 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CaCO3 content (percentage)', blank=True, null=True)
    met_active_caco3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_active_caco3_set',  db_comment='Method used for active CaCO3',  blank=True, null=True)
    gypsum = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Gypsum content (percentage)', blank=True, null=True)
    met_gypsum = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_gypsum_set',  db_comment='Method used for Gypsum content',  blank=True, null=True)
    cec = models.DecimalField( max_digits=30, decimal_places=10, db_comment='CEC (cmol/Kg)', blank=True, null=True)
    met_cec = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_cec_set',  db_comment='Method used for CEC',  blank=True, null=True)
    ca = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Ca++ (cmol/Kg)', blank=True, null=True)
    mg = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Mg++ (cmol/Kg)', blank=True, null=True)
    na = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Na+ (cmol/Kg)', blank=True, null=True)
    k = models.DecimalField( max_digits=30, decimal_places=10, db_comment='K+ (cmol/Kg)', blank=True, null=True)
    met_exc = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_exc_set',  db_comment='EXCHANGEABLE CATIONS METHOD',  blank=True, null=True)
    base_saturation = models.DecimalField( max_digits=30, decimal_places=10, db_comment='base saturation', blank=True, null=True)          
    esp = models.DecimalField( max_digits=30, decimal_places=10, db_comment='ESP (ratio)', blank=True, null=True)  
    sol_ca = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Sol. Ca++ (cmol/L)', blank=True, null=True)
    sol_mg = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Sol. Mg++ (cmol/L)', blank=True, null=True)
    sol_na = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Sol. Na++ (cmol/L)', blank=True, null=True)
    met_sol_cations = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_sol_cations_set',  db_comment='Method used for soluble cations',  blank=True, null=True)
    sar = models.DecimalField( max_digits=30, decimal_places=10, db_comment='SAR (ratio)', blank=True, null=True)
    n_tot = models.DecimalField( max_digits=30, decimal_places=10, db_comment='N tot content (g/Kg)', blank=True, null=True)
    met_n_tot = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_n_tot_set',  db_comment='Method used for N tot content',  blank=True, null=True)
    p_cont = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Available P content(mg/kg)', blank=True, null=True)
    met_p_cont = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_p_cont_set',  db_comment='Method used for available P content',  blank=True, null=True)
    nh4 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_nh4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_nh4_set', blank=True, null=True)
    no3 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_no3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_no3_set', blank=True, null=True)
    roc = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    toc400 = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_roc_toc400 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_roc_toc400_set',blank=True, null=True)
    feox = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Feox (g/kg)', blank=True, null=True)
    fed = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fed (g/kg)', blank=True, null=True)
    fep = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fep (g/kg)', blank=True, null=True)
    fe_tot = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Fe tot (g/kg)', blank=True, null=True)
    met_fe_tot = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_fe_tot_set',blank=True, null=True)
    mn = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Mn (mg/kg)', blank=True, null=True)
    met_mn = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_mn_set',  db_comment='Method used for Mn', blank=True, null=True)
    zn = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Zn (mg/kg)', blank=True, null=True)
    met_zn = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_zn_set',  db_comment='Method used for Zn', blank=True, null=True)
    cu = models.DecimalField( max_digits=30, decimal_places=10, db_comment='Cu (mg/kg)', blank=True, null=True)
    met_cu = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_cu_set',  db_comment='Method used for Cu', blank=True, null=True) 
    pb = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_pb = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_pb_set', blank=True, null=True)
    hg = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_hg = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_hg_set', blank=True, null=True)
    cd = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_cd = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_cd_set', blank=True, null=True)
    ni = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_ni = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_ni_set', blank=True, null=True)
    sb = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_sb = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_sb_set', blank=True, null=True)
    cr = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_cr = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_cr_set', blank=True, null=True)
    as_value = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_as = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_as_set', blank=True, null=True)
    co = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_co = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_co_set', blank=True, null=True)
    v = models.DecimalField( max_digits=30, decimal_places=10, db_comment='', blank=True, null=True)
    met_v = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdata_met_v_set', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  


    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'lab_data'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
### Point Layer - "Layer Description" sheet
class LayerRemnants(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    abundance = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cementing1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerremnants_cementing1_set',  blank=True, null=True)
    cementing2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerremnants_cementing2_set',  blank=True, null=True)
    size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerremnants_size1_set',  blank=True, null=True)
    size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerremnants_size2_set',  blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_remnants'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
class LayerCoarseFragments(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    litho_type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_litho_type1_set',  blank=True, null=True)
    litho_type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_litho_type2_set',  blank=True, null=True)
    litho_type3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_litho_type3_set',  blank=True, null=True)
    litho_type4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_litho_type4_set',  blank=True, null=True)
    size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_size1_set',  blank=True, null=True)
    size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_size2_set',  blank=True, null=True)
    size3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_size3_set',  blank=True, null=True)
    size4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_size4_set',  blank=True, null=True)
    weath1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_weath1_set',  blank=True, null=True)
    weath2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_weath2_set',  blank=True, null=True)
    weath3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_weath3_set',  blank=True, null=True)
    weath4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoarsefragments_weath4_set',  blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class1.')
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class2.')
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class3.')
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class4.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_coarse_fragments'
        db_table_comment = 'Coarse fragments. A coarse fragment is a mineral particle, derived from the parent material, > 2 mm in its equivalent diameter'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )      
class LayerArtefacts(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    abundance = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    black_carb = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_type1_set',  blank=True, null=True)
    type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_type2_set',  blank=True, null=True)
    type3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_type3_set',  blank=True, null=True)
    type4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_type4_set',  blank=True, null=True)
    type5 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_type5_set',  blank=True, null=True)
    size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_size1_set',  blank=True, null=True)
    size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_size2_set',  blank=True, null=True)
    size3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_size3_set',  blank=True, null=True)
    size4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_size4_set',  blank=True, null=True)
    size5 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerartefacts_size5_set',  blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance5 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_artefacts'
        db_table_comment = 'Artefacts are solid or liquid substances that are: created or substantially modified by humans as part of an industrial or artisanal manufacturing process, or brought to the surface by human activity from a depth, where they were not influenced by surface processes, and deposited in an environment, where they do not commonly occur.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )   

class LayerCracks(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    persistenc = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercracks_persistenc_set',  blank=True, null=True)
    continuity = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercracks_continuity_set',  blank=True, null=True)
    avg_width = models.DecimalField(max_digits=16, decimal_places=2, validators=[validate_positive], blank=True, null=True)
    abundance = models.PositiveIntegerField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_cracks'
        db_table_comment = 'Report persistence and continuity'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
   
class LayerMatrixColours(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    munsell_m1 = models.TextField(blank=True, null=True)
    munsell_d1 = models.TextField(blank=True, null=True)
    area1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    munsell_d2 = models.TextField(blank=True, null=True)
    area2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    munsell_d3 = models.TextField(blank=True, null=True)
    area3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_matrix_colours'
        db_table_comment = 'Report the colour of the soil matrix. If there is more than one matrix colour, report up to three, the dominant one first, and give the percentage of the exposed area'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerLithogenicVariegates(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier') 
    munsell_m1 = models.TextField(blank=True, null=True)
    size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerlithogenicvariegates_size1_set',  blank=True, null=True)
    area1 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerlithogenicvariegates_size2_set',  blank=True, null=True)
    area2 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    size3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerlithogenicvariegates_size3_set',  blank=True, null=True)
    area3 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_lithogenic_variegates'
        db_table_comment = 'Report colour, size class, and abundance. If more than one colour occurs, report up to three, the dominant one first, and give size class and abundance for each colour separately.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )        

class LayerRedoximorphic(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    oxi_inner = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    oxi_outer = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    oxi_random = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_inner = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_outer = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    red_random = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abund_oxi = models.DecimalField(max_digits=12, decimal_places=4, validators=[validate_percentage], db_comment='Abundance of cemented oximorphic features, by volume [%]', blank=True, null=True)
    clr1_munsell_m = models.TextField(blank=True, null=True)
    clr1_munsell_d = models.TextField(blank=True, null=True)
    clr1_substance = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_substance_set',   blank=True, null=True)
    clr1_location = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_location_set',  blank=True, null=True)
    clr1_size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_size1_set',  blank=True, null=True)
    clr1_size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_size2_set',  blank=True, null=True)
    clr1_mottles_c = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_mottles_c_set',  blank=True, null=True)
    clr1_mottles_b = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_mottles_b_set',  blank=True, null=True)
    clr1_cement = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr1_cement_set',  blank=True, null=True)
    clr1_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    clr2_munsell_m = models.TextField(blank=True, null=True)
    clr2_munsell_d = models.TextField(blank=True, null=True)
    clr2_substance = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_substance_set',   blank=True, null=True)
    clr2_location = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_location_set',  blank=True, null=True)
    clr2_size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_size1_set',  blank=True, null=True)
    clr2_size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_size2_set',  blank=True, null=True)
    clr2_mottles_c = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_mottles_c_set',  blank=True, null=True)
    clr2_mottles_b = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_mottles_b_set',  blank=True, null=True)
    clr2_cement = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr2_cement_set',  blank=True, null=True)
    clr2_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    clr3_munsell_m = models.TextField(blank=True, null=True)
    clr3_munsell_d = models.TextField(blank=True, null=True)
    clr3_substance = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_substance_set',   blank=True, null=True)
    clr3_location = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_location_set',  blank=True, null=True)
    clr3_size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_size1_set',  blank=True, null=True)
    clr3_size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_size2_set',  blank=True, null=True)
    clr3_mottles_c = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_mottles_c_set',  blank=True, null=True)
    clr3_mottles_b = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_mottles_b_set',  blank=True, null=True)
    clr3_cement = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerredoximorphic_clr3_cement_set',  blank=True, null=True)
    clr3_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_redoximorphic'
        db_table_comment = ''
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        ) 

class LayerCoatingsBridges(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    clay_coat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay coatings in percentage')
    form_coat = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoatingsbridges_form_coat_set',   blank=True, null=True, db_comment='refer to clay coatings')
    org_coat = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoatingsbridges_org_coat_set',   blank=True, null=True, db_comment='Organic matter coatings and oxide coatings on sand and/or coarse silt grains')
    crack_coat = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of cracked coatings in percentage')
    clay_bridg = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay bridges in percentage')
    form_bridg = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoatingsbridges_form_bridg_set',   blank=True, null=True, db_comment='refer to clay bridge')
    form_org = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercoatingsbridges_form_org_set',   blank=True, null=True, db_comment='refer to organic matter coatings and oxide coatings (report only if matrix colour value ≤ 3)')
    sand_silt = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of uncoated sand and coarse silt grains in percentage')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_coatings_bridges'
        db_table_comment = 'Report the abundance of clay coatings in % of the surfaces of soil aggregates, coarse fragments and/or biopore walls clay bridges between sand grains in % of involved sand grains.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
           
class LayerCarbonates(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    matr_c = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_matr_c_set',   blank=True, null=True)
    matr_c_ret = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_matr_c_ret_set',   blank=True, null=True)
    sec_type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_type1_set',   blank=True, null=True)
    sec_type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_type2_set',   blank=True, null=True)
    sec_type3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_type3_set',   blank=True, null=True)
    sec_type4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_type4_set',   blank=True, null=True)
    sec_size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_size1_set',   blank=True, null=True)
    sec_size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_size2_set',   blank=True, null=True)
    sec_size3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_size3_set',   blank=True, null=True)
    sec_size4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_size4_set',   blank=True, null=True)
    sec_shape1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_shape1_set',   blank=True, null=True)
    sec_shape2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_shape2_set',   blank=True, null=True)
    sec_shape3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_shape3_set',   blank=True, null=True)
    sec_shape4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layercarbonates_sec_shape4_set',   blank=True, null=True)
    sec_abund1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sec_abund4 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_carbonates'
        db_table_comment = 'Layer Carbonates'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerGypsum(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    content = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_content_set',  blank=True, null=True)
    sec_gypsum = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    sgypsum1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_sgypsum1_set',  blank=True, null=True)
    sgypsum2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_sgypsum2_set',  blank=True, null=True)
    type1_size = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_type1_size_set',   blank=True, null=True)
    type2_size = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_type2_size_set',   blank=True, null=True)
    type1_shape = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_type1_shape_set',   blank=True, null=True)
    type2_shape = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layergypsum_type2_shape_set',   blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_gypsum'
        db_table_comment = 'Report the gypsum content in the soil matrix. If readily soluble salts are absent or present in small amounts only, gypsum can be estimated by measuring the electrical conductivity in soil suspensions of different soil-water relations after 30 minutes (in the case of fine-grained gypsum). This method detects primary and secondary gypsum. Note: Higher gypsum contents may be differentiated by abundance of H2O-soluble pseudomycelia/crystals and a soil colour with high value and low chroma'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerSecondarySilica(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layersecondarysilica_type1_set',  blank=True, null=True, db_comment='Report the type of secondary silica, type1 is dominant')
    type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layersecondarysilica_type2_set',  blank=True, null=True, db_comment='Report the type of secondary silica')
    dnfcsize1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layersecondarysilica_dnfcsize1_set',  blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type1')
    dnfcsize2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layersecondarysilica_dnfcsize2_set',  blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type2')
    abund = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Report the total percentage (by exposed area) of secondary silica')
    abund_dnfc = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a cemented layer, report in addition the percentage (by volume) of those durinodes and remnants that have a diameter ≥ 1 cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_secondary_silica'
        db_table_comment = 'Secondary silica (SiO2) is off-white and predominantly consisting of opal and microcrystalline forms. It occurs as laminar caps, lenses, (partly) filled interstices, bridges between sand grains, and as coatings at surfaces of soil aggregates, biopore walls, coarse fragments, and remnants of broken-up cemented layers. Report the type of secondary silica. If more than one type occurs, report up to two, the dominant one first.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerConsistence(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    cement = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Report the percentage (by volume, related to the whole soil) of the layer that is cemented.')
    cement_ag1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_cement_ag1_set',  blank=True, null=True, db_comment='Report the cementing agents')
    cement_ag2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_cement_ag2_set',  blank=True, null=True)
    cement_ag3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_cement_ag3_set',  blank=True, null=True)
    cement_cls = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_cement_cls_set',  blank=True, null=True)
    rrclass_m = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_rrclass_m_set',  blank=True, null=True, db_comment='Rupture resistance, non-cemented soil moist')
    rrclass_d = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_rrclass_d_set',  blank=True, null=True, db_comment='Rupture resistance, non-cemented soil dry')
    susceptib = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_susceptib_set',  blank=True, null=True, db_comment='Some layers are prone to cementation after repeated drying and wetting. Report the susceptibility')
    m_failure = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_m_failure_set',  blank=True, null=True, db_comment='Report the manner of failure (brittleness)')
    plastic = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_plastic_set',  blank=True, null=True, db_comment='Plasticity is the degree to which reworked soil can be permanently deformed without rupturing')
    penet_res = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    stickiness = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerconsistence_stickiness_set',  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_consistence'
        db_table_comment = 'Consistence is the degree and kind of cohesion and adhesion that soil exhibits. Consistence is reported separately for cemented and non-cemented (parts of) layers. If a specimen of soil does not fall into pieces by applying low forces, one has to check, whether it is cemented'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerPermafrost(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    cry_alter1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerpermafrost_cry_alter1_set',  blank=True, null=True)
    cry_alter2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerpermafrost_cry_alter2_set',  blank=True, null=True)
    cry_alter3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerpermafrost_cry_alter3_set',  blank=True, null=True)
    permafrost = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerpermafrost_permafrost_set',  blank=True, null=True)
    cry_abund1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cry_abund2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    cry_abund3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_permafrost'
        db_table_comment = 'Estimate the total percentage (by exposed area, related to the whole soil) affected by cryogenic alteration. Report up to three features, the dominant one first, and report the percentage for each feature separately.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerOrganicCarbon(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    contentmin = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    contentmax = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    nat_accum1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerorganiccarbon_nat_accum1_set',  blank=True, null=True)
    nat_accum2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerorganiccarbon_nat_accum2_set',  blank=True, null=True)
    nat_accum3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerorganiccarbon_nat_accum3_set',  blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    black_carb = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_organic_carbon'
        db_table_comment = 'Report the estimated organic carbon content. It is based on the Munsell value, moist, and the texture'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )
 
class LayerRoots(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    a_lt2mm = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerroots_a_lt2mm_set',  blank=True, null=True, db_comment='diameter <= 2mm')
    a_lt05mm = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerroots_a_lt05mm_set',  blank=True, null=True, db_comment='diameter < 0,5mm')
    a_05to2mm = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerroots_a_05to2mm_set',  blank=True, null=True, db_comment='diameter from 0.5 to 2 mm')
    a_gt2mm = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerroots_a_gt2mm_set',  blank=True, null=True, db_comment='diameter > 2mm')
    a_2to5mm = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerroots_a_2to5mm_set',  blank=True, null=True, db_comment='diameter from 2 to 5 mm')
    a_gt5mm = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerroots_a_gt5mm_set',  blank=True, null=True, db_comment='diameter > 5mm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_roots'
        db_table_comment = 'Count the number of roots per dm2, separately for the six diameter classes, and report the abundance classes'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerAnimalActivity(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layeranimalactivity_type1_set',  blank=True, null=True)
    type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layeranimalactivity_type2_set',  blank=True, null=True)
    type3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layeranimalactivity_type3_set',  blank=True, null=True)
    type4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layeranimalactivity_type4_set',  blank=True, null=True)
    type5 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layeranimalactivity_type5_set',  blank=True, null=True)
    mammal = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    bird = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    worm = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    insect = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    unspecify = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_animal_activity'
        db_table_comment = 'Report the animal activity that has visibly changed the features of the layer. If applicable, report up to 5 types, the dominant one first. Report the percentage (by exposed area), separately for mammal activity, bird activity, worm activity, insect activity and unspecified activity'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerHumanAlterations(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    nat_mat1 =models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_nat_mat1_set',  blank=True, null=True)
    nat_mat2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_nat_mat2_set',  blank=True, null=True)
    nat_mat3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_nat_mat3_set',  blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    texture = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_texture_set',  blank=True, null=True)
    carbonate = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_carbonate_set',   blank=True, null=True)
    carbon = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    alter1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_alter1_set',   blank=True, null=True)
    alter2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_alter2_set',  blank=True, null=True)
    aggregate = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerhumanalterations_aggregate_set',  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_human_alterations'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerDegreeDecomposition(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    vis_plant = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, validators=[validate_percentage])
    sbdiv_horz = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerdegreedecomposition_sbdiv_horz_set',  blank=True, null=True)
    plant_res1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerdegreedecomposition_plant_res1_set',  blank=True, null=True)
    plant_res2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerdegreedecomposition_plant_res2_set',  blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_degree_decomposition'
        db_table_comment = 'Refer to the transformation of visible plant tissues into visibly homogeneous organic matter.'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerNonMatrixPore(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    type1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_type1_set',  blank=True, null=True)
    size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_size1_set',  blank=True, null=True)
    abund1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_abund1_set',  blank=True, null=True)
    type2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_type2_set',  blank=True, null=True)
    size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_size2_set',  blank=True, null=True)
    abund2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_abund2_set',  blank=True, null=True)
    type3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_type3_set',  blank=True, null=True)
    size3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_size3_set',  blank=True, null=True)
    abund3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_abund3_set',  blank=True, null=True)
    type4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_type4_set',  blank=True, null=True)
    size4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_size4_set',  blank=True, null=True)
    abund4 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layernonmatrixpore_abund4_set',  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_nonmatrix_pore'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class PointLayer(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')
    point = models.ForeignKey(PointGeneral, on_delete=models.CASCADE, related_name='pointlayer_point_set', db_comment='Foreign Key field: point') 
    horizon = models.TextField(db_comment='layer horizon designation', default='?', blank=True, null=True )
    number = models.SmallIntegerField(validators=[validate_positive], db_comment='layer order in point')
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm',blank=True, null=True)
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm',blank=True, null=True)
    lower_bound = models.TextField(db_comment='layer lower boundary ', blank=True, null=True )
    hom_part = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    hom_alluvt = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_hom_alluvt_set',  blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    wat_satur = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_wat_satur_set',  blank=True, null=True, db_comment='Types of water saturation')
    wat_status = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_wat_status_set',  blank=True, null=True, db_comment='Soil water status')
    o_mineral =  models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_o_mineral_set',  blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    bounddist = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_bounddist_set',  blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundshape = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_boundshape_set',  blank=True, null=True)
    wind = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_wind_set',  blank=True, null=True, db_comment='Wind deposition')
    tex_cls = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_tex_cls_set',  blank=True, null=True, db_comment='Texture class') 
    tex_subcls = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_tex_subcls_set',  blank=True, null=True, db_comment='Texture subclass')
    struct_w_s = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Structure Wedge-shaped aggregates tilted between ≥ 10° and ≤ 60° from the horizontal: abundance, by volume [%]')
    rh_value = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_rh_value_set',  blank=True, null=True, db_comment='Rh Value')
    weathering = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Initial weathering abundance')
    sol_salts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    saline_eff_cont = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Saline efflorescence Continuity')
    ph_value = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    ph_solution = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_ph_solution_set',  blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    fracts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    avg_fracts = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    volc_abund = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_volc_abund_set',  blank=True, null=True)
    volc_thnaf = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_volc_thnaf_set',  blank=True, null=True)
    bulk_dens = models.DecimalField( max_digits=30, decimal_places=10, blank=True, null=True)
    pack_dens = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_pack_dens_set',  blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_mat = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_parent_mat_set',  blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    coars_text = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by coarser-textured parts of any orientation (vertical, horizontal, inclined) having a width of ≥ 0.5 cm')
    coars_text_v_tongues = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by continuous vertical tongues of coarser-textured parts with a horizontal extension of ≥ 1 cm (if these tongues are absent, report 0%)')
    coars_text_depth = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='the depth range in cm, where these tongues cover ≥ 10% of the exposed area (if they extend across several layers, the length is only reported in the description of that layer, where they start at the layer’s upper limit).')
    coars_text_h_area = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='In the middle of the layer, prepare a horizontal surface, 50 cm x 50 cm, and report the percentage (by horizontal area covered) of the coarser-textured parts.')
    stress_fts_pressfaces = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Pressure faces in % of the surfaces of soil aggregates')
    stress_fts_slicksides = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True, db_comment='Slickensides in % of the surfaces of soil aggregates.')
    ribbonl_acc_substances = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_ribbonl_acc_substances_set', blank=True, null=True)
    ribbonl_acc_number = models.IntegerField(blank=True, null=True)
    ribbonl_acc_comb_thick = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If there are 2 or more ribbon-like accumulations in one layer, report the number of the accumulations and their combined thickness in cm')
    sur_crusts_sealing1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_sur_crusts_sealing1_set', blank=True, null=True)
    sur_crusts_sealing2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_sur_crusts_sealing2_set', blank=True, null=True)
    sur_crusts_sealing3 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='pointLayer_sur_crusts_sealing3_set', blank=True, null=True)
    sur_crusts_avg_thickn = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    layerremnants = models.OneToOneField(LayerRemnants, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Remnants of broken-up cemented layers')
    layercoarsefragments = models.OneToOneField(LayerCoarseFragments, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Coarse fragments')
    layerartefacts = models.OneToOneField(LayerArtefacts, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Artefacts')
    layercracks = models.OneToOneField(LayerCracks, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Cracks')
    layercoatingsbridges = models.OneToOneField(LayerCoatingsBridges, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerCoatingsBridges')
    layercarbonates = models.OneToOneField(LayerCarbonates, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Section Layer Carbonates')
    layergypsum = models.OneToOneField(LayerGypsum, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerGypsum')
    layersecondarysilica = models.OneToOneField(LayerSecondarySilica, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerSecondarySilica')
    layerconsistence = models.OneToOneField(LayerConsistence, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerConsistence')
    layerpermafrost =  models.OneToOneField(LayerPermafrost, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerPermafrostFeatures')   
    layerorganiccarbon =  models.OneToOneField(LayerOrganicCarbon, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerOrganicCarbon')   
    layerroots =  models.OneToOneField(LayerRoots, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRoots')   
    layeranimalactivity  =  models.OneToOneField(LayerAnimalActivity, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerAnimalActivity')   
    layerhumanalterations =  models.OneToOneField(LayerHumanAlterations, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerHumanAlterations')   
    layerdegreedecomposition =  models.OneToOneField(LayerDegreeDecomposition, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerDegreeDecomposition')   
    layernonmatrixpore = models.OneToOneField(LayerNonMatrixPore, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerNonMatrixPore')   
    layermatrixcolours = models.OneToOneField(LayerMatrixColours, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Matrix colour')   
    layerlithogenicvariegates = models.OneToOneField(LayerLithogenicVariegates, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerLithogenicVariegates')
    layerredoximorphic = models.OneToOneField(LayerRedoximorphic, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='LayerRedoximorphicFeatures')
    
    labdata =  models.OneToOneField(LabData, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True, db_comment='Layer Laboratory data')
    
    ## layerstructure_layer_set LayerStructure

    def _get_thickness(self):
        if self.lower and self.upper: 
            return self.lower - self.upper
        else: return None
    thickness = property(_get_thickness)   
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'point_layer'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

class LayerStructure(models.Model):
    id = models.TextField(primary_key=True, db_comment='identifier')  
    layer = models.ForeignKey(PointLayer, on_delete=models.CASCADE, related_name='layerstructure_layer_set', db_comment='point Layer' )
    level = models.ForeignKey(TaxonomyValue, on_delete=models.RESTRICT, related_name='layerstructure_level_set' )
    type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerstructure_type_set',  blank=True, null=True)
    grade = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerstructure_grade_set',  blank=True, null=True)
    penetrab = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerstructure_penetrab_set',  blank=True, null=True)
    size1 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerstructure_size1_set',  blank=True, null=True)
    size2 = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='layerstructure_size2_set',  blank=True, null=True)
    abundance_vol = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance1 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField( max_digits=30, decimal_places=10, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_structure'
        unique_together = (('layer', 'level'),)
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

###########################
# REQUEST
###########################

    
class Request(models.Model):
    creation = models.DateField( db_comment='Creation date')
    who_id = models.TextField( db_comment='Identifier of the User')
    who_name = models.TextField( db_comment='Name of the User')
    who_email = models.TextField( db_comment='Email of the User')
    what_interpolation = models.BooleanField(blank=True, null=True, db_comment='Requested Interpolation')
    what_measure = models.TextField( db_comment='Data measure: CHOICE!!!!! ', blank=True, null=True)
    what_section = models.TextField( db_comment='Data section: CHOICE!!!!! ', blank=True, null=True)
    why = models.TextField( db_comment='Purpose')
    where = models.JSONField( db_comment='AOI in geoJSON format') 
    where_anchor = models.JSONField( db_comment='AOI anchor in geoJSON format') 
    when_from = models.DateField( db_comment='Period start', blank=True, null=True)
    when_to = models.DateField( db_comment='Period End', blank=True, null=True)
    status = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='request_status_set',  db_comment='status of Request', blank=True, null=True)
    mgr_id = models.TextField( db_comment='SIS Staff member - Id', blank=True, null=True)
    mgr_name = models.TextField( db_comment='SIS Staff member - Name', blank=True, null=True)
    mgr_email = models.TextField( db_comment='SIS Staff member - Email', blank=True, null=True)
    mgr_msg  = models.TextField( db_comment='Message to the user by SIS staff', blank=True, null=True)
    variogram = models.JSONField( db_comment='Variogram - interpolation preliminary result if done and what_interpolation is true', blank=True, null=True) 
    points = models.JSONField( db_comment='Points - Filtered data result, can be empty', blank=True, null=True) 
    parameters = models.JSONField( db_comment='interpolation parameters', blank=True, null=True)
    raster = models.TextField( db_comment='Geonode Id of the raster', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'requests'
        permissions = (
            ('access', 'Can access backoffice data'),
            ('view', 'Can view backoffice data'),
            ('write', 'Can write backoffice data'),
        )

###########################
# LabDataExtraMeasureData
###########################

class LabDataExtraMeasure(models.Model):
    id = models.BigAutoField(primary_key=True)
    measure = models.ForeignKey(TaxonomyValue, on_delete=models.CASCADE, related_name='labdataextrameasure_measure_set' )
    method = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdataextrameasure_method_set',  blank=True, null=True)
    unit = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='labdataextrameasure_unit_set',  blank=True, null=True)
    labdata = models.ForeignKey(LabData, on_delete=models.CASCADE, related_name='labdataextrameasure_labdata_set')
    value = models.DecimalField( max_digits=30, decimal_places=10, db_comment='numeric value of measure', blank=True, null=True )
    value_text = models.TextField( db_comment='textual value of measure', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'labdata_extra_measure'
        db_table_comment = 'Laboratory data extra measures'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )

###########################
# Photos
###########################

class Photo(models.Model):
    id = models.TextField(primary_key=True, db_comment='Geonode document identifier (number)', serialize=False)
    title = models.TextField(db_comment='Photo title')
    caption = models.TextField(blank=True, null=True, db_comment='Description')
    point = models.ForeignKey(PointGeneral, on_delete=models.CASCADE, related_name='photo_point_set', db_comment='Point soil data identifier') 
    type = models.ForeignKey(TaxonomyValue, on_delete=models.SET_NULL, related_name='photo_type_set',  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'photos'
        db_table_comment = 'photos descriptor'
        permissions = (
            ('view', 'can view data'),
            ('write', 'can write data'),
        )


###########################
# Cron Jobs
###########################
class CronJob(models.Model):
    type = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='job_type_set', db_comment='update/interpolate') 
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='job_request_set', db_comment=' id della richiesta ....ci sono i parametri', blank=True, null=True) 
    status = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='job_status_set', db_comment='status del job') 
    date = models.DateTimeField( db_comment='Date of the insertion')
    log = models.TextField( db_comment='last message ....usare api per scrivere se no prevedo casini', null=True, blank=True)
    
    objects = models.Manager().using('backoffice')
    class Meta:
        managed = True
        db_table = 'cron_jobs'
        db_table_comment = 'Cron jobs '
        permissions = (
            ('view', 'can view data'),
            ('add', 'can add data'),
            ('change', 'can change data'),
            ('delete', 'can delete data'),
        )
