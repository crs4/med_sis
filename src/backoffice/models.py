from django.db import models
from django.contrib.gis.db import models as gis_models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


""" class ValidationErrorCollector:
    def __init__(self):
        self.errors = {}

    def add_error(self, field, error):
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(error)

    def raise_errors(self):
        if self.errors:
            raise ValidationError(self.errors) """


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

####
## related_name = lowercase( %Model + '_' + %fieldname + '_set' ) 
##
###########################
## Uilities 
###########################
class Taxonomy(models.Model):
    id = models.TextField(primary_key=True, db_comment='category code')
    criterion = models.TextField(db_comment='category description')
    super = models.TextField(db_comment='super category name', blank=True, null=True)
     
    def _get_code(self):
        "Returns the category code"
        x = id.split('.')
        return x[1]

    def _get_taxonomy(self):
        "Returns the category code"
        x = id.split('.')
        return x[0]    
    
    code = property(_get_code) 
    taxonomy = property(_get_taxonomy) 
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'taxonomy'
        db_table_comment = 'SOILS4MED Taxonomies and  WRB2022 Taxonomies'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )


###########################
## XLSx Uploads
###########################
class XLSxUpload(models.Model):

    UPLOAD_RESULTS = [
        ("UPLOADED" , "UPLOADED"),
        ("IMPORT_SUCCESS" , "IMPORT_SUCCESS"),
        ("IMPORT_WITH_ERROR" , "IMPORT_WITH_ERROR"),
        ("CRITICAL_ERROR" , "CRITICAL_ERROR"),
    ]
    type = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='xlsx_upload_type', db_comment='Type of the upload')
    title = models.TextField(db_comment='sheet name')
    report = models.JSONField( db_comment='Report of the upload')
    data = models.JSONField( db_comment='Data uploaded')
    editor = models.TextField( db_comment='Owner of the upload', null=True, blank=True)
    date = models.DateTimeField( db_comment='Date of the upload')
    status = models.TextField( choices=UPLOAD_RESULTS, db_comment='Status of the upload' )
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'xlsx_upload'
        db_table_comment = 'XLSx Data Uploads'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class XSLxSheetConf(models.Model):
    type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='xlsxsheetconf_type_set', blank=True, null=True)
    name = models.TextField(db_comment='sheet name')
    size = models.IntegerField(db_comment='Sheet columns number')
    first = models.IntegerField( db_comment='Sheet columns first data row')
    note = models.TextField(db_comment='Sheet description')

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        ordering = ['type','name']
        unique_together = (('type', 'name'),)
        db_table = 'xlsx_sheet'
        db_table_comment = 'table with xlsx sheet description'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class XSLxMapping(models.Model):
    type = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='xlsx_mapping_type')
    sheet = models.TextField(db_comment='sheet name')
    col = models.IntegerField(db_comment='Sheet column order')
    model = models.TextField(db_comment='target class model')
    field = models.TextField(db_comment='target field in the target class model')
    taxonomy = models.TextField(blank=True, null=True, db_comment='taxonomy name')
    note = models.TextField(blank=True, null=True, db_comment='field description')
    field_level = models.TextField(blank=True, null=True, db_comment='upper level field name in the target model')
    value_level = models.IntegerField(blank=True, null=True, db_comment='value for the upper level field')
    paragraph = models.TextField(blank=True, null=True, db_comment='WRB Annex 4 paragraph ')
    section = models.TextField(blank=True, null=True, db_comment='Input Section')
    fcheck = models.TextField(blank=False, null=False, db_comment='Value check and type')
    
    objects = models.Manager().using('backoffice')
    class Meta:
        managed = True
        ordering = ['type','sheet','col']
        unique_together = (('type', 'sheet','col'),)
        db_table = 'xlsx_mapping'
        db_table_comment = 'table with the mapping between xlsx sheets and django models'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

###########################
# Profile\Samples Genealogy
###########################

class Project(models.Model):
    id = models.TextField(primary_key=True, db_comment='Project identifier ')
    title = models.TextField(blank=True, null=True, db_comment='project name')
    descr = models.TextField(blank=True, null=True, db_comment='project description')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'project'
        db_table_comment = 'projects descriptor'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class Genealogy(models.Model):
    old_code = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True, db_comment='note about owner ')
    refer = models.TextField(blank=True, null=True, db_comment='reference')
    pub_year = models.IntegerField(blank=True, null=True, db_comment='year of pubblication')
    web_link = models.TextField(blank=True, null=True)
    avail = models.TextField(blank=True, null=True, db_comment='Data availability and/or use restrictions')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'profile_genealogy'
        db_table_comment = 'genealogy of profile data' 
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

###########################
# Profile General
###########################
class LandformTopography(models.Model):
    grad_ups = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface upslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    grad_downs = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface downslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    slope_asp = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_positive], blank=True, null=True, db_comment='If the profile lies on a slope, report the compass direction that the slope faces, viewed downslope; e.g., 225°')
    slope_shp = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landformtopography_slope_shape_set', blank=True, null=True, db_comment='If the profile lies on a slope, report the slope shape in 2 directions: up-/downslope (perpendicular to the elevation contour, i.e. the vertical curvature) and across slope (along the elevation contour, i.e. the horizontal curvature); e.g., Linear (L), Convex (V) or Concave (C).')
    position = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landformtopography_position_set', blank=True, null=True, db_comment='If the profile lies in an uneven terrain, report the profile position.')
    landform1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landformtopography_landform1_set', blank=True, null=True)
    landform2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landformtopography_landform2_set', blank=True, null=True)
    activity1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landformtopography_activity1_set', blank=True, null=True)
    activity2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landformtopography_activity2_set', blank=True, null=True)
    geo_descr = models.TextField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'landform_topography'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class CoarseFragments(models.Model):
    total_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    class1size = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='coarsefragments_class1size_set', blank=True, null=True)
    class2size = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='coarsefragments_class2size_set',  blank=True, null=True)
    class3size = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='coarsefragments_class3size_set',  blank=True, null=True)
    class1area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    class2area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    class3area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'coarse_fragments'
        db_table_comment = 'Report the total percentage of the area that is covered by coarse surface fragments. In addition, report at least one and up to three size classes and report the percentage of the area that is covered by the coarse surface fragments of the respective size class, the dominant one first.\r\nClasses size are in p_coarse_size'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
    """
    def clean(self):
        if self.class1_size is not None and self.class1_size.startswith("p_coarse_size."):
                raise ValidationError({'class1_size': ('Wrong classification.')})
        if self.class2_size is not None and self.class2_size.startswith("p_coarse_size."):
                raise ValidationError({'class2_size': ('Wrong classification.')})
        if self.class3_size is not None and self.class3_size.startswith("p_coarse_size."):
                raise ValidationError({'class3_size': ('Wrong classification.')})
    """

class ClimateAndWeather(models.Model):
    clim_koppen = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_clim_koppen_set', blank=True, null=True)
    eco_shultz = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_eco_shultz_set', blank=True, null=True)
    season = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_season_set', blank=True, null=True)
    curr_weath = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_curr_weath_set', blank=True, null=True)
    past_weath = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_past_weath_set', blank=True, null=True)
    soil_temp = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_soil_temp_set', blank=True, null=True)
    soil_moist = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='climateandweather_soil_moist_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'climate_weather'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class Cultivated(models.Model):
    type = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='cultivated_type_set', blank=True, null=True, db_comment='value from p_cultivation_type ')
    actual1 = models.TextField(blank=True, null=True, db_comment='actual dominant specie')
    actual2 = models.TextField(blank=True, null=True, db_comment='actual second specie')
    actual3 = models.TextField(blank=True, null=True, db_comment='actual third specie')
    cessation = models.DateField(blank=True, null=True, db_comment='editable if last dominant specie is NOT NULL')
    area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    prod1_tech = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='cultivated_prod1_tech_set', blank=True, null=True, db_comment='Report the techniques that refer to the surrounding area of the soil profile. If more than one type of technique is present, report in the array up to three, the dominant one first. Value from p_productivity_techniques')
    prod2_tech = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='cultivated_prod2_tech_set', blank=True, null=True)
    prod3_tech = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='cultivated_prod3_tech_set', blank=True, null=True)
    last1 = models.TextField(blank=True, null=True, db_comment="last dominant specie, editable if actual_species1 is NULL")
    last2 = models.TextField(blank=True, null=True, db_comment="Second last specie, editable if actual_species2 is NULL ")
    last3 = models.TextField(blank=True, null=True, db_comment="Third last specie, editable if actual_species3 is NULL ")
    rotation1 = models.TextField(blank=True, null=True, db_comment='Report the dominant specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the most frequent)')
    rotation2 = models.TextField(blank=True, null=True, db_comment='Report the second specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    rotation3 = models.TextField(blank=True, null=True, db_comment='Report the third specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'cultivated'
        db_table_comment = 'Report up to three actual cultivated species (in the array "actual_species") using the scientific name. If currently under fallow, report the up to 3 last species (in the array "last_species") and indicate month and year of harvest or of cultivation cessation. Insert the species in the sequence of the area covered starting with the species that covers the largest area. Report the up to 3 species that have been cultivated in the last five years in rotation with the actual or last species (1 is the most frequent) in the array column "rotational_species"'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
    """
    def clean(self):
        if self.cultivation_cessation is not None and (self.last_species1 is None or self.actual_species1 is not None):
            raise ValidationError({'cultivation_cessation': ('cultivation_cessation error no dominant last specie present or actual dominant specie.')})
        if self.last_species1 is not None and (self.cultivation_cessation is None or self.actual_species1 is not None):
            raise ValidationError({'last_species1': ('last_species1 error no cultivation_cessation or actual specie present.')})
        if self.last_species2 is not None and (self.last_species1 is None or self.actual_species2 is not None):
            raise ValidationError({'last_species2': ('last_species2 error no dominant last specie or second actual specie present.')})
        if self.last_species3 is not None and (self.last_species2 is None or self.actual_species3 is not None):
            raise ValidationError({'last_species3': ('last_species3 error no second last specie or third actual specie present.')})
        if self.cultivation_type is not None and self.cultivation_type.startswith("p_cultivation_type."):
            raise ValidationError({'cultivation_type': ('Wrong classification.')})
        if self.spec_prod_tech1 is not None and self.spec_prod_tech1.startswith("p_productivity_techniques."):
            raise ValidationError({'spec_prod_tech1': ('Wrong classification.')})
        if self.spec_prod_tech2 is not None and self.spec_prod_tech2.startswith("p_productivity_techniques."):
            raise ValidationError({'spec_prod_tech2': ('Wrong classification.')})
        if self.spec_prod_tech3 is not None and self.spec_prod_tech3.startswith("p_productivity_techniques."):
            raise ValidationError({'spec_prod_tech3': ('Wrong classification.')})

    """ 

class LandUse(models.Model):
    land_use = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landuse_land_use_set', blank=True, null=True)
    corine = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='landuse_corine_set', blank=True, null=True)
    cultivated =  models.OneToOneField(Cultivated, on_delete=models.SET_DEFAULT, default=None, db_comment='Cultivated Land')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'land_use'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
    """
    def clean(self):
        if self.land_use is not None and self.land_use.startswith("p_land_use."):
            raise ValidationError({'land_use': ('Wrong classification.')})
        if self.corine is not None and self.corine.startswith("p_corine."):              
            raise ValidationError({'Corine': ('Wrong classification.')})
    """        

class NotCultivated(models.Model):
    LEVEL_TYPES = [
        ("Upper-stratum" , "Upper-stratum"),
        ("Mid-stratum" , "Mid-stratum"),
        ("Ground-stratum" , "Ground-stratum"),
    ]
    
    
    landuse = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='notcultivated_landuse_set')
    veget1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='notcultivated_veget1_set', blank=True, null=True)
    veget2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='notcultivated_veget2_set', blank=True, null=True)
    veget3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='notcultivated_veget3_set', blank=True, null=True)
    stratum = models.TextField(blank=True, null=True)
    avg_height = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    max_height = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    species1 = models.TextField(blank=True, null=True)
    species2 = models.TextField(blank=True, null=True)
    species3 = models.TextField(blank=True, null=True)

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'not_cultivated'
        unique_together = (('stratum', 'landuse'),)
        db_table_comment = 'For each profile, compile as many rows as the vegetation strata (STRATA_TYPES) are. Report the average height and the maximum height in m above ground for each stratum separately. Report the vegetation cover. For the upper stratum and the mid-stratum, report the percentage (by area) of the crown cover. For the ground stratum, report the percentage (by area) of the ground cover. Report up to three important species per stratum, e.g., Fagus orientalis. If you do not know the species, report the next higher taxonomic rank. The (maximum 3) species must be insert in the array column species.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """        
    def clean(self):
        # Ensures constraint on model level, raises ValidationError
            if self.species2 is not None and self.species1 is None :
                raise ValidationError({'species2': ('species2 error no dominant specie present.')})
            if self.species3 is not None and ( self.species2 is None or self.species1 is None ) :
                raise ValidationError({'species3': ('species3 error no dominant or second specie present.')})
            if self.dominant_vegetation_type is not None and self.dominant_vegetation_type.startswith("p_vegetation_type."):
                    raise ValidationError({'dominant_vegetation_type': ('Wrong classification.')})
            if self.second_vegetation_type is not None and self.second_vegetation_type.startswith("p_vegetation_type."):
                    raise ValidationError({'second_vegetation_type': ('Wrong classification.')})
            if self.third_vegetation_type is not None and self.third_vegetation_type.startswith("p_vegetation_type."):
                    raise ValidationError({'third_vegetation_type': ('Wrong classification.')})
    """

class Surface(models.Model):
    crust_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    ground_form = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surface_ground_form_set', blank=True, null=True, db_comment='Patterned ground form field')
    tech_alter = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surface_tech_alteration_set', blank=True, null=True)
    bedr_form = models.TextField(blank=True, null=True)
    bedr_lith = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    outc_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    outc_dist = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    outc_size = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    ground_wat = models.DecimalField(max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    wat_above = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='surface_water_above_set', blank=True, null=True)
    wat_drain = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='surface_water_drain_set', blank=True, null=True)
    wat_repell = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='surface_water_repellence_set', blank=True, null=True)
    desert_ven = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    desert_var = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'surface'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class SurfaceCracks(models.Model):
    width1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfacecracks_width1_set', blank=True, null=True)
    dist1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfacecracks_dist1_set', blank=True, null=True)
    spat_arr1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='surfacecracks_spat_arr1_set', blank=True, null=True)
    persist1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfacecracks_persist1_set', blank=True, null=True)
    width2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfacecracks_width2_set', blank=True, null=True)
    dist2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfacecracks_dist2_set', blank=True, null=True)
    spat_arr2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='surfacecracks_spat_arr2_set', blank=True, null=True)
    persist2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfacecracks_persist2_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'surface_cracks'
        db_table_comment = 'For each profile, compile as many rows as the width classes are. If surface cracks are present, report the average width of the cracks. If the soil surface between cracks of larger width classes is regularly divided by cracks of smaller width classes, report the two width classes.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """"
    def clean(self):
        # Ensures constraint on model level, raises ValidationError
        if self.dominant_width_class is not None and self.dominant_width_class.startswith("p_surface_cracks_width."):
                raise ValidationError({'width_class': ('Wrong classification.')})
        if self.dominant_distance_between_cracks is not None and self.dominant_distance_between_cracks.startswith("p_surface_cracks_distance."):
                raise ValidationError({'distance_between_cracks': ('Wrong classification.')})
        if self.dominant_spatial_arrangement is not None and self.dominant_spatial_arrangement.startswith("p_surface_cracks_arrangement."):
                raise ValidationError({'spatial_arrangement': ('Wrong classification.')})
        if self.dominant_persistence is not None and self.dominant_persistence.startswith("p_surface_cracks_persistence."):
                raise ValidationError({'persistence': ('Wrong classification.')})
        if self.secondary_width_class is not None and self.secondary_width_class.startswith("p_surface_cracks_width."):
                raise ValidationError({'width_class': ('Wrong classification.')})
        if self.secondary_distance_between_cracks is not None and self.secondary_distance_between_cracks.startswith("p_surface_cracks_distance."):
                raise ValidationError({'distance_between_cracks': ('Wrong classification.')})
        if self.secondary_spatial_arrangement is not None and self.secondary_spatial_arrangement.startswith("p_surface_cracks_arrangement."):
                raise ValidationError({'spatial_arrangement': ('Wrong classification.')})
        if self.secondary_persistence is not None and self.secondary_persistence.startswith("p_surface_cracks_persistence."):
                raise ValidationError({'persistence': ('Wrong classification.')})
    """

class LitterLayer(models.Model):
    avg_thick = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    area = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    max_thick = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'litter_layer'
        db_table_comment = 'Observe an area of 5 m x 5 m with the profile at its centre. Report the average and the maximum thickness of the litter layer in cm. If there is no litter layer, report 0 cm as thickness.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )  

class SurfaceUnevenness(models.Model):
    position = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_position_set', blank=True, null=True)
    nat_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_nat_type_set', blank=True, null=True)
    nat_avg_h = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_elev = models.DecimalField( max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    nat_dist = models.DecimalField(max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    hum_type1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_hum_type1_set', blank=True, null=True)
    hum_type2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_hum_type2_set', blank=True, null=True)
    hum_ter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_h = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_w = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    hum_noter_d = models.DecimalField( max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    ero_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    ero_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_erosion_type_set', blank=True, null=True)
    ero_degree = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_erosion_degree_set', blank=True, null=True)
    ero_activ = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='surfaceunevenness_erosion_activity_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'surface_unevenness'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        ) 
    """        
    def clean(self):
        if self.position is not None and self.position.startswith("p_surface_unevenness_profile_position."):
            raise ValidationError({'position': ('Wrong classification.')}) 
        if self.natural_type is not None and self.natural_type.startswith("p_surface_unevenness_natural_type."):
            raise ValidationError({'natural_type': ('Wrong classification.')})
        if self.human_made_type_1 is not None and self.human_made_type_1.startswith("p_surface_unevenness_human_made_type."):
            raise ValidationError({'human_made_type_1': ('Wrong classification.')})
        if self.human_made_type_2 is not None and self.human_made_type_2.startswith("p_surface_unevenness_human_made_type."):
            raise ValidationError({'human_made_type_2': ('Wrong classification.')})
        if self.erosion_type is not None and self.erosion_type.startswith("p_surface_unevenness_erosion_type."):
             raise ValidationError({'type': ('Wrong classification.')})
        if self.erosion_degree is not None and self.erosion_degree.startswith("p_surface_unevenness_erosion_degree."):
            raise ValidationError({'degree': ('Wrong classification.')})
        if self.erosion_activity is not None and self.erosion_activity.startswith("p_surface_unevenness_erosion_activity."):
            raise ValidationError({'activity': ('Wrong classification.')})                 
    """


    """     
    def clean(self):
        error_collector = ValidationErrorCollector()
        
        # Validazione dei campi numerici
        for field_name in ['surface_crusts_area', 'outcrops_area_covered', 'desert_ventifacts', 'desert_varnish']:
            value = getattr(self, field_name)
            if value is not None:
                try:
                    validate_percentage(value)
                except ValidationError as e:
                    error_collector.add_error(field_name, e)
        
        # Validazione del campo ground_water_depth
        if self.ground_water_depth is not None:
            try:
                validate_positive(self.ground_water_depth)
            except ValidationError as e:
                error_collector.add_error('ground_water_depth', e)
        
        # Validazione dei campi ForeignKey
        taxonomy_validations = {
            'patterned_ground_form': 'p_patterned_ground_form.',
            'technical_surface_alteration': 'p_technical_surface_alteration.',
            'bedrock_lithology': 'l_p_parent_material.',
            'water_above_surface': 'p_water_above_surface.',
            'water_drainage_condition': 'p_drainage_condition.',
            'water_repellence_type': 'p_water_repellence.'
        }
        
        for field_name, prefix in taxonomy_validations.items():
            value = getattr(self, field_name)
            if value is not None and str(value).startswith(prefix):
                error_collector.add_error(field_name, ValidationError(_('Wrong classification.')))
        
        error_collector.raise_errors() 
    """

class ProfileGeneral(models.Model):
    code = models.TextField(primary_key=True, db_comment='profile identifier')
    date = models.DateField(db_comment='date of the description')
    surveyors = models.TextField(blank=True, null=True, db_comment='surveyors names comma separated')
    location = models.TextField(blank=True, null=True, db_comment='Name of the profile location')
    lat_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Latitude in decimal degree')
    lon_wgs84 = models.DecimalField(max_digits=14, decimal_places=8, db_comment='WGS84 Longitude in decimal degree')
    gps = models.BooleanField(blank=True, null=True, db_comment='is a gps acquisition?')
    elev_m_asl = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude above the sea level in meter')
    elev_dem = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Altitude in meters retrived from a dem in meter')
    survey_m = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profilegeneral_survey_method_set',  blank=True, null=True, db_comment='The code of the survey method')
    notes = models.TextField(blank=True, null=True)

    horizons = models.TextField(blank=True, null=True, db_comment='Horizons sequence of the profile')
    old_cls = models.TextField(blank=True, null=True, db_comment='Old classification of the profile location')
    new_cls = models.TextField(blank=True, null=True, db_comment='New classification of the profile location')
    cls_sys = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilegeenral_cls_sys_set', blank=True, null=True, db_comment='value from p_classification_system ')
    project = models.ForeignKey(Project, models.SET_NULL, blank=True, null=True, related_name='profilegeneral_project_set', db_comment='Survey/Project identifier')
    
    coarsefragments =  models.OneToOneField(CoarseFragments, on_delete=models.SET_DEFAULT, default=None, db_comment='Coarse Fragments')
    litterlayer =  models.OneToOneField(LitterLayer, on_delete=models.SET_DEFAULT, default=None, db_comment='Litter Layer')
    landuse =  models.OneToOneField(LandUse, on_delete=models.SET_DEFAULT, default=None, db_comment='Land Use ')
    surface =  models.OneToOneField(Surface, on_delete=models.SET_DEFAULT, default=None, db_comment='Surface ')
    surfacecracks =  models.OneToOneField(SurfaceCracks, on_delete=models.SET_DEFAULT, default=None, db_comment='Surface cracks')
    landformtopography = models.OneToOneField(LandformTopography, on_delete=models.SET_DEFAULT, default=None, db_comment='landform_topography')
    climateandweather = models.OneToOneField(ClimateAndWeather, on_delete=models.SET_DEFAULT, default=None, db_comment='Climate weather')
    genealogy =  models.OneToOneField(Genealogy, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Genealogy')
    surfaceUnevenness =  models.OneToOneField(SurfaceUnevenness, on_delete=models.SET_DEFAULT, default=None, db_comment='Surface Unevenness')
    
    ## profilelayer_profile_set ProfileLayer

    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'profile_general'
        db_table_comment = 'The Soil Profile main table'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

#########################################
## Lab Data 
#########################################
class LabData(models.Model):
    gravel = models.DecimalField(max_digits=40, decimal_places=6, validators=[validate_percentage],  db_comment='Gravel content (%)' , blank=True, null=True)
    cls_sys =  models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='labdata_cls_sys_set', db_comment='Classification system used for texture of fine earth', blank=True, null=True)
    texture = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='labdata_texture_set', db_comment='texture class', blank=True, null=True)      
    sand = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Sand  (percentage of the fine earth)', blank=True, null=True)
    v_c_sand = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Very coarse sand (percentage of the fine earth)', blank=True, null=True)
    c_sand = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Coarse sand (percentage of the fine earth)', blank=True, null=True)
    m_sand = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Medium sand (percentage of the fine earth)', blank=True, null=True)
    f_sand = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage],db_comment='Fine sand (percentage of the fine earth)', blank=True, null=True)
    v_f_sand  = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Very Fine sand (percentage of the fine earth)', blank=True, null=True)
    met_sand = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  db_comment='Method used for sand content', related_name='labdata_met_sand_set', blank=True, null=True)
    silt = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Silt (percentage of the fine earth)', blank=True, null=True)
    c_silt = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Coarse silt (percentage of the fine earth)', blank=True, null=True)
    f_silt = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_percentage], db_comment='Fine silt  (percentage of the fine earth)', blank=True, null=True)
    met_silt = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for silt content', related_name='labdata_met_silt_set', blank=True, null=True)
    clay = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Clay  (percentage of the fine earth)', blank=True, null=True)
    met_clay = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for clay content', related_name='labdata_met_clay_set', blank=True, null=True)
    bulk_dens = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Bulk density (g/cm3)'	, blank=True, null=True)
    el_cond = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Electric conductivity (dS/m)', blank=True, null=True)
    met_el_cond = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Electric conductivity', related_name='labdata_met_el_cond_set', blank=True, null=True)
    hy_cond = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Hydraulic conductivity at saturation (mm/h)', blank=True, null=True)
    met_hy_cond = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Hydraulic conductivity at saturation', related_name='labdata_met_hy_cond_set', blank=True, null=True)
    satur = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Saturation (percentage)', blank=True, null=True)
    field_cap = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Field capacity (percentage)', blank=True, null=True)
    wilting_p = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Wilting point (percentage)', blank=True, null=True)
    met_s_f_w = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for saturation, field capacity, wilting point', related_name='labdata_met_s_f_w_set', blank=True, null=True)
    acidity = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Soil acidity: Exchangeable Al (meq/100g)', blank=True, null=True)
    met_acidity = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,db_comment='Method used for Soil acidity: Exchangeable Al (meq/100g)',  related_name='labdata_met_acidity_set', blank=True, null=True)
    ph_h2o = models.DecimalField(max_digits=30, decimal_places=10, db_comment='pH (H2O)', blank=True, null=True)
    met_ph_h20 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for pH (H2O)', related_name='labdata_met_ph_h20_set', blank=True, null=True)
    ph_kcl = models.DecimalField(max_digits=30, decimal_places=10, db_comment='pH (KCl)', blank=True, null=True)
    met_ph_kcl = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for pH (KCl)', related_name='labdata_met_ph_xcl_set', blank=True, null=True)
    ph_ccl = models.DecimalField(max_digits=30, decimal_places=10, db_comment='pH (CaCl2)', blank=True, null=True)
    met_ph_ccl = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for pH (CaCl2)', related_name='labdata_met_ph_ccl_set', blank=True, null=True)
    org_car = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Organic Carbon content (g/kg)', blank=True, null=True)
    met_org_car = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Organic Carbon content', related_name='labdata_met_org_car_set', blank=True, null=True)
    org_mat = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Organic matter content (percentage)', blank=True, null=True)
    met_org_mat = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for organic matter content', related_name='labdata_met_org_mat_set', blank=True, null=True)
    caco3 = models.DecimalField(max_digits=30, decimal_places=10, db_comment='CaCO3 content (percentage)', blank=True, null=True)
    met_caco3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used CaCO3 content', related_name='labdata_met_caco3_set', blank=True, null=True)
    gypsum = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Gypsum content (percentage)', blank=True, null=True)
    met_gypsum = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Gypsum content', related_name='labdata_met_gypsum_set', blank=True, null=True)
    cec = models.DecimalField(max_digits=30, decimal_places=10, db_comment='CEC (cmol/Kg)', blank=True, null=True)
    met_cec = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for CEC', related_name='labdata_met_cec_set', blank=True, null=True)
    ca = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Ca++ (cmol/Kg)', blank=True, null=True)
    met_ca = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Ca++' , related_name='labdata_met_ca_set', blank=True, null=True)
    mg = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Mg++ (cmol/Kg)', blank=True, null=True)
    met_mg = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Mg++', related_name='labdata_met_mg_set', blank=True, null=True)
    na = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Na+ (cmol/Kg)', blank=True, null=True)
    met_na = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Na+', related_name='labdata_met_na_set', blank=True, null=True)
    k = models.DecimalField(max_digits=30, decimal_places=10, db_comment='K+ (cmol/Kg)', blank=True, null=True)
    met_k = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for K+', related_name='labdata_met_k_set', blank=True, null=True)
    n_tot = models.DecimalField(max_digits=30, decimal_places=10, db_comment='N tot content (g/Kg)', blank=True, null=True)
    met_n_tot = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for N tot content', related_name='labdata_met_n_tot_set', blank=True, null=True)
    p_cont = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Available P content(mg/kg)', blank=True, null=True)
    met_p_cont = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for available P content', related_name='labdata_met_p_cont_set', blank=True, null=True)
    feox = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Feox (g/kg)', blank=True, null=True)
    fed = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Fed (g/kg)', blank=True, null=True)
    fep = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Fep (g/kg)', blank=True, null=True)
    fe_tot = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Fe tot (g/kg)', blank=True, null=True)
    mn = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Mn (mg/kg)', blank=True, null=True)
    met_mn = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Mn', related_name='labdata_met_mn_set', blank=True, null=True)
    zn = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Zn (mg/kg)', blank=True, null=True)
    met_zn = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Zn', related_name='labdata_met_zn_set', blank=True, null=True)
    cu = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Cu (mg/kg)', blank=True, null=True)
    met_cu = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_comment='Method used for Cu', related_name='labdata_met_cu_set', blank=True, null=True) 
    act_caco3 = models.DecimalField(max_digits=30, decimal_places=10, db_comment='Active CaCO3 (%)', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'lab_data'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        # Ensures constraint on model level, raises ValidationError  
        if self.texture_class is not None and self.texture_class.startswith("l_texture_classes"):
            raise ValidationError({'texture_class': ('Wrong classification.')})  
        if self.classif_sys is not None and self.classif_sys.startswith("p_classification_system."):
            raise ValidationError({'classif_sys': ('Wrong classification.')}) 
        if self.upper is None or self.lower is None or self.upper < self.lower:
            raise ValidationError({'upper': ('lower cannot be smaller then upper or a null value.')}) 
    """

###########################
# Profile Layer
###########################
class LayerRemnants(models.Model):
    abundance = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cementing1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerremnants_cementing1_set', blank=True, null=True)
    cementing2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerremnants_cementing2_set', blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerremnants_size1_agent_set', blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerremnants_size2_agent_set', blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_remnants'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
    """
    def clean(self):
        if self.cementing_agent1 is not None and self.cementing_agent1.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agent1': ('Wrong classification.')})
        if self.cementing_agent2 is not None and self.cementing_agent2.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agent2': ('Wrong classification.')})    
        if self.size_agent1 is not None and self.size_agent1.startswith("l_size_shape."):
            raise ValidationError({'size_agent1': ('Wrong classification.')})
        if self.size_agent2 is not None and self.size_agent2.startswith("l_size_shape."):
            raise ValidationError({'size_agent2': ('Wrong classification.')})
    """

class LayerCoarseFragments(models.Model):
    litho_type1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_litho_type1_set', blank=True, null=True)
    litho_type2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_litho_type2_set', blank=True, null=True)
    litho_type3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_litho_type3_set', blank=True, null=True)
    litho_type4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_litho_type4_set', blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_size1_set', blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_size2_set', blank=True, null=True)
    size3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_size3_set', blank=True, null=True)
    size4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_size4_set', blank=True, null=True)
    weath1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_weath1_set', blank=True, null=True)
    weath2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_weath2_set', blank=True, null=True)
    weath3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_weath3_set', blank=True, null=True)
    weath4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layercoarsefragmentslithology_weath4_set', blank=True, null=True)
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
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
         
class LayerArtefacts(models.Model):
    abundance = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    black_carb = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    type1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_type1_set',  blank=True, null=True)
    type2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_type2_set',  blank=True, null=True)
    type3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_type3_set',  blank=True, null=True)
    type4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_type4_set',  blank=True, null=True)
    type5 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_type5_set',  blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_size1_set',  blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_size2_set',  blank=True, null=True)
    size3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_size3_set',  blank=True, null=True)
    size4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_size4_set',  blank=True, null=True)
    size5 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerartefacts_size5_set',  blank=True, null=True)
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
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.type1 is not None and self.type1.startswith("l_artefacts."):
                    raise ValidationError({'type1': ('Wrong classification.')})
            if self.type2 is not None and self.type2.startswith("l_artefacts."):
                    raise ValidationError({'type2': ('Wrong classification.')})
            if self.type3 is not None and self.type3.startswith("l_artefacts."):
                    raise ValidationError({'type3': ('Wrong classification.')})
            if self.type4 is not None and self.type4.startswith("l_artefacts."):
                    raise ValidationError({'type4': ('Wrong classification.')})
            if self.type5 is not None and self.type5.startswith("l_artefacts."):
                    raise ValidationError({'type5': ('Wrong classification.')})
            if self.size_type1 is not None and self.size_type1.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type1': ('Wrong classification.')})
            if self.size_type2 is not None and self.size_type2.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type2': ('Wrong classification.')})
            if self.size_type3 is not None and self.size_type3.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type3': ('Wrong classification.')})
            if self.size_type4 is not None and self.size_type4.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type4': ('Wrong classification.')})
            if self.size_type5 is not None and self.size_type5.startswith("l_artefacts_size."):
                    raise ValidationError({'size_type5': ('Wrong classification.')})         
    """    

class LayerCracks(models.Model):
    persistenc = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercracks_persistence_set', blank=True, null=True)
    continuity = models.ForeignKey(Taxonomy, models.SET_NULL,  related_name='layercracks_continuity_set', blank=True, null=True)
    avg_width = models.DecimalField(max_digits=16, decimal_places=2, validators=[validate_positive], blank=True, null=True)
    abundance = models.PositiveIntegerField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_cracks'
        db_table_comment = 'Report persistence and continuity'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
    
    """
    def clean(self):
        if self.persistence is not None and self.persistence.startswith("l_cracks_persistence."):
            raise ValidationError({'persistence': ('Wrong classification.')})
        if self.continuity is not None and self.continuity.startswith("l_cracks_continuity."):
            raise ValidationError({'continuity': ('Wrong classification.')})
    """
    
class LayerStressFeatures(models.Model):
    pressfaces = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Pressure faces in % of the surfaces of soil aggregates')
    slicksides = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Slickensides in % of the surfaces of soil aggregates.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_stress_features'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
        db_table_comment = 'Stress features result from soil aggregates that are pressed against each other due to swelling clays. The aggregate surfaces may be shiny. There are two types: Pressure faces do not slide past each other and have no striations, slickensides slide past each other and have striations.'

class LayerMatrixColours(models.Model):
    munsell_m1 = models.TextField(blank=True, null=True)
    munsell_d1 = models.TextField(blank=True, null=True)
    area1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    munsell_d2 = models.TextField(blank=True, null=True)
    area2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    munsell_d3 = models.TextField(blank=True, null=True)
    area3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_matrix_colour'
        db_table_comment = 'Report the colour of the soil matrix. If there is more than one matrix colour, report up to three, the dominant one first, and give the percentage of the exposed area'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class LayerTextureColour(models.Model):
    coars_text = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by coarser-textured parts of any orientation (vertical, horizontal, inclined) having a width of ≥ 0.5 cm')
    v_tongues = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by continuous vertical tongues of coarser-textured parts with a horizontal extension of ≥ 1 cm (if these tongues are absent, report 0%)')
    depth = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='the depth range in cm, where these tongues cover ≥ 10% of the exposed area (if they extend across several layers, the length is only reported in the description of that layer, where they start at the layer’s upper limit).')
    h_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='In the middle of the layer, prepare a horizontal surface, 50 cm x 50 cm, and report the percentage (by horizontal area covered) of the coarser-textured parts.')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_texture_colour'
        db_table_comment = 'If a layer consists of darker-coloured finer-textured and lighter-coloured coarser-textured parts that do not form horizontal layers but can easily be distinguished, describe them separately'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class LayerLithogenicVariegates(models.Model): 
    munsell_m1 = models.TextField(blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerlithogenicvariegates_size_class1_set', blank=True, null=True)
    area1 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m2 = models.TextField(blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerlithogenicvariegates_size_class2_set', blank=True, null=True)
    area2 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_m3 = models.TextField(blank=True, null=True)
    size3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerlithogenicvariegates_size_class3_set', blank=True, null=True)
    area3 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_lithogenic_variegates'
        db_table_comment = 'Report colour, size class, and abundance. If more than one colour occurs, report up to three, the dominant one first, and give size class and abundance for each colour separately.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        # Ensures constraint on model level, raises ValidationError  
        if self.size_class is not None and self.size_class.startswith("l_lithogenic_size."):
            raise ValidationError({'size_class': ('Wrong classification.')}) 
    """
           
class LayerRedoximorphicFeatures(models.Model):
    oxi_inner = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    oxi_outer = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    oxi_random = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    red_inner = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    red_outer = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    red_random = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abund_oxi = models.DecimalField(max_digits=12, decimal_places=4, validators=[validate_percentage], db_comment='Abundance of cemented oximorphic features, by volume [%]')
    
    #redoximorphic_colour_redoximorphic_features_set from LayerRedoximorphicColour
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_redoximorphic'
        db_table_comment = ''
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class LayerRedoximorphicColour(models.Model):
    features = models.ForeignKey(LayerRedoximorphicFeatures, on_delete=models.CASCADE, related_name='layerredoximorphiccolour_features_set', db_comment='LayerRedoximorphicFeatures')  
    colour_nr = models.SmallIntegerField(validators=[validate_positive], db_comment='layer redoximorphic colour number')
    munsell_m = models.TextField(blank=True, null=True)
    munsell_d = models.TextField(blank=True, null=True)
    substance = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_substance_set', blank=True, null=True)
    location = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_location_set',blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_size1_set',blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_size2_set',blank=True, null=True)
    mottles_c = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_mottles_c_set',blank=True, null=True)
    mottles_b = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_mottles_b_set',blank=True, null=True)
    cement = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerredoximorphiccolour_cement_set',blank=True, null=True)
    area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_redoximorphic_colour'
        db_table_comment = 'Report the colour according to the Munsell Color Charts'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        # Ensures constraint on model level, raises ValidationError    
            if self.substance is not None and self.substance.startswith("l_redoximorphic_substance."):
                
                    raise ValidationError({'substance': ('Wrong classification.')}) 
            if self.location is not None and self.location.startswith("l_redoximorphic_location."):
                
                    raise ValidationError({'location': ('Wrong classification.')}) 
            if self.size_class1 is not None and self.size_class1.startswith("l_oximorphic_size."):
                
                    raise ValidationError({'size_class1': ('Wrong classification.')}) 
            if self.size_class2 is not None and self.size_class2.startswith("l_oximorphic_size."):
                
                    raise ValidationError({'size_class2': ('Wrong classification.')}) 
            if self.mottles_contrast is not None and self.mottles_contrast.startswith("l_mottles_contrast."):
                
                    raise ValidationError({'mottles_contrast': ('Wrong classification.')})   
            if self.mottles_boundary is not None and self.mottles_boundary.startswith("l_mottles_boundary."):
                
                    raise ValidationError({'mottles_boundary': ('Wrong classification.')}) 
            if self.cementation_class is not None and self.cementation_class.startswith("l_oximorphic_cementation."):
                
                    raise ValidationError({'cementation_class': ('Wrong classification.')}) 
    """

class LayerCoatingsBridges(models.Model):
    clay_coat = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay coatings in percentage')
    form_coat = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercoatingsbridges_form_coat_set', blank=True, null=True, db_comment='refer to clay coatings')
    org_coat = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercoatingsbridges_org_coat_set', blank=True, null=True, db_comment='Organic matter coatings and oxide coatings on sand and/or coarse silt grains')
    crack_coat = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of cracked coatings in percentage')
    clay_bridg = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay bridges in percentage')
    form_bridg = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercoatingsbridges_form_bridg_set', blank=True, null=True, db_comment='refer to clay bridge')
    form_org = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercoatingsbridges_form_org_set', blank=True, null=True, db_comment='refer to organic matter coatings and oxide coatings (report only if matrix colour value ≤ 3)')
    sand_silt = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of uncoated sand and coarse silt grains in percentage')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_coatings_bridges'
        db_table_comment = 'Report the abundance of clay coatings in % of the surfaces of soil aggregates, coarse fragments and/or biopore walls clay bridges between sand grains in % of involved sand grains.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )
    
    """
    def clean(self):
            if self.form_coatings is not None and self.form_coatings.startswith("l_form_coatings."):
                    raise ValidationError({'form_coatings': ('Wrong classification.')})
            if self.form_bridge is not None and self.form_bridge.startswith("l_form_coatings."):
                    raise ValidationError({'form_bridge': ('Wrong classification.')})
            if self.organic_coatings is not None and self.organic_coatings.startswith("l_organic_coatings."):
                    raise ValidationError({'organic_coatings': ('Wrong classification.')})
            if self.form_organic is not None and self.form_organic.startswith("l_form_coatings."):
                    raise ValidationError({'form_organic': ('Wrong classification.')})
    """
                   
class LayerRibbonlikeAccumulations(models.Model):
    substances = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerribbonlikeaccumulations_substances_set', blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    comb_thick = models.DecimalField(max_digits=30, decimal_places=10, validators=[validate_positive], blank=True, null=True, db_comment='If there are 2 or more ribbon-like accumulations in one layer, report the number of the accumulations and their combined thickness in cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_ribbonlike_accumulations'
        db_table_comment = 'Ribbon-like accumulations are thin, horizontally continuous accumulations within the matrix of another layer. Report the accumulated substance(s).'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        if self.substances is not None and self.substances.startswith("l_ribbonlike_substances."):
            raise ValidationError({'substances': ('Wrong classification.')})
    """
            
class LayerCarbonates(models.Model):
    matr_c = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_matr_c_set', blank=True, null=True)
    matr_c_ret = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_matr_c_ret_set', blank=True, null=True)
    sec_type1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_type1_set', blank=True, null=True)
    sec_type2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_type2_set', blank=True, null=True)
    sec_type3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_type3_set', blank=True, null=True)
    sec_type4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_type4_set', blank=True, null=True)
    sec_size1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_size1_set', blank=True, null=True)
    sec_size2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_size2_set', blank=True, null=True)
    sec_size3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_size3_set', blank=True, null=True)
    sec_size4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_size4_set', blank=True, null=True)
    sec_shape1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_shape1_set', blank=True, null=True)
    sec_shape2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_shape2_set', blank=True, null=True)
    sec_shape3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_shape3_set', blank=True, null=True)
    sec_shape4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercarbonates_sec_shape4_set', blank=True, null=True)
    sec_abund1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    sec_abund2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    sec_abund3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    sec_abund4 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_carbonates'
        db_table_comment = 'Layer Carbonates'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        if self.matrix_carbonate_content is not None and self.carbonate_content.startswith("l_carbonate_contents"):
            raise ValidationError({'carbonate_content': ('Wrong classification.')}) 
        if self.matrix_carbonate_retarded_reaction is not None and self.carbonate_retarded_reaction.startswith("l_retarded_reaction"):
            raise ValidationError({'carbonate_retarded_reaction': ('Wrong classification.')}) 
        if self.secondary_type1 is not None and self.secondary_type1.startswith("l_secondary_carbonate_types."):
            raise ValidationError({'type1': ('Wrong classification.')})
        if self.secondary_type2 is not None and self.secondary_type2.startswith("l_secondary_carbonate_types."):
            raise ValidationError({'type2': ('Wrong classification.')})
        if self.secondary_type3 is not None and self.secondary_type3.startswith("l_secondary_carbonate_types."):
            raise ValidationError({'type3': ('Wrong classification.')})
        if self.secondary_type4 is not None and self.secondary_type4.startswith("l_secondary_carbonate_types."):
            raise ValidationError({'type4': ('Wrong classification.')})
        if self.secondary_size1 is not None and self.secondary_size1.startswith("l_mineral_size."):
            raise ValidationError({'size1': ('Wrong classification.')})
        if self.secondary_size2 is not None and self.secondary_size2.startswith("l_mineral_size."):
            raise ValidationError({'size2': ('Wrong classification.')})
        if self.secondary_size3 is not None and self.secondary_size3.startswith("l_mineral_size."):
            raise ValidationError({'size3': ('Wrong classification.')})
        if self.secondary_size4 is not None and self.secondary_size4.startswith("l_mineral_size."):
            raise ValidationError({'size4': ('Wrong classification.')})
        if self.secondary_shape1 is not None and self.secondary_shape1.startswith("l_mineral_shape."):
            raise ValidationError({'shape1': ('Wrong classification.')})
        if self.secondary_shape2 is not None and self.secondary_shape2.startswith("l_mineral_shape."):
            raise ValidationError({'shape2': ('Wrong classification.')})
        if self.secondary_shape3 is not None and self.secondary_shape3.startswith("l_mineral_shape."):
            raise ValidationError({'shape3': ('Wrong classification.')})
        if self.secondary_shape4 is not None and self.secondary_shape4.startswith("l_mineral_shape."):
            raise ValidationError({'shape4': ('Wrong classification.')})
    """

class LayerGypsum(models.Model):
    content = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_content_set', blank=True, null=True)
    sec_gypsum = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    sgypsum1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_sgypsum1_set', blank=True, null=True)
    sgypsum2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_sgypsum2_set', blank=True, null=True)
    type1_size = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_type1_size_set', blank=True, null=True)
    type2_size = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_type2_size_set', blank=True, null=True)
    type1_shape = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_type1_shap_set', blank=True, null=True)
    type2_shape = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layergypsum_type2_shap_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_gypsum'
        db_table_comment = 'Report the gypsum content in the soil matrix. If readily soluble salts are absent or present in small amounts only, gypsum can be estimated by measuring the electrical conductivity in soil suspensions of different soil-water relations after 30 minutes (in the case of fine-grained gypsum). This method detects primary and secondary gypsum. Note: Higher gypsum contents may be differentiated by abundance of H2O-soluble pseudomycelia/crystals and a soil colour with high value and low chroma'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        if self.sgypsum_type1 is not None and self.sgypsum_type1.startswith("l_sgypsum_type."):
                raise ValidationError({'sgypsum_type1': ('Wrong classification.')})
        if self.type1_size is not None and self.type1_size.startswith("l_mineral_size."):
                raise ValidationError({'type1_size': ('Wrong classification.')})
        if self.type1_shape is not None and self.type1_shape.startswith("l_mineral_shape."):
                raise ValidationError({'type1_shape': ('Wrong classification.')})
    """

class LayerSecondarySilica(models.Model):
    type1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersecondarysilica_type1_set', blank=True, null=True, db_comment='Report the type of secondary silica, type1 is dominant')
    type2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersecondarysilica_type2_set', blank=True, null=True, db_comment='Report the type of secondary silica')
    dnfcsize1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersecondarysilica_dnfcsize1_set', blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type1')
    dnfcsize2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersecondarysilica_dnfcsize2_set', blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type2')
    abund = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Report the total percentage (by exposed area) of secondary silica')
    abund_dnfc = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a cemented layer, report in addition the percentage (by volume) of those durinodes and remnants that have a diameter ≥ 1 cm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_secondary_silica'
        db_table_comment = 'Secondary silica (SiO2) is off-white and predominantly consisting of opal and microcrystalline forms. It occurs as laminar caps, lenses, (partly) filled interstices, bridges between sand grains, and as coatings at surfaces of soil aggregates, biopore walls, coarse fragments, and remnants of broken-up cemented layers. Report the type of secondary silica. If more than one type occurs, report up to two, the dominant one first.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.type1 is not None and self.type1.startswith("l_ssilica_types."):
                raise ValidationError({'type1': ('Wrong classification.')})
            if self.type2 is not None and self.type2.startswith("l_ssilica_types."):
                raise ValidationError({'type2': ('Wrong classification.')})
            if self.type1_dnfcsize is not None and self.type1_dnfcsize.startswith("l_dnfc_size."):
                raise ValidationError({'type1_dnfcsize': ('Wrong classification.')})
            if self.type2_dnfcsize is not None and self.type2_dnfcsize.startswith("l_dnfc_size."):
                raise ValidationError({'type2_dnfcsize': ('Wrong classification.')})
    """

class LayerConsistence(models.Model):
    cement = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Report the percentage (by volume, related to the whole soil) of the layer that is cemented.')
    cement_ag1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_cement_ag1_set', blank=True, null=True, db_comment='Report the cementing agents')
    cement_ag2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_cement_ag2_set', blank=True, null=True)
    cement_ag3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_cement_ag3_set', blank=True, null=True)
    cement_cls = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_cement_cls_set', blank=True, null=True)
    rrclass_m = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_rrclass_m_set', blank=True, null=True, db_comment='Rupture resistance, non-cemented soil moist')
    rrclass_d = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_rrclass_d_set', blank=True, null=True, db_comment='Rupture resistance, non-cemented soil dry')
    susceptib = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_susceptib_set', blank=True, null=True, db_comment='Some layers are prone to cementation after repeated drying and wetting. Report the susceptibility')
    m_failure = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_m_failure_set', blank=True, null=True, db_comment='Report the manner of failure (brittleness)')
    plastic = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerconsistence_plastic_set', blank=True, null=True, db_comment='Plasticity is the degree to which reworked soil can be permanently deformed without rupturing')
    penet_res = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    stickiness = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_consistence'
        db_table_comment = 'Consistence is the degree and kind of cohesion and adhesion that soil exhibits. Consistence is reported separately for cemented and non-cemented (parts of) layers. If a specimen of soil does not fall into pieces by applying low forces, one has to check, whether it is cemented'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        if self.cementing_agents1 is not None and self.cementing_agents1.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agents1': ('Wrong classification.')})
        if self.cementing_agents2 is not None and self.cementing_agents2.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agents2': ('Wrong classification.')})
        if self.cementing_agents3 is not None and self.cementing_agents3.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agents3': ('Wrong classification.')})
        if self.cementing_agents4 is not None and self.cementing_agents4.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agents4': ('Wrong classification.')})
        if self.cementation_class is not None and self.cementation_class.startswith("l_cementation_class."):
            raise ValidationError({'cementation_class': ('Wrong classification.')})
        if self.rrclass_moist is not None and self.rrclass_moist.startswith("rrclass_moist."):
            raise ValidationError({'rrclass_moist': ('Wrong classification.')})
        if self.rrclass_dry is not None and self.rrclass_dry.startswith("l_rrclass_dry."):
            raise ValidationError({'rrclass_dry': ('Wrong classification.')})
        if self.susceptibility is not None and self.susceptibility.startswith("l_susceptibility."):
            raise ValidationError({'susceptibility': ('Wrong classification.')})
        if self.manner_failure is not None and self.manner_failure.startswith("l_manner_failure."):
            raise ValidationError({'manner_failure': ('Wrong classification.')})
        if self.plasticity is not None and self.plasticity.startswith("l_plasticity."):
            raise ValidationError({'plasticity': ('Wrong classification.')})
        if self.stickiness is not None and self.stickiness.startswith("l_stickiness."):
            raise ValidationError({'stickiness': ('Wrong classification.')})
    """

class LayerSurfaceCrusts(models.Model):
    sealing1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersurfacecrusts_sealing1_set', blank=True, null=True)
    sealing2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersurfacecrusts_sealing2_set', blank=True, null=True)
    sealing3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layersurfacecrusts_sealing3_set', blank=True, null=True)
    avg_thickn = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_surface_crusts'
        db_table_comment = 'A crust is a thin layer of soil constituents bound together into a horizontal mat or into small polygonal plates (see Schoeneberger et al., 2012). Soil crusts develop in the first mineral layer(s) and are formed by a sealing agent of physical, chemical and/or biological origin.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.sealing_agent1 is not None and self.sealing_agent1.startswith("l_sealing_agent."):
                raise ValidationError({'sealing_agent1': ('Wrong classification.')})
            if self.sealing_agent2 is not None and self.sealing_agent2.startswith("l_sealing_agent."):
                raise ValidationError({'sealing_agent2': ('Wrong classification.')})
            if self.sealing_agent3 is not None and self.sealing_agent3.startswith("l_sealing_agent."):
                raise ValidationError({'sealing_agent3': ('Wrong classification.')})
    """

class LayerPermafrostFeatures(models.Model):
    cry_alter1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_cry_alter1_set', blank=True, null=True)
    cry_alter2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_cry_alter2_set', blank=True, null=True)
    cry_alter3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_cry_alter3_set', blank=True, null=True)
    permafrost = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_layers_permafrost_set', blank=True, null=True)
    cry_abund1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cry_abund2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cry_abund3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_permafrost_features'
        db_table_comment = 'Estimate the total percentage (by exposed area, related to the whole soil) affected by cryogenic alteration. Report up to three features, the dominant one first, and report the percentage for each feature separately.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.cryogenic_alteration1 is not None and self.cryogenic_alteration1.startswith("l_cryogenic_alteration."):
                    raise ValidationError({'cryogenic_alteration1': ('Wrong classification.')})
            if self.cryogenic_alteration2 is not None and self.cryogenic_alteration2.startswith("l_cryogenic_alteration."):
                    raise ValidationError({'cryogenic_alteration2': ('Wrong classification.')})
            if self.cryogenic_alteration3 is not None and self.cryogenic_alteration3.startswith("l_cryogenic_alteration."):
                    raise ValidationError({'cryogenic_alteration3': ('Wrong classification.')})
            if self.layers_permafrost is not None and self.layers_permafrost.startswith("l_layers_permafrost."):
                    raise ValidationError({'layers_permafrost': ('Wrong classification.')})
    """

class LayerOrganicCarbon(models.Model):
    contentmin = models.DecimalField(max_digits=40, decimal_places=10, blank=True, null=True)
    contentmax = models.DecimalField(max_digits=40, decimal_places=10, blank=True, null=True)
    nat_accum1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerorganiccarbon_nat_accum1_set', blank=True, null=True)
    nat_accum2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerorganiccarbon_nat_accum2_set', blank=True, null=True)
    nat_accum3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerorganiccarbon_nat_accum3_set', blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    black_carb = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_organic_carbon'
        db_table_comment = 'Report the estimated organic carbon content. It is based on the Munsell value, moist, and the texture'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.natural_accumulations1 is not None and self.natural_accumulations1.startswith("l_accumulation."):
                    raise ValidationError({'natural_accumulations1': ('Wrong classification.')})
            if self.natural_accumulations2 is not None and self.natural_accumulations2.startswith("l_accumulation."):
                    raise ValidationError({'natural_accumulations2': ('Wrong classification.')})
            if self.natural_accumulations3 is not None and self.natural_accumulations3.startswith("l_accumulation."):
                    raise ValidationError({'natural_accumulations3': ('Wrong classification.')})
    """

class LayerRoots(models.Model):
    a_lt2mm = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerroots_a_lt2mm_set', blank=True, null=True, db_comment='diameter <= 2mm')
    a_lt05mm = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerroots_a_lt05mm_set', blank=True, null=True, db_comment='diameter < 0,5mm')
    a_05to2mm = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerroots_a_05to2mm_set', blank=True, null=True, db_comment='diameter from 0.5 to 2 mm')
    a_gt2mm = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerroots_a_gt2mm_set', blank=True, null=True, db_comment='diameter > 2mm')
    a_2to5mm = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerroots_a_2to5mm_set', blank=True, null=True, db_comment='diameter from 2 to 5 mm')
    a_gt5mm = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerroots_a_gt5mm_set', blank=True, null=True, db_comment='diameter > 5mm')
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_roots'
        db_table_comment = 'Count the number of roots per dm2, separately for the six diameter classes, and report the abundance classes'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.abundance_less2mm is not None and self.abundance_less2mm.startswith("l_root_abundance."):
                    raise ValidationError({'abundance_less2mm': ('Wrong classification.')})
            if self.abundance_less05mm is not None and self.abundance_less05mm.startswith("l_root_abundance."):
                    raise ValidationError({'abundance_less05mm': ('Wrong classification.')})
            if self.abundance_05to2mm is not None and self.abundance_05to2mm.startswith("l_root_abundance."):
                    raise ValidationError({'abundance_05to2mm': ('Wrong classification.')})
            if self.abundance_greater2mm is not None and self.abundance_greater2mm.startswith("l_root_abundance."):
                    raise ValidationError({'abundance_greater2mm': ('Wrong classification.')})
            if self.abundance_2to5mm is not None and self.abundance_2to5mm.startswith("l_root_abundance."):
                    raise ValidationError({'abundance_2to5mm': ('Wrong classification.')})
            if self.abundance_greater5mm is not None and self.abundance_greater5mm.startswith("l_root_abundance."):
                    raise ValidationError({'abundance_greater5mm': ('Wrong classification.')})
    """

class LayerAnimalActivity(models.Model):
    type1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='Layeranimalactivity_type1_set', blank=True, null=True)
    type2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='Layeranimalactivity_type2_set', blank=True, null=True)
    type3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='Layeranimalactivity_type3_set', blank=True, null=True)
    type4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='Layeranimalactivity_type4_set', blank=True, null=True)
    type5 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='Layeranimalactivity_type5_set', blank=True, null=True)
    mammal = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    bird = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    worm = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    insect = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    unspecify = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_animal_activity'
        db_table_comment = 'Report the animal activity that has visibly changed the features of the layer. If applicable, report up to 5 types, the dominant one first. Report the percentage (by exposed area), separately for mammal activity, bird activity, worm activity, insect activity and unspecified activity'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.type1 is not None and self.type1.startswith("l_type_animal_activity."):
                raise ValidationError({'type1': ('Wrong classification.')})
            if self.type2 is not None and self.type2.startswith("l_type_animal_activity."):
                raise ValidationError({'type2': ('Wrong classification.')})
            if self.type3 is not None and self.type3.startswith("l_type_animal_activity."):
                raise ValidationError({'type3': ('Wrong classification.')})
            if self.type4 is not None and self.type4.startswith("l_type_animal_activity."):
                raise ValidationError({'type4': ('Wrong classification.')})
            if self.type5 is not None and self.type5.startswith("l_type_animal_activity."):
                raise ValidationError({'type5': ('Wrong classification.')})
    """

class LayerHumanAlterations(models.Model):
    nat_mat1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_nat_mat1_set', blank=True, null=True)
    nat_mat2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_nat_mat2_set', blank=True, null=True)
    nat_mat3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_nat_mat3_set', blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    texture = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_texture_set', blank=True, null=True)
    carbonate = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_carbonate_set', blank=True, null=True)
    carbon = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    alter1 = models.ForeignKey(Taxonomy, models.SET_NULL,related_name='layerhumanalterations_alter1_set',  blank=True, null=True)
    alter2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_alter2_set', blank=True, null=True)
    aggregate = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerhumanalterations_aggregate_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_human_alterations'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.natural_material1 is not None and self.natural_material1.startswith("l_natural_material."):
                    raise ValidationError({'natural_material1': ('Wrong classification.')})
            if self.natural_material2 is not None and self.natural_material2.startswith("l_natural_material."):
                    raise ValidationError({'natural_material2': ('Wrong classification.')})
            if self.natural_material3 is not None and self.natural_material3.startswith("l_natural_material."):
                    raise ValidationError({'natural_material3': ('Wrong classification.')})
            if self.texture_class is not None and self.texture_class.startswith("l_texture_classes."):
                    raise ValidationError({'texture_class': ('Wrong classification.')})
            if self.carbonate_content is not None and self.carbonate_content.startswith("l_secondary_carbonate_types."):
                    raise ValidationError({'carbonate_content': ('Wrong classification.')})
            if self.alteration1 is not None and self.alteration1.startswith("l_insitu_alterations."):
                    raise ValidationError({'alteration1': ('Wrong classification.')})
            if self.alteration2 is not None and self.alteration2.startswith("l_insitu_alterations."):
                    raise ValidationError({'alteration2': ('Wrong classification.')})
            if self.aggregate_formation is not None and self.aggregate_formation.startswith("l_aggregate_formation."):
                    raise ValidationError({'aggregate_formation': ('Wrong classification.')})
    """

class LayerDegreeDecomposition(models.Model):
    vis_plant = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    sbdiv_horz = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerdegreedecomposition_sbdiv_horz_set', blank=True, null=True)
    plant_res1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerdegreedecomposition_plant_res1_set', blank=True, null=True)
    plant_res2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerdegreedecomposition_plant_res2_set', blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_degree_decomposition'
        db_table_comment = 'Refer to the transformation of visible plant tissues into visibly homogeneous organic matter.'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
            if self.subdivision_horizon is not None and self.subdivision_horizon.startswith("l_subdivision_horizon."):
                    raise ValidationError({'subdivision_horizon': ('Wrong classification.')})
            if self.plant_residue1 is not None and self.plant_residue1.startswith("l_dead_plant."):
                    raise ValidationError({'plant_residue1': ('Wrong classification.')})
            if self.plant_residue2 is not None and self.plant_residue2.startswith("l_dead_plant."):
                    raise ValidationError({'plant_residue2': ('Wrong classification.')})   
    """

class LayerNonMatrixPore(models.Model):
    type1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type1_set', blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type1size_set', blank=True, null=True)
    abund1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type1abund_set', blank=True, null=True)
    type2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type2_set', blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type2size_set', blank=True, null=True)
    abund2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type2abund_set', blank=True, null=True)
    type3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type3_set', blank=True, null=True)
    size3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type3size_set', blank=True, null=True)
    abund3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type3abund_set', blank=True, null=True)
    type4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type4_set', blank=True, null=True)
    size4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type4size_set', blank=True, null=True)
    abund4 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layernonmatrixpore_type4abund_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_nonmatrix_pore'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        # Ensures constraint on model level, raises ValidationError  
        if self.type1 is not None and self.type1.startswith("l_nonmatrix_pores."):
            raise ValidationError({'type1': ('Wrong classification.')}) 
        if self.type2 is not None and self.type2.startswith("l_nonmatrix_pores."):
            raise ValidationError({'type2': ('Wrong classification.')}) 
        if self.type3 is not None and self.type3.startswith("l_nonmatrix_pores."):
            raise ValidationError({'type3': ('Wrong classification.')}) 
        if self.type4 is not None and self.type4.startswith("l_nonmatrix_pores."):
            raise ValidationError({'type4': ('Wrong classification.')}) 
        if self.type2 is not None and self.type1 is None :
            raise ValidationError({'type2': ('nonmatrix_pore type1 is indefined.')}) 
        if self.type3 is not None and ( self.type1 is None or self.type2 is None ):
            raise ValidationError({'type3': ('nonmatrix_pore type1 or type2 is indefined.')}) 
        if self.type4 is not None and ( self.type1 is None or self.type2 is None or self.type3 is None):
            raise ValidationError({'type4': ('nonmatrix_pore type1 or type2 or type3 is indefined.')}) 
        if self.type1_dominant_size is not None and self.type1_dominant_size.startswith("l_pore_size."):
            raise ValidationError({'type1_dominant_size': ('Wrong classification.')}) 
        if self.type1_abundance is not None and self.type1_abundance.startswith("l_pore_abundance."):
            raise ValidationError({'type1_abundance': ('Wrong classification.')})
        if self.type2_dominant_size is not None and self.type2_dominant_size.startswith("l_pore_size."):
            raise ValidationError({'type2_dominant_size': ('Wrong classification.')}) 
        if self.type2_abundance is not None and self.type2_abundance.startswith("l_pore_abundance."):
            raise ValidationError({'type2_abundance': ('Wrong classification.')})
        if self.type3_dominant_size is not None and self.type3_dominant_size.startswith("l_pore_size."):
            raise ValidationError({'type3_dominant_size': ('Wrong classification.')}) 
        if self.type3_abundance is not None and self.type3_abundance.startswith("l_pore_abundance."):
            raise ValidationError({'type3_abundance': ('Wrong classification.')})
        if self.type4_dominant_size is not None and self.type4_dominant_size.startswith("l_pore_size."):
            raise ValidationError({'type4_dominant_size': ('Wrong classification.')}) 
        if self.type4_abundance is not None and self.type4_abundance.startswith("l_pore_abundance."):
            raise ValidationError({'type4_abundance': ('Wrong classification.')}) 
    """
 
class ProfileLayer(models.Model):
    profile = models.ForeignKey(ProfileGeneral, on_delete=models.CASCADE, related_name='profilelayer_profile_set', db_comment='Foreign Key field: profile') 
    design = models.TextField(db_comment='layer horizon designation')
    number = models.SmallIntegerField(validators=[validate_positive], db_comment='layer order in profile')
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm',blank=True, null=True)
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm',blank=True, null=True)
    lower_bound = models.TextField(db_comment='layer lower boundary ')
    hom_part = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    hom_alluvt = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_hom_alluvt_set', blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    wat_satur = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_wat_satur_set', blank=True, null=True, db_comment='Types of water saturation')
    wat_status = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_wat_status_set', blank=True, null=True, db_comment='Soil water status')
    o_mineral = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_o_mineral_set', blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    bounddist = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_bounddist_set', blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundshape = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_boundshape_set', blank=True, null=True)
    wind = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_wind_set', blank=True, null=True, db_comment='Wind deposition')
    tex_cls = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_tex_cls_set', blank=True, null=True, db_comment='Texture class') 
    tex_subcls = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_tex_subcls_set', blank=True, null=True, db_comment='Texture subclass')
    struct_w_s = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Structure Wedge-shaped aggregates tilted between ≥ 10° and ≤ 60° from the horizontal: abundance, by volume [%]')
    rh_value = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_rh_value_set', blank=True, null=True, db_comment='Rh Value')
    weathering = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], db_comment='Initial weathering abundance')
    sol_salts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    ph_value = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    ph_solution = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_phsolution_layers', blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    fracts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    avg_fracts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    volc_abund = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_volc_abund', blank=True, null=True)
    volc_thnaf = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_volc_thnaf_layers', blank=True, null=True)
    bulk_dens = models.DecimalField(max_digits=30, decimal_places=10, blank=True, null=True)
    pack_dens = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_pack_dens_layers', blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_mat = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilelayer_parent_mat_layers', blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    note = models.TextField(blank=True, null=True)

    remnants = models.OneToOneField(LayerRemnants, on_delete=models.SET_DEFAULT, default=None, db_comment='Remnants of broken-up cemented layers')
    coarsefragments = models.OneToOneField(LayerCoarseFragments, on_delete=models.SET_DEFAULT, default=None, db_comment='Coarse fragments')
    artefacts = models.OneToOneField(LayerArtefacts, on_delete=models.SET_DEFAULT, default=None, db_comment='Artefacts')
    cracks = models.OneToOneField(LayerCracks, on_delete=models.SET_DEFAULT, default=None, db_comment='Cracks')
    stressfeatures = models.OneToOneField(LayerStressFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='Stress Features')
    coatingsbridges = models.OneToOneField(LayerCoatingsBridges, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerCoatingsBridges')
    ribbonlikeaccumulations = models.OneToOneField(LayerRibbonlikeAccumulations, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRibbonlikeAccumulations')
    carbonates = models.OneToOneField(LayerCarbonates, on_delete=models.SET_DEFAULT, default=None, db_comment='Section Layer Carbonates')
    gypsum = models.OneToOneField(LayerGypsum, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerGypsum')
    secondarysilica = models.OneToOneField(LayerSecondarySilica, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerSecondarySilica')
    consistence = models.OneToOneField(LayerConsistence, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerConsistence')
    surfacecrusts = models.OneToOneField(LayerSurfaceCrusts, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerSurfaceCrusts')   
    permafrost =  models.OneToOneField(LayerPermafrostFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerPermafrostFeatures')   
    organiccarbon =  models.OneToOneField(LayerOrganicCarbon, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerOrganicCarbon')   
    roots =  models.OneToOneField(LayerRoots, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRoots')   
    animalactivity  =  models.OneToOneField(LayerAnimalActivity, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerAnimalActivity')   
    humanalterations =  models.OneToOneField(LayerHumanAlterations, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerHumanAlterations')   
    degreedecomposition =  models.OneToOneField(LayerDegreeDecomposition, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerDegreeDecomposition')   
    nonmatrixpore = models.OneToOneField(LayerNonMatrixPore, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerNonMatrixPore')   
    labdata =  models.OneToOneField(LabData, on_delete=models.SET_DEFAULT, default=None, db_comment='Layer Laboratory data')
    matrixcolours = models.OneToOneField(LayerMatrixColours, on_delete=models.SET_DEFAULT, default=None, db_comment='Matrix colour')   
    texturecolour = models.OneToOneField(LayerTextureColour, on_delete=models.SET_DEFAULT, default=None, db_comment='Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts')
    lithogenicvariegates = models.OneToOneField(LayerLithogenicVariegates, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerLithogenicVariegates')
    redoximorphicfeatures = models.OneToOneField(LayerRedoximorphicFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRedoximorphicFeatures')
    
    ## layerstructure_layer_set LayerStructure

    def _get_thickness(self):
        "Returns the thickness"
        if self.lower and self.upper: 
            return self.lower - self.upper
        else: return None
    thickness = property(_get_thickness)   
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'layer'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class LayerStructure(models.Model):
    LEVEL_TYPES = [
        ("Type 1" , "First level structure Type 1"),
        ("Type 2" , "First level structure Type 2"),
        ("Type 3" , "First level structure Type 3"),
        ("Type 1.1" , "Second level structure Type 1.1"),
        ("Type 1.2" , "Second level structure Type 1.2"),
        ("Type 2.1" , "Second level structure Type 2.1"),
        ("Type 2.2" , "Second level structure Type 2.2"),
        ("Type 3.1" , "Second level structure Type 3.1"),
        ("Type 3.2" , "Second level structure Type 3.2"),
        ("Type 1.1.1" , "Third-level structure Type 1.1.1"),
        ("Type 1.2.1" , "Third-level structure Type 1.2.1"),
        ("Type 2.1.1" , "Third-level structure Type 2.1.1"),
        ("Type 2.2.1" , "Third-level structure Type 2.2.1"),
        ("Type 3.1.1" , "Third-level structure Type 3.1.1"),
        ("Type 3.2.1" , "Third-level structure Type 3.2.1"),
    ]
    
    layer = models.ForeignKey(ProfileLayer, on_delete=models.CASCADE, related_name='layerstructure_layer_set', db_comment='Profile Layer' )
    level = models.TextField(choices=LEVEL_TYPES)
    type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerstructure_type_set', blank=True, null=True)
    grade = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerstructure_grade_set', blank=True, null=True)
    penetrab = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerstructure_penetrab_set', blank=True, null=True)
    size1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerstructure_size1_set', blank=True, null=True)
    size2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='layerstructure_size2_set', blank=True, null=True)
    abundance_vol = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer_structure_types'
        unique_together = (('layer', 'level'),)
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

    """
    def clean(self):
        # Ensures constraint on model level, raises ValidationError
        if self.type is not None and self.type.startswith("l_structure_types."):
            raise ValidationError({'type': ('Wrong classification.')}) 
        if self.grade is not None and self.grade.startswith("l_structural_grade."):
            raise ValidationError({'grade': ('Wrong classification.')}) 
        if self.penetrability is not None and self.penetrability.startswith("l_aggregate_penetrability."):
            raise ValidationError({'penetrability': ('Wrong classification.')}) 
        if self.size_class1 is not None and self.size_class1.startswith("l_aggregate_size."):
            raise ValidationError({'size_class1': ('Wrong classification.')}) 
        if self.size_class2 is not None and self.size_class2.startswith("l_aggregate_size."):
            raise ValidationError({'size_class2': ('Wrong classification.')})      
    """