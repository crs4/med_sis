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

class Taxonomy(models.Model):
    name = models.TextField(db_comment='category code')
    criterion = models.TextField(db_comment='category description')
    taxonomy = models.TextField(db_comment='taxonomy name')
    super = models.TextField(db_comment='super category name', blank=True, null=True)
     
    def _get_code(self):
        "Returns the category code"
        return self.taxonomy + '.' + self.name
    
    code = property(_get_code) 
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        unique_together = (('taxonomy', 'name'),)
        db_table = 'taxonomy'
        db_table_comment = 'SOILS4MED Taxonomies from WRB2022 Taxonomies'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class Project(models.Model):
    code = models.TextField(blank=True, null=True, db_comment='Project identifier ')
    title = models.TextField(blank=True, null=True, db_comment='project name')
    description = models.TextField(blank=True, null=True, db_comment='project description')
    
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
    project_id = models.IntegerField(blank=True, null=True, db_comment='project identifier in the SIS')
    owner_note = models.TextField(blank=True, null=True, db_comment='note about owner ')
    reference = models.TextField(blank=True, null=True, db_comment='reference')
    pub_year = models.IntegerField(blank=True, null=True, db_comment='year of pubblication')
    web_link = models.TextField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True, db_comment='Data availability and/or use restrictions')
    
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

class LandformTopography(models.Model):
    gradient_upslope = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface upslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    gradient_downslope = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface downslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    slope_aspect = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_positive], blank=True, null=True, db_comment='If the profile lies on a slope, report the compass direction that the slope faces, viewed downslope; e.g., 225°')
    slope_shape = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='slope_shape_landforms', blank=True, null=True, db_comment='If the profile lies on a slope, report the slope shape in 2 directions: up-/downslope (perpendicular to the elevation contour, i.e. the vertical curvature) and across slope (along the elevation contour, i.e. the horizontal curvature); e.g., Linear (L), Convex (V) or Concave (C).')
    profile_position = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='profile_position_landforms', blank=True, null=True, db_comment='If the profile lies in an uneven terrain, report the profile position.')
    landform1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='landform1_landforms', blank=True, null=True)
    landform2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='landform2_landforms', blank=True, null=True)
    landform1_activity = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='landform1_activity_landforms', blank=True, null=True)
    landform2_activity = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='landform2_activity_landforms', blank=True, null=True)
    geomorphic_features_description = models.TextField(blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'landform_topography'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class ClimateAndWeather(models.Model):
    climate_koppen = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='climate_koppen', related_name='profileclimateweather_climate_koppen_set', blank=True, null=True)
    ecozone_shultz = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='ecozone_shultz', related_name='profileclimateweather_ecozone_shultz_set', blank=True, null=True)
    season = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='season', related_name='profileclimateweather_season_set', blank=True, null=True)
    current_weather = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='current_weather', related_name='profileclimateweather_current_weather_set', blank=True, null=True)
    past_weather = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='past_weather', related_name='profileclimateweather_past_weather_set', blank=True, null=True)
    soil_temp_regime = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='soil_temp_regime', related_name='profileclimateweather_soil_temp_regime_set', blank=True, null=True)
    soil_moist_regime = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='soil_moist_regime', related_name='profileclimateweather_soil_moist_regime_set', blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'climate_weather'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

class LandUse(models.Model):
    land_use = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='land_use_landuses', blank=True, null=True)
    corine = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='corine_landuses', blank=True, null=True)
    cultivated =  models.OneToOneField('Cultivated', on_delete=models.SET_DEFAULT, default=None, db_comment='Cultivated Section')
    
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

class Cultivated(models.Model):
    cultivation_type = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='cultivation_type', blank=True, null=True, db_comment='value from p_cultivation_type ')
    actual_species1 = models.TextField(blank=True, null=True, db_comment='actual dominant specie')
    actual_species2 = models.TextField(blank=True, null=True, db_comment='actual second specie')
    actual_species3 = models.TextField(blank=True, null=True, db_comment='actual third specie')
    cultivation_cessation = models.DateField(blank=True, null=True, db_comment='editable if last dominant specie is NOT NULL')
    cultivation_cover_by_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    spec_prod_tech1 = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='spec_prod_tech1', related_name='profilecultivated_special_productivity_technique1_set', blank=True, null=True, db_comment='Report the techniques that refer to the surrounding area of the soil profile. If more than one type of technique is present, report in the array up to three, the dominant one first. Value from p_productivity_techniques')
    spec_prod_tech2 = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='spec_prod_tech2', related_name='profilecultivated_special_productivity_technique2_set', blank=True, null=True)
    spec_prod_tech3 = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='spec_prod_tech3', related_name='profilecultivated_special_productivity_technique3_set', blank=True, null=True)
    last_species1 = models.TextField(blank=True, null=True, db_comment="last dominant specie, editable if actual_species1 is NULL")
    last_species2 = models.TextField(blank=True, null=True, db_comment="Second last specie, editable if actual_species2 is NULL ")
    last_species3 = models.TextField(blank=True, null=True, db_comment="Third last specie, editable if actual_species3 is NULL ")
    rotational_species1 = models.TextField(blank=True, null=True, db_comment='Report the dominant specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the most frequent)')
    rotational_species2 = models.TextField(blank=True, null=True, db_comment='Report the second specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    rotational_species3 = models.TextField(blank=True, null=True, db_comment='Report the third specie that have been cultivated in the last five years in rotation with the actual or last species (the first is the mostfrequent)')
    
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

class Surface(models.Model):
    surface_crusts_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    patterned_ground_form = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profile_patterned_ground_form_set', blank=True, null=True, db_comment='Patterned ground form field')
    technical_surface_alteration = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profile_technical_surface_alteration_set', blank=True, null=True)
    bedrock_formation_name = models.TextField(blank=True, null=True)
    bedrock_lithology = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='bedrock_lithology', blank=True, null=True)
    outcrops_area_covered = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    outcrops_average_distance = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    outcrops_size = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    ground_water_depth = models.DecimalField(max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    water_above_surface = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profile_water_above_surface_set', blank=True, null=True)
    water_drainage_condition = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profile_water_drainage_condition_set', blank=True, null=True)
    water_repellence_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profile_water_repellence_type_set', blank=True, null=True)
    desert_ventifacts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    desert_varnish = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('backoffice')
    
    class Meta:
        managed = True
        db_table = 'surface'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
        )

"""     def clean(self):
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
        
        error_collector.raise_errors() """

class ProfileLayer(models.Model):
    profile = models.ForeignKey('ProfileGeneral', on_delete=models.CASCADE, related_name='layer_profile_set', db_comment='Foreign Key field: profile') 
    designation = models.TextField(db_comment='Horizon designation')
    layer_number = models.SmallIntegerField(validators=[validate_positive], db_comment='layer order in profile')
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm')
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm')
    homogeneity_part = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    homogeneity_alluvial_tephra = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='homogeneity_alluvial_tephra_layers', blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    water_saturation = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='water_saturation_layers', blank=True, null=True, db_comment='Types of water saturation')
    water_status = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='water_status_layers', blank=True, null=True, db_comment='Soil water status')
    organicmineral = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='organicmineral_layers', blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    boundaries_distinctness = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='boundaries_distinctness_layers', blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundaries_shape = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='boundaries_shape_layers', blank=True, null=True)
    wind_disposition = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='wind_disposition_layers', blank=True, null=True, db_comment='Wind deposition')
    texture_class = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='texture_class_layers', blank=True, null=True, db_comment='Texture class') 
    texture_subclass = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='texture_subclass_layers', blank=True, null=True, db_comment='Texture subclass')
    rh_value = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='rh_value_layers', blank=True, null=True, db_comment='Rh Value')
    initial_weathering = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], db_comment='Initial weathering abundance')
    soluble_salts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    field_ph_misured_value = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    field_ph_solution = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='field_ph_solution_layers', blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    continuity_volume_fractures = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    continuity_average_fractures = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    volcanic_glasses_abundance = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='volcanic_glasses_abundance_layers', blank=True, null=True)
    volcanic_glasses_thixotropy_naf = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='volcanic_glasses_thixotropy_naf_layers', blank=True, null=True)
    bulk_density = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    packing_density = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='packing_density_layers', blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_material = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='parent_material_layers', blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    note = models.TextField(blank=True, null=True)
    
    def _get_thickness(self):
        "Returns the thickness"
        return self.lower - self.upper
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

class ProfileGeneral(models.Model):
    code = models.TextField(primary_key=True, db_comment='profile identifier')
    date = models.DateField(db_comment='date of the description')
    surveyors = models.TextField(blank=True, null=True, db_comment='surveyors names comma separated')
    location_name = models.TextField(blank=True, null=True, db_comment='Name of the profile location')
    lat_wgs84 = models.DecimalField(max_digits=20, decimal_places=10, db_comment='WGS84 Latitude in decimal degree')
    lon_wgs84 = models.DecimalField(max_digits=20, decimal_places=10, db_comment='WGS84 Longitude in decimal degree')
    gps = models.BooleanField(blank=True, null=True, db_comment='is a gps acquisition?')
    elevation_m_asl = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True, db_comment='Altitude above the sea level in meter')
    elevation_dem = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True, db_comment='Altitude in meters retrived from a dem in meter')
    survey_method = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profile_survey_method_set',  blank=True, null=True, db_comment='The code of the survey method')
    notes = models.TextField(blank=True, null=True)

    landuse =  models.OneToOneField(LandUse, on_delete=models.SET_DEFAULT, default=None, db_comment='LandUse Section')
    surface =  models.OneToOneField(Surface, on_delete=models.SET_DEFAULT, default=None, db_comment='Surface Section')
    landform_topography = models.OneToOneField(LandformTopography, on_delete=models.SET_DEFAULT, default=None, db_comment='landform_topography Section')
    climate_weather = models.OneToOneField(ClimateAndWeather, on_delete=models.SET_DEFAULT, default=None, db_comment='Climate weather Section')
    
    horizon_sequence = models.TextField(blank=True, null=True, db_comment='Horizons sequence of the profile')
    old_classification = models.TextField(blank=True, null=True, db_comment='Old classification of the profile location')
    new_classification = models.TextField(blank=True, null=True, db_comment='New classification of the profile location')
    classification_sys = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilehorizonsequence_classification_sys_set', blank=True, null=True, db_comment='value from p_classification_system ')
    
    project = models.ForeignKey(Project, models.SET_NULL, blank=True, null=True, related_name='profile_project_set', db_comment='Survey/Project identifier')
    genealogy =  models.OneToOneField(Genealogy, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Genealogy')
    
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