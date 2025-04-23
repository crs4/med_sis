""" # This is the Django model module for SoilData App.
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_percentage(value):
    if not ( isinstance(value, (int, float, complex)) and value >= 0 and value <= 100 ):
      raise ValidationError("%(value)s is not a percentage" )

def validate_positive(value):
    if not ( isinstance(value, (int, float, complex)) and value >= 0 ):
      raise ValidationError("%(value)s is negative" )

def validate_latitude(value):
    if not ( isinstance(value, (int, float, complex)) and value > -90 and value < 90 ) :
      raise ValidationError("%(value)s isn't a valid latitude" )

def validate_longitude(value):
    if not ( isinstance(value, (int, float, complex)) and value > -180 and value < 180 ) :
      raise ValidationError("%(value)s isn't a valid longitude" )

###########################
## Utilities
###########################
class Taxonomy(models.Model):
    name = models.TextField(db_comment='category code')
    criterion = models.TextField(db_comment='category description')
    taxonomy = models.TextField(db_comment='taxonomy name')
    super = models.TextField(db_comment='super category name', blank=True, null=True)
     
    def _get_code(self):
        "Returns the category code"
        return self.taxonomy + '.' + self.name
    
    code = property(_get_code) 
    
    objects = models.Manager().using('soildatastore')
     
    class Meta:
        managed = True
        unique_together = (('taxonomy', 'name'),)
        db_table = 'taxonomy'
        db_table_comment = 'SOILS4MED Taxonomies from WRB2022 Taxonomies'
  
class LabMethod(models.Model):
    name = models.TextField(db_comment='method name',primary_key=True )
    type = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='type', related_name='labmethod_type_set', blank=True, null=True)
    description = models.TextField(blank=True, null=True, db_comment='method description')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'lab_method'
        db_table_comment = 'Laboratory methods'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )    

class LabMeasurement(models.Model):
    name = models.TextField(db_comment='measure name', primary_key=True )
    method_type = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='type', related_name='labmeasure_type_set', blank=True, null=True)
    description = models.TextField(blank=True, null=True, db_comment='measure description')
    unit = models.TextField(blank=True, null=True, db_comment='unit of measure')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'lab_measure'
        db_table_comment = 'Laboratory measures'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        ) 
          
###########################
## XLSx Uploads
###########################
class XLSxUpload(models.Model):

    UPLOAD_RESULTS = [
        ("0" , "system error"),
        ("1" , "data imported with error"),
        ("2" , "data sucessfully imported"),
    ]
    type = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='type', related_name='xlsxupload_type_set', db_comment='Type of the upload')
    report = models.JSONField( db_comment='Report of the upload')
    data = models.JSONField( db_comment='Data uploaded')
    user = models.TextField( db_comment='Owner of the upload', null=True, blank=True)
    date = models.DateTimeField( db_comment='Date of the upload', null=True, blank=True)
    status = models.CharField( max_length=1, choices=UPLOAD_RESULTS, null=True, blank=True, db_comment='Status of the upload' )
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'xlsx_upload'
        db_table_comment = 'XLSx Data Uploads'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

class XSLxSheet(models.Model):
    type = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='type', related_name='mapping_type_set', blank=True, null=True)
    name = models.TextField(db_comment='sheet name')
    size = models.IntegerField(db_comment='Sheet columns number')
    first = models.IntegerField(default=1, db_comment='Sheet columns first data row')
    note = models.TextField(db_comment='Sheet description')
    code = models.TextField(db_comment='sheet code', primary_key=True )

    objects = models.Manager().using('soildatastore')
    class Meta:
        managed = True
        ordering = ['type','name']
        unique_together = (('type', 'name'),)
        db_table = 'xlsx_sheet'
        db_table_comment = 'table with xlsx sheet description'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        ) 


class XSLxMapping(models.Model):
    type = models.ForeignKey(Taxonomy, models.SET_NULL, db_column='type', related_name='mapping_type_set', blank=True, null=True)
    sheet = models.TextField(db_comment='sheet name')
    col_order = models.IntegerField(primary_key=True, db_comment='Sheet column order')
    model = models.TextField(db_comment='target class model')
    fieldname = models.TextField(db_comment='target field in the target class model')
    taxonomy = models.TextField(blank=True, null=True, db_comment='taxonomy name')
    note = models.TextField(blank=True, null=True, db_comment='field description')
    field_level = models.TextField(blank=True, null=True, db_comment='upper level field name in the target model')
    value_level = models.IntegerField(blank=True, null=True, db_comment='value for the upper level field')
    paragraph = models.TextField(blank=True, null=True, db_comment='WRB Annex 4 paragraph ')
    section = models.TextField(blank=True, null=True, db_comment='Input Section')
    check = models.TextField(blank=False, null=False, db_comment='Value check and type')
    
    objects = models.Manager().using('soildatastore')
    class Meta:
        managed = True
        ordering = ['type','sheet','col_order']
        unique_together = (('type', 'sheet','col_order'),)
        db_table = 'xlsx_mapping'
        db_table_comment = 'table with the mapping between xlsx sheets and django models'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        ) 

#########################################
## Projects and Data Genealogy
#########################################   
class Project(models.Model):
    code = models.TextField(blank=True, null=True, db_comment='Project identifier ')
    title = models.TextField(blank=True, null=True, db_comment='project name')
    description = models.TextField(blank=True, null=True, db_comment='project description')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'project'
        db_table_comment = 'projects descriptor'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )   
                
class Genealogy(models.Model):
    old_code = models.TextField(blank=True, null=True)
    project_id = models.IntegerField(blank=True, null=True, db_comment='project identifier in the SIS')
    owner_note = models.TextField(blank=True, null=True, db_comment='note about owner ')
    reference = models.TextField(blank=True, null=True, db_comment='reference')
    pub_year = models.IntegerField(blank=True, null=True, db_comment='year of pubblication')
    web_link = models.TextField(blank=True, null=True)
    availability = models.TextField(blank=True, null=True, db_comment='Data availability and/or use restrictions')
    
    objects = models.Manager().using('soildatastore')
    
    class Meta:
        managed = True
        db_table = 'profile_genealogy'
        db_table_comment = 'genealogy of profile data' 
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )                    

#########################################
## General and Surface Data
#########################################   
class LandformTopography(models.Model):
    gradient_upslope = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface upslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    gradient_downslope = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Ground surface downslope inclination with respect to the horizontal plane. If the profile lies on a flat surface, the gradient is 0%. ')
    slope_aspect = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_positive], blank=True, null=True, db_comment='If the profile lies on a slope, report the compass direction that the slope faces, viewed downslope; e.g., 225°')
    slope_shape = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='If the profile lies on a slope, report the slope shape in 2 directions: up-/downslope (perpendicular to the elevation contour, i.e. the vertical curvature) and across slope (along the elevation contour, i.e. the horizontal curvature); e.g., Linear (L), Convex (V) or Concave (C).')
    profile_position = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='If the profile lies in an uneven terrain, report the profile position.')
    landform1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    landform2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    landform1_activity = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    landform2_activity = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    geomorphic_features_description = models.TextField(blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')
    
    class Meta:
        managed = True
        db_table = 'landform_topography'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        # Ensures constraint on model level, raises ValidationError
        if self.slope_shape is not None and self.slope_shape.startswith("p_slope_shape."):
            raise ValidationError({'slope_shape': ('Wrong classification.')})
        if self.profile_position is not None and self.profile_position.startswith("p_profile_position."):
            raise ValidationError({'profile_position': ('Wrong classification.')})
        if self.landform1 is not None and self.landform1.startswith("p_geomorphic_feature_landform."):
            raise ValidationError({'landform1': ('Wrong classification.')})
        if self.landform1_activity is not None and self.landform1_activity.startswith("p_landform_activity."):
            raise ValidationError({'landform1_activity': ('Wrong classification.')})
        if self.landform2 is not None and self.landform2.startswith("p_geomorphic_feature_landform."):
            raise ValidationError({'landform2': ('Wrong classification.')})
        if self.landform2_activity is not None and self.landform2_activity.startswith("p_landform_activity."):
            raise ValidationError({'landform2_activity': ('Wrong classification.')})

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
    
    objects = models.Manager().using('soildatastore')
    
    class Meta:
        managed = True
        db_table = 'cultivated'
        db_table_comment = 'Report up to three actual cultivated species (in the array "actual_species") using the scientific name. If currently under fallow, report the up to 3 last species (in the array "last_species") and indicate month and year of harvest or of cultivation cessation. Insert the species in the sequence of the area covered starting with the species that covers the largest area. Report the up to 3 species that have been cultivated in the last five years in rotation with the actual or last species (1 is the most frequent) in the array column "rotational_species"'
        permissions = (     
            ('access_soildata', 'view_soildata', 'vrite_soildata'),
        )

    def clean(self):
        # Ensures constraint on model level, raises ValidationError
            if self.cultivation_cessation is not None and ( self.last_species1 is None or self.actual_species1 is not None ):
                raise ValidationError({'cultivation_cessation': ('cultivation_cessation error no dominant last specie present or actual dominant specie.')})
            if self.last_species1 is not None and ( self.cultivation_cessation is None or self.actual_species1 is not None ):
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

class LandUse(models.Model):
    land_use = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  blank=True, null=True)
    corine = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  blank=True, null=True)
    cultivated =  models.OneToOneField(Cultivated, on_delete=models.SET_DEFAULT, default=None, db_comment='Cultivated Section')
    #not_cultivated_landuse_set from ProfileNotCultivated
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'land_use'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.land_use is not None and self.land_use.startswith("p_land_use."):
            raise ValidationError({'land_use': ('Wrong classification.')})
        if self.corine is not None and self.corine.startswith("p_corine."):              
            raise ValidationError({'Corine': ('Wrong classification.')})
           
class NotCultivated(models.Model):
    STRATA_TYPES = [
        ("0" , "Ground stratum"),
        ("1" , "Upper stratum"),
        ("2" , "Mid stratum"),
    ]
    
    landuse = models.ForeignKey(LandUse, on_delete=models.CASCADE, related_name='not_cultivated_landuse_set')
    dominant_vegetation_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    second_vegetation_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    third_vegetation_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    vegetation_average_height = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    vegetation_maximum_height = models.DecimalField(max_digits=12, decimal_places=5, blank=True, null=True)
    vegetation_strata = models.CharField( max_length=1,  choices=STRATA_TYPES)
    vegetation_cover_by_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    species1 = models.TextField(blank=True, null=True)
    species2 = models.TextField(blank=True, null=True)
    species3 = models.TextField(blank=True, null=True)

    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        unique_together = (('landuse', 'vegetation_strata'),)
        db_table = 'not_cultivated'
        db_table_comment = 'For each profile, compile as many rows as the vegetation strata (STRATA_TYPES) are. Report the average height and the maximum height in m above ground for each stratum separately. Report the vegetation cover. For the upper stratum and the mid-stratum, report the percentage (by area) of the crown cover. For the ground stratum, report the percentage (by area) of the ground cover. Report up to three important species per stratum, e.g., Fagus orientalis. If you do not know the species, report the next higher taxonomic rank. The (maximum 3) species must be insert in the array column species.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
        
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

class CoarseFragments(models.Model):
    total_area_covered = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    class1_size = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,   blank=True, null=True)
    class2_size = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,   blank=True, null=True)
    class3_size = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,   blank=True, null=True)
    class1_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    class2_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    class3_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')
    
    class Meta:
        managed = True
        db_table = 'coarse_fragments'
        db_table_comment = 'Report the total percentage of the area that is covered by coarse surface fragments. In addition, report at least one and up to three size classes and report the percentage of the area that is covered by the coarse surface fragments of the respective size class, the dominant one first.\r\nClasses size are in p_coarse_size'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.class1_size is not None and self.class1_size.startswith("p_coarse_size."):
                raise ValidationError({'class1_size': ('Wrong classification.')})
        if self.class2_size is not None and self.class2_size.startswith("p_coarse_size."):
                raise ValidationError({'class2_size': ('Wrong classification.')})
        if self.class3_size is not None and self.class3_size.startswith("p_coarse_size."):
                raise ValidationError({'class3_size': ('Wrong classification.')})

class LitterLayer(models.Model):
    average_thickness = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    area_covered = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    maximum_thickness = models.DecimalField(max_digits=12, decimal_places=6, validators=[validate_positive], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'litter_layer'
        db_table_comment = 'Observe an area of 5 m x 5 m with the profile at its centre. Report the average and the maximum thickness of the litter layer in cm. If there is no litter layer, report 0 cm as thickness.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )          

class SurfaceUnevenness(models.Model):
    position = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    natural_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    natural_average_height_difference = models.DecimalField(db_column='natural_avg_height_diff', max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    natural_average_elevated_areas_diameter = models.DecimalField(db_column='natural_avg_elev_areas_diameter', max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    natural_average_distance_max_height = models.DecimalField(db_column='natural_avg_dist_max_height', max_digits=20, decimal_places=8, validators=[validate_positive], blank=True, null=True)
    human_made_type_1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    human_made_type_2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    human_made_terrace_average_height = models.DecimalField(db_column='human_average_height', max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    human_made_no_terrace_average_height_difference = models.DecimalField( db_column='human_average_height_diff', max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    human_made_no_terrace_average_width = models.DecimalField(db_column='human_average_width', max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    human_made_no_terrace_average_max_depth_height = models.DecimalField(db_column='human_average_max_depth', max_digits=12, decimal_places=3, validators=[validate_positive], blank=True, null=True)
    erosion_area_affected = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    erosion_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,blank=True, null=True)
    erosion_degree = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    erosion_activity = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'surface_unevenness'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
        
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

class SurfaceCracks(models.Model):
    dominant_width_class = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilesurfacecracks_dominant_width_class_set', blank=True, null=True)
    dominant_distance_between_cracks = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilesurfacecracks_dominant_distance_between_cracks_set', blank=True, null=True)
    dominant_spatial_arrangement = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profilesurfacecracks_dominant_spatial_arrangement_set', blank=True, null=True)
    dominant_persistence = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilesurfacecracks_dominant_persistence_set', blank=True, null=True)
    secondary_width_class = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilesurfacecracks_secondary_width_class_set', blank=True, null=True)
    secondary_distance_between_cracks = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilesurfacecracks_secondary_distance_between_cracks_set', blank=True, null=True)
    secondary_spatial_arrangement = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,  related_name='profilesurfacecracks_secondary_spatial_arrangement_set', blank=True, null=True)
    secondary_persistence = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilesurfacecracks_secondary_persistence_set', blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'surface_cracks'
        db_table_comment = 'For each profile, compile as many rows as the width classes are. If surface cracks are present, report the average width of the cracks. If the soil surface between cracks of larger width classes is regularly divided by cracks of smaller width classes, report the two width classes.'
        objects = models.Manager().using('soildatastore')
        
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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
    
    surface_cracks =  models.OneToOneField(SurfaceCracks, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Surface Cracks')
    litter_layer =  models.OneToOneField(LitterLayer, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Litter layer')
    coarse_fragments =  models.OneToOneField(CoarseFragments, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Coarse fragments')
    surface_unevenness =  models.OneToOneField(SurfaceUnevenness, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Water Surface Unevenness')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'surface'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.patterned_ground_form is not None and self.patterned_ground_form.startswith("p_patterned_ground_form."):
            raise ValidationError({'patterned_ground_form': ('Wrong classification.')})
        if self.technical_surface_alteration is not None and self.technical_surface_alteration.startswith("p_technical_surface_alteration."):
            raise ValidationError({'alteration': ('Wrong classification.')})
        if self.bedrock_lithology is not None and self.bedrock_lithology.startswith("l_p_parent_material."):
            raise ValidationError({'bedrock_lithology': ('Wrong classification.')})
        if self.water_above_surface is not None and self.water_above_surface.startswith("p_water_above_surface."):
            raise ValidationError({'water_above_surface': ('Wrong classification.')})
        if self.water_drainage_condition is not None and self.water_drainage_condition.startswith("p_drainage_condition."):
            raise ValidationError({'water_drainage_condition': ('Wrong classification.')})
        if self.water_repellence_type is not None and self.water_repellence_type.startswith("p_water_repellence."):
            raise ValidationError({'water_repellence_type': ('Wrong classification.')})

class ClimateAndWeather(models.Model):
    climate_koppen = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='climate_koppen', related_name='profileclimateweather_climate_koppen_set', blank=True, null=True)
    ecozone_shultz = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='ecozone_shultz', related_name='profileclimateweather_ecozone_shultz_set', blank=True, null=True)
    season = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='season', related_name='profileclimateweather_season_set', blank=True, null=True)
    current_weather = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='current_weather', related_name='profileclimateweather_current_weather_set', blank=True, null=True)
    past_weather = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='past_weather', related_name='profileclimateweather_past_weather_set', blank=True, null=True)
    soil_temp_regime = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='soil_temp_regime', related_name='profileclimateweather_soil_temp_regime_set', blank=True, null=True)
    soil_moist_regime = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, db_column='soil_moist_regime', related_name='profileclimateweather_soil_moist_regime_set', blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')
    
    class Meta:
        managed = True
        db_table = 'climate_weather'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
    def clean(self):
        if self.climate_koppen is not None and self.climate_koppen.startswith("p_climate_koppen."):
            raise ValidationError({'climate_koppen': ('Wrong classification.')})
        if self.ecozone_shultz is not None and self.ecozone_shultz.startswith("p_ecozone_shultz."):
            raise ValidationError({'ecozone_shultz': ('Wrong classification.')})
        if self.season is not None and self.season.startswith("p_season_of_description."):
            raise ValidationError({'season': ('Wrong classification.')})
        if self.current_weather is not None and self.current_weather.startswith("p_current_weather."):
            raise ValidationError({'current_weather': ('Wrong classification.')})
        if self.past_weather is not None and self.past_weather.startswith("p_past_weather."):
            raise ValidationError({'past_weather': ('Wrong classification.')})
        if self.soil_temp_regime is not None and self.soil_temp_regime.startswith("p_soil_temp_regime."):
            raise ValidationError({'soil_temp_regime': ('Wrong classification.')})
        if self.soil_moist_regime is not None and self.soil_moist_regime.startswith("p_soil_moist_regime."):
            raise ValidationError({'soil_moist_regime': ('Wrong classification.')})

  
#########################################
## Layer Data
#########################################
class LayerRemnants(models.Model):
    total_abundance = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cementing_agent1 = models.ForeignKey(Taxonomy, models.SET_NULL,  blank=True, null=True)
    cementing_agent2 = models.ForeignKey(Taxonomy, models.SET_NULL,  blank=True, null=True)
    size_agent1 = models.ForeignKey(Taxonomy, models.SET_NULL,  blank=True, null=True)
    size_agent2 = models.ForeignKey(Taxonomy, models.SET_NULL,  blank=True, null=True)
    abundance_agent1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance_agent2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_remnants'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.cementing_agent1 is not None and self.cementing_agent1.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agent1': ('Wrong classification.')})
        if self.cementing_agent2 is not None and self.cementing_agent2.startswith("l_cementing_agent."):
            raise ValidationError({'cementing_agent2': ('Wrong classification.')})    
        if self.size_agent1 is not None and self.size_agent1.startswith("l_size_shape."):
            raise ValidationError({'size_agent1': ('Wrong classification.')})
        if self.size_agent2 is not None and self.size_agent2.startswith("l_size_shape."):
            raise ValidationError({'size_agent2': ('Wrong classification.')})

class LayerCoarseFragments(models.Model):
    total_abundance = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage], db_comment='coars fragments total abbundance by volume in percentage')
    free_pore = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Between coarse fragments, large pores may exist that are visible with the naked eye and do not contain soil material. Report the total percentage (by volume, related to the whole soil).')
    #layer_coarse_fragments_lithology_set from LayerCoarseFragmentLithology
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_coarse_fragments'
        db_table_comment = 'Coarse fragments. A coarse fragment is a mineral particle, derived from the parent material, > 2 mm in its equivalent diameter'

class LayerCoarseFragmentsLithology(models.Model):
    coarse_fragments = models.ForeignKey(LayerCoarseFragments, on_delete=models.CASCADE, related_name='coarse_fragments_lithology_coarse_fragments_set', db_comment='LayerCoarseFragmentsLithologies' )
    lithology_nr = models.IntegerField()
    lithology_type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,blank=True, null=True)
    size_class1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_class2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_class3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_class4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    weathering_class1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    weathering_class2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    weathering_class3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    weathering_class4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class1.')
    abundance2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class2.')
    abundance3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class3.')
    abundance4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage], db_comment='Report the total percentage of the volume occupied by coarse fragments for class4.')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_coarse_fragment_lithology'
        unique_together = (('coarse_fragments', 'lithology_nr',),)
        db_table_comment = 'Coarse fragments Lithology.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
          
class LayerArtefacts(models.Model):
    total_abundance = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    black_carbon = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    type1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    type2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    type3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    type4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    type5 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_type1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_type2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_type3 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_type4 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_type5 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    abundance_type1 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance_type2 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance_type3 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance_type4 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    abundance_type5 = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_artefacts'
        db_table_comment = 'Artefacts are solid or liquid substances that are: created or substantially modified by humans as part of an industrial or artisanal manufacturing process, or brought to the surface by human activity from a depth, where they were not influenced by surface processes, and deposited in an environment, where they do not commonly occur.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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

class LayerStructure(models.Model):
    wedge_shaped = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Wedge-shaped aggregates tilted between ≥ 10° and ≤ 60° from the horizontal: abundance, by volume [%]')
    #layer_structure_types_structure_set from LayerStructureTypes
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_structure'
        db_table_comment = 'Layer Structure'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

class LayerStructureTypes(models.Model):
    LEVEL_TYPES = [
        ("1" , "First level structure Type 1"),
        ("2" , "First level structure Type 2"),
        ("3" , "First level structure Type 3"),
        ("4" , "Second level structure Type 1.1"),
        ("5" , "Second level structure Type 1.2"),
        ("6" , "Second level structure Type 2.1"),
        ("7" , "Second level structure Type 2.2"),
        ("8" , "Second level structure Type 3.1"),
        ("9" , "Second level structure Type 3.2"),
        ("A" , "Third-level structure Type 1.1.1"),
        ("B" , "Third-level structure Type 1.2.1"),
        ("C" , "Third-level structure Type 2.1.1"),
        ("D" , "Third-level structure Type 2.2.1"),
        ("E" , "Third-level structure Type 3.1.1"),
        ("F" , "Third-level structure Type 3.2.1"),
    ]
    
    structure = models.ForeignKey(LayerStructure, on_delete=models.CASCADE, related_name='layer_structure_types_structure_set', db_comment='LayerStructure' )
    level_type = models.CharField(max_length=1, choices=LEVEL_TYPES)
    type = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    grade = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    penetrability = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_class1 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    size_class2 = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    abundance_vol = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance_class1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance_class2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_structure_types'
        unique_together = (('structure', 'level_type'),)
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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

class LayerCracks(models.Model):
    persistence = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layercracks_persistence_set', blank=True, null=True)
    continuity = models.ForeignKey(Taxonomy, models.SET_NULL,  related_name='layercracks_continuity_set', blank=True, null=True)
    average_width = models.DecimalField(max_digits=16, decimal_places=2, validators=[validate_positive], blank=True, null=True)
    abundance_cracks = models.PositiveIntegerField(blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_cracks'
        db_table_comment = 'Report persistence and continuity'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.persistence is not None and self.persistence.startswith("l_cracks_persistence."):
            raise ValidationError({'persistence': ('Wrong classification.')})
        if self.continuity is not None and self.continuity.startswith("l_cracks_continuity."):
            raise ValidationError({'continuity': ('Wrong classification.')})

class LayerStressFeatures(models.Model):
    pressure_faces = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Pressure faces in % of the surfaces of soil aggregates')
    slickensides = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Slickensides in % of the surfaces of soil aggregates.')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_stress_features'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
        db_table_comment = 'Stress features result from soil aggregates that are pressed against each other due to swelling clays. The aggregate surfaces may be shiny. There are two types: Pressure faces do not slide past each other and have no striations, slickensides slide past each other and have striations.'

class LayerMatrixColours(models.Model):
    munsell_moist_dominat = models.TextField(blank=True, null=True)
    munsell_dry_dominat = models.TextField(blank=True, null=True)
    exposed_area_dominat = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    munsell_moist_2 = models.TextField(blank=True, null=True)
    munsell_dry_2 = models.TextField(blank=True, null=True)
    exposed_area_2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    munsell_moist_3 = models.TextField(blank=True, null=True)
    munsell_dry_3 = models.TextField(blank=True, null=True)
    exposed_area_3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_matrix_colour'
        db_table_comment = 'Report the colour of the soil matrix. If there is more than one matrix colour, report up to three, the dominant one first, and give the percentage of the exposed area'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

class LayerTextureColour(models.Model):
    coarser_textured = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by coarser-textured parts of any orientation (vertical, horizontal, inclined) having a width of ≥ 0.5 cm')
    vertical_tongues = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='the percentage (by exposed area) occupied by continuous vertical tongues of coarser-textured parts with a horizontal extension of ≥ 1 cm (if these tongues are absent, report 0%)')
    depth_range = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='the depth range in cm, where these tongues cover ≥ 10% of the exposed area (if they extend across several layers, the length is only reported in the description of that layer, where they start at the layer’s upper limit).')
    horizontal_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='In the middle of the layer, prepare a horizontal surface, 50 cm x 50 cm, and report the percentage (by horizontal area covered) of the coarser-textured parts.')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_texture_colour'
        db_table_comment = 'If a layer consists of darker-coloured finer-textured and lighter-coloured coarser-textured parts that do not form horizontal layers but can easily be distinguished, describe them separately'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

class LayerLithogenicVariegates(models.Model): 
    munsell_moist_dominant = models.TextField(blank=True, null=True)
    size_class_dominant = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    exposed_area_dominant = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_moist2 = models.TextField(blank=True, null=True)
    size_class2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    exposed_area2 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    munsell_moist3 = models.TextField(blank=True, null=True)
    size_class3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    exposed_area3 = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage],  blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_lithogenic_variegates'
        db_table_comment = 'Report colour, size class, and abundance. If more than one colour occurs, report up to three, the dominant one first, and give size class and abundance for each colour separately.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        # Ensures constraint on model level, raises ValidationError  
        if self.size_class is not None and self.size_class.startswith("l_lithogenic_size."):
            raise ValidationError({'size_class': ('Wrong classification.')}) 

class LayerRedoximorphicFeatures(models.Model):
    oximorphic_inner = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    oximorphic_outer = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    oximorphic_random = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    reductimorphic_inner = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    reductimorphic_outer = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    reductimorphic_random = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cemented_oximorphic = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of cemented oximorphic features, by volume [%]')
    abundance_cemented_oximorphic_features = models.DecimalField(max_digits=12, decimal_places=4, validators=[validate_percentage], db_comment='Abundance of cemented oximorphic features, by volume [%]')
    
    #redoximorphic_colour_redoximorphic_features_set from LayerRedoximorphicColour
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_coarse_fragments'
        db_table_comment = 'Coarse fragments. A coarse fragment is a mineral particle, derived from the parent material, > 2 mm in its equivalent diameter'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

class LayerRedoximorphicColour(models.Model):
    COLOUR_NUMBERS = [
        ("1" , "Colour 1 - Dominant"),
        ("2" , "Colour 2"),
        ("3" , "Colour 3"),
    ]
    features = models.ForeignKey(LayerRedoximorphicFeatures, on_delete=models.CASCADE, related_name='redoximorphic_colour_redoximorphic_features_set', db_comment='LayerRedoximorphicFeatures')  
    colour_nr = models.CharField(max_length=1, choices=COLOUR_NUMBERS)
    munsell_moist = models.TextField(blank=True, null=True)
    munsell_dry = models.TextField(blank=True, null=True)
    substance = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    size_class1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    size_class2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    mottles_contrast = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    mottles_boundary = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    cementation_class = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    exposed_area = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_redoximorphic_colour'
        unique_together = (('layer', 'colour_nr'),)
        db_table_comment = 'Report the colour according to the Munsell Color Charts'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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

class LayerColours(models.Model):
    matrix_colours = models.OneToOneField(LayerMatrixColours, on_delete=models.SET_DEFAULT, default=None, db_comment='Matrix colour')   
    texture_colour = models.OneToOneField(LayerTextureColour, on_delete=models.SET_DEFAULT, default=None, db_comment='Combinations of darker-coloured finer-textured and lighter-coloured coarser-textured parts')
    lithogenic_variegates = models.OneToOneField(LayerLithogenicVariegates, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerLithogenicVariegates')
    redoximorphic_features = models.OneToOneField(LayerRedoximorphicFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRedoximorphicFeatures')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_colours'
        db_table_comment = 'Layer Coloured Features'    
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

class LayerCoatingsBridges(models.Model):
    clay_coatings = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay coatings in percentage')
    form_coatings = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='refer to clay coatings')
    organic_coatings = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Organic matter coatings and oxide coatings on sand and/or coarse silt grains')
    cracked_coatings = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of cracked coatings in percentage')
    clay_bridges = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of clay bridges in percentage')
    form_bridge = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='refer to clay bridge')
    form_organic = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='refer to organic matter coatings and oxide coatings (report only if matrix colour value ≤ 3)')
    sand_silt = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Abundance of uncoated sand and coarse silt grains in percentage')
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_coatings_bridges'
        db_table_comment = 'Report the abundance of clay coatings in % of the surfaces of soil aggregates, coarse fragments and/or biopore walls clay bridges between sand grains in % of involved sand grains.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.form_coatings is not None and self.form_coatings.startswith("l_form_coatings."):
                    raise ValidationError({'form_coatings': ('Wrong classification.')})
            if self.form_bridge is not None and self.form_bridge.startswith("l_form_coatings."):
                    raise ValidationError({'form_bridge': ('Wrong classification.')})
            if self.organic_coatings is not None and self.organic_coatings.startswith("l_organic_coatings."):
                    raise ValidationError({'organic_coatings': ('Wrong classification.')})
            if self.form_organic is not None and self.form_organic.startswith("l_form_coatings."):
                    raise ValidationError({'form_organic': ('Wrong classification.')})

class LayerRibbonlikeAccumulations(models.Model):
    substances = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    combined_thickness = models.DecimalField(max_digits=40, decimal_places=20, validators=[validate_positive], blank=True, null=True, db_comment='If there are 2 or more ribbon-like accumulations in one layer, report the number of the accumulations and their combined thickness in cm')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_ribbonlike_accumulations'
        db_table_comment = 'Ribbon-like accumulations are thin, horizontally continuous accumulations within the matrix of another layer. Report the accumulated substance(s).'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.substances is not None and self.substances.startswith("l_ribbonlike_substances."):
            raise ValidationError({'substances': ('Wrong classification.')})

class LayerCarbonates(models.Model):
    matrix_content = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    matrix_content_retarded_reaction = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_type1 = models.ForeignKey(Taxonomy, models.SET_NULL,blank=True, null=True)
    secondary_type2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_type3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_type4 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_size1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_size2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_size3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_size4 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_shape1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_shape2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_shape3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_shape4 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    secondary_abundance_type1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    secondary_abundance_type2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    secondary_abundance_type3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    secondary_abundance_type4 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_carbonates'
        db_table_comment = 'Layer Carbonates'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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
                       
class LayerGypsum(models.Model):
    content = models.ForeignKey(Taxonomy, models.SET_NULL,blank=True, null=True)
    secondary_gypsum = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    sgypsum_type1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    sgypsum_type2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type1_size = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type2_size = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type1_shape = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type2_shape = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_gypsum'
        db_table_comment = 'Report the gypsum content in the soil matrix. If readily soluble salts are absent or present in small amounts only, gypsum can be estimated by measuring the electrical conductivity in soil suspensions of different soil-water relations after 30 minutes (in the case of fine-grained gypsum). This method detects primary and secondary gypsum. Note: Higher gypsum contents may be differentiated by abundance of H2O-soluble pseudomycelia/crystals and a soil colour with high value and low chroma'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.sgypsum_type1 is not None and self.sgypsum_type1.startswith("l_sgypsum_type."):
                    raise ValidationError({'sgypsum_type1': ('Wrong classification.')})
            if self.type1_size is not None and self.type1_size.startswith("l_mineral_size."):
                    raise ValidationError({'type1_size': ('Wrong classification.')})
            if self.type1_shape is not None and self.type1_shape.startswith("l_mineral_shape."):
                    raise ValidationError({'type1_shape': ('Wrong classification.')})

class LayerSecondarySilica(models.Model):
    type1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Report the type of secondary silica, type1 is dominant')
    type2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Report the type of secondary silica')
    type1_dnfcsize = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type1')
    type2_dnfcsize = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a layer that has been cemented by secondary silica, report their size class for type2')
    abundance = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Report the total percentage (by exposed area) of secondary silica')
    abundance_dnfc = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='If a layer shows durinodes and/or remnants of a cemented layer, report in addition the percentage (by volume) of those durinodes and remnants that have a diameter ≥ 1 cm')
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_secondary_silica'
        db_table_comment = 'Secondary silica (SiO2) is off-white and predominantly consisting of opal and microcrystalline forms. It occurs as laminar caps, lenses, (partly) filled interstices, bridges between sand grains, and as coatings at surfaces of soil aggregates, biopore walls, coarse fragments, and remnants of broken-up cemented layers. Report the type of secondary silica. If more than one type occurs, report up to two, the dominant one first.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.type1 is not None and self.type1.startswith("l_ssilica_types."):
                raise ValidationError({'type1': ('Wrong classification.')})
            if self.type2 is not None and self.type2.startswith("l_ssilica_types."):
                raise ValidationError({'type2': ('Wrong classification.')})
            if self.type1_dnfcsize is not None and self.type1_dnfcsize.startswith("l_dnfc_size."):
                raise ValidationError({'type1_dnfcsize': ('Wrong classification.')})
            if self.type2_dnfcsize is not None and self.type2_dnfcsize.startswith("l_dnfc_size."):
                raise ValidationError({'type2_dnfcsize': ('Wrong classification.')})
            
class LayerConsistence(models.Model):
    cementation = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Report the percentage (by volume, related to the whole soil) of the layer that is cemented.')
    cementing_agents1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Report the cementing agents')
    cementing_agents2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    cementing_agents3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    cementation_class = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    rrclass_moist = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Rupture resistance, non-cemented soil moist')
    rrclass_dry = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Rupture resistance, non-cemented soil dry')
    susceptibility = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Some layers are prone to cementation after repeated drying and wetting. Report the susceptibility')
    manner_failure = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Report the manner of failure (brittleness)')
    plasticity = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='Plasticity is the degree to which reworked soil can be permanently deformed without rupturing')
    penetration_resistance = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    stickiness = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_consistence'
        db_table_comment = 'Consistence is the degree and kind of cohesion and adhesion that soil exhibits. Consistence is reported separately for cemented and non-cemented (parts of) layers. If a specimen of soil does not fall into pieces by applying low forces, one has to check, whether it is cemented'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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

class LayerSurfaceCrusts(models.Model):
    sealing_agent1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    sealing_agent2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    sealing_agent3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    average_thickness = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_surface_crusts'
        db_table_comment = 'A crust is a thin layer of soil constituents bound together into a horizontal mat or into small polygonal plates (see Schoeneberger et al., 2012). Soil crusts develop in the first mineral layer(s) and are formed by a sealing agent of physical, chemical and/or biological origin.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.sealing_agent1 is not None and self.sealing_agent1.startswith("l_sealing_agent."):
                raise ValidationError({'sealing_agent1': ('Wrong classification.')})
            if self.sealing_agent2 is not None and self.sealing_agent2.startswith("l_sealing_agent."):
                raise ValidationError({'sealing_agent2': ('Wrong classification.')})
            if self.sealing_agent3 is not None and self.sealing_agent3.startswith("l_sealing_agent."):
                raise ValidationError({'sealing_agent3': ('Wrong classification.')})

class LayerPermafrostFeatures(models.Model):
    cryogenic_alteration1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_cryogenic_alteration1_set', blank=True, null=True)
    cryogenic_alteration2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_cryogenic_alteration2_set', blank=True, null=True)
    cryogenic_alteration3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_cryogenic_alteration3_set', blank=True, null=True)
    layers_permafrost = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerpermafrostfeatures_layers_permafrost_set', blank=True, null=True)
    cryogenic_abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cryogenic_abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    cryogenic_abundance3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_permafrost_features'
        db_table_comment = 'Estimate the total percentage (by exposed area, related to the whole soil) affected by cryogenic alteration. Report up to three features, the dominant one first, and report the percentage for each feature separately.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.cryogenic_alteration1 is not None and self.cryogenic_alteration1.startswith("l_cryogenic_alteration."):
                    raise ValidationError({'cryogenic_alteration1': ('Wrong classification.')})
            if self.cryogenic_alteration2 is not None and self.cryogenic_alteration2.startswith("l_cryogenic_alteration."):
                    raise ValidationError({'cryogenic_alteration2': ('Wrong classification.')})
            if self.cryogenic_alteration3 is not None and self.cryogenic_alteration3.startswith("l_cryogenic_alteration."):
                    raise ValidationError({'cryogenic_alteration3': ('Wrong classification.')})
            if self.layers_permafrost is not None and self.layers_permafrost.startswith("l_layers_permafrost."):
                    raise ValidationError({'layers_permafrost': ('Wrong classification.')})

class LayerOrganicCarbon(models.Model):
    content_min = models.DecimalField(max_digits=40, decimal_places=10, blank=True, null=True)
    content_max = models.DecimalField(max_digits=40, decimal_places=10, blank=True, null=True)
    natural_accumulations1 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerorganiccarbon_natural_accumulations1_set', blank=True, null=True)
    natural_accumulations2 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerorganiccarbon_natural_accumulations2_set', blank=True, null=True)
    natural_accumulations3 = models.ForeignKey(Taxonomy, models.SET_NULL, related_name='layerorganiccarbon_natural_accumulations3_set', blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    black_carbon = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_organic_carbon'
        db_table_comment = 'Report the estimated organic carbon content. It is based on the Munsell value, moist, and the texture'

        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.natural_accumulations1 is not None and self.natural_accumulations1.startswith("l_accumulation."):
                    raise ValidationError({'natural_accumulations1': ('Wrong classification.')})
            if self.natural_accumulations2 is not None and self.natural_accumulations2.startswith("l_accumulation."):
                    raise ValidationError({'natural_accumulations2': ('Wrong classification.')})
            if self.natural_accumulations3 is not None and self.natural_accumulations3.startswith("l_accumulation."):
                    raise ValidationError({'natural_accumulations3': ('Wrong classification.')})
            
class LayerRoots(models.Model):
    abundance_less2mm = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='diameter <= 2mm')
    abundance_less05mm = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='diameter < 0,5mm')
    abundance_05to2mm = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='diameter from 0.5 to 2 mm')
    abundance_greater2mm = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='diameter > 2mm')
    abundance_2to5mm = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='diameter from 2 to 5 mm')
    abundance_greater5mm = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True, db_comment='diameter > 5mm')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_roots'
        db_table_comment = 'Count the number of roots per dm2, separately for the six diameter classes, and report the abundance classes'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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
    
class LayerAnimalActivity(models.Model):
    type1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type4 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type5 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    mammal_activity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    bird_activity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    worm_activity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    insect_activity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    unspecified_activity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_animal_activity'
        db_table_comment = 'Report the animal activity that has visibly changed the features of the layer. If applicable, report up to 5 types, the dominant one first. Report the percentage (by exposed area), separately for mammal activity, bird activity, worm activity, insect activity and unspecified activity'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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
 
class LayerHumanAlterations(models.Model):
    natural_material1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    natural_material2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    natural_material3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance3 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    texture_class = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    carbonate_content = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    carbon_content = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    alteration1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    alteration2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    aggregate_formation = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_human_alterations'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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

class LayerDegreeDecomposition(models.Model):
    visible_plant = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[validate_percentage])
    subdivision_horizon = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    plant_residue1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    plant_residue2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    abundance1 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    abundance2 = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_degree_decomposition'
        db_table_comment = 'Refer to the transformation of visible plant tissues into visibly homogeneous organic matter.'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
            if self.subdivision_horizon is not None and self.subdivision_horizon.startswith("l_subdivision_horizon."):
                    raise ValidationError({'subdivision_horizon': ('Wrong classification.')})
            if self.plant_residue1 is not None and self.plant_residue1.startswith("l_dead_plant."):
                    raise ValidationError({'plant_residue1': ('Wrong classification.')})
            if self.plant_residue2 is not None and self.plant_residue2.startswith("l_dead_plant."):
                    raise ValidationError({'plant_residue2': ('Wrong classification.')})   

class LayerNonMatrixPore(models.Model):
    type1 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type1_dominant_size = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type1_abundance = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type2 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type2_dominant_size = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type2_abundance = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type3 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type3_dominant_size = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type3_abundance = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type4 = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type4_dominant_size = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    type4_abundance = models.ForeignKey(Taxonomy, models.SET_NULL, blank=True, null=True)
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer_nonmatrix_pore'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

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

#########################################
## Sample Layer
#########################################
class SampleLayer(models.Model):
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm')
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm')
    homogeneity_part = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    homogeneity_alluvial_tephra = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    water_saturation = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Types of water saturation')
    water_status = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Soil water status')
    organicmineral = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    boundaries_distinctness = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundaries_shape = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    wind_disposition = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Wind deposition')
    texture_class = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Texture class') 
    texture_subclass = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Texture subclass')
    rh_value = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Rh Value')
    initial_weathering = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage], db_comment='Initial weathering abundance')
    soluble_salts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    field_ph_misured_value = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    field_ph_solution = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    continuity_volume_fractures = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    continuity_average_fractures = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    volcanic_glasses_abundance = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,blank=True, null=True)
    volcanic_glasses_thixotropy_naf = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    bulk_density = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    packing_density = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_material = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    note = models.TextField(blank=True, null=True)
    
    remnants = models.OneToOneField(LayerRemnants, on_delete=models.SET_DEFAULT, default=None, db_comment='Remnants of broken-up cemented layers')
    coarse_fragments = models.OneToOneField(LayerCoarseFragments, on_delete=models.SET_DEFAULT, default=None, db_comment='Coarse fragments')
    artefacts = models.OneToOneField(LayerArtefacts, on_delete=models.SET_DEFAULT, default=None, db_comment='Artefacts')
    structure = models.OneToOneField(LayerStructure, on_delete=models.SET_DEFAULT, default=None, db_comment='Structure')
    cracks = models.OneToOneField(LayerCracks, on_delete=models.SET_DEFAULT, default=None, db_comment='Cracks')
    stress_features = models.OneToOneField(LayerStressFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='Stress Features')
    colours = models.OneToOneField(LayerColours, on_delete=models.SET_DEFAULT, default=None, db_comment='Section Colours')
    coatings_bridges = models.OneToOneField(LayerCoatingsBridges, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerCoatingsBridges')
    ribbonlike_accumulations = models.OneToOneField(LayerRibbonlikeAccumulations, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRibbonlikeAccumulations')
    carbonates = models.OneToOneField(LayerCarbonates, on_delete=models.SET_DEFAULT, default=None, db_comment='Section Layer Carbonates')
    gypsum = models.OneToOneField(LayerGypsum, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerGypsum')
    secondary_silicia = models.OneToOneField(LayerSecondarySilica, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerSecondarySilica')
    consistence = models.OneToOneField(LayerConsistence, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerConsistence')
    surface_crusts = models.OneToOneField(LayerSurfaceCrusts, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerSurfaceCrusts')   
    permafrost_features =  models.OneToOneField(LayerPermafrostFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerPermafrostFeatures')   
    organic_carbon =  models.OneToOneField(LayerOrganicCarbon, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerOrganicCarbon')   
    roots =  models.OneToOneField(LayerRoots, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRoots')   
    animal_activity  =  models.OneToOneField(LayerAnimalActivity, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerAnimalActivity')   
    human_alteration =  models.OneToOneField(LayerHumanAlterations, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerHumanAlterations')   
    degree_decomposition =  models.OneToOneField(LayerDegreeDecomposition, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerDegreeDecomposition')   
    non_matrix_pore = models.OneToOneField(LayerNonMatrixPore, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerNonMatrixPore')   
    
    #sample_labdata_sample_layer_set from SampleLabData

    def _get_thickness(self):
        "Returns the thickness"
        return self.lower - self.upper
    thickness = property(_get_thickness)   
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'sample_layer'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
        
    def clean(self):
        # Ensures constraint on model level, raises ValidationError
        if self.upper < self.lower:
            raise ValidationError({'upper': ('lower cannot be smaller then upper.')}) 
        if self.water_saturation is not None and self.water_saturation.startswith("l_water_saturation"):
            raise ValidationError({'water_type': ('Wrong classification.')})
        if self.water_status is not None and self.water_status.startswith("l_water_status"):
            raise ValidationError({'water_status': ('Wrong classification.')}) 
        if self.homogeneity_alluvial_tephra is not None and self.homogeneity_alluvial_tephra.startswith("l_alluvial_tephra."):
            raise ValidationError({'homogeneity_alluvial_tephra': ('Wrong classification.')})
        if self.boundaries_distinctness is not None and self.boundaries_distinctness.startswith("l_boundaries."):
            raise ValidationError({'boundaries_distinctness': ('Wrong classification.')})
        if self.boundaries_shape is not None and self.boundaries_shape.startswith("l_shape."):
            raise ValidationError({'boundaries_shape': ('Wrong classification.')})
        if self.organicmineral is not None and self.organicmineral.startswith("l_organic_mineral"):
            raise ValidationError({'organicmineral': ('Wrong classification.')}) 
        if self.wind_disposition is not None and self.wind_disposition.startswith("l_wind"):
            raise ValidationError({'wind_disposition': ('Wrong classification.')}) 
        if self.texture_class is not None and self.texture_class.startswith("l_texture_classes"):
            raise ValidationError({'texture_class': ('Wrong classification.')}) 
        if self.texture_subclass is not None and self.texture_subclass.startswith("l_texture_subclasses"):
            raise ValidationError({'texture_subclass': ('Wrong classification.')}) 
        if self.rh_value is not None and self.rh_value.startswith("l_rh_value"):
            raise ValidationError({'rh_value': ('Wrong classification.')}) 
        if self.field_ph_solution is not None and self.field_ph_solution.startswith("l_potenziometric_measure"):
            raise ValidationError({'field_ph_solution': ('Wrong classification.')}) 
        if self.packing_density is not None and self.packing_density.startswith("l_packing_density"):
            raise ValidationError({'packing_density': ('Wrong classification.')}) 
        if self.parent_material is not None and self.parent_material.startswith("l_type_parent_material"):
            raise ValidationError({'parent_material': ('Wrong classification.')})  

#########################################
## Sample General
#########################################     
class SampleGeneral(models.Model):
    code = models.TextField(unique=True, db_comment='profile identifier')
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
    layer =  models.OneToOneField(SampleLayer, on_delete=models.SET_DEFAULT, default=None, db_comment='Layer of the Sample')
    
    ## Genealogy section
    project = models.ForeignKey(Project, models.SET_NULL, blank=True, null=True, related_name='profile_project_set', db_comment='Survey/Project identifier')
    genealogy =  models.OneToOneField(Genealogy, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Genealogy')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'sample_general'
        db_table_comment = 'The Soil Sample main table'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.survey_method is not None and self.survey_method.startswith("p_survey_methods."):
            raise ValidationError({'survey_method': ('Wrong classification.')})
        if self.classification_sys is not None and self.classification_sys.startswith("p_classification_system."):
            raise ValidationError({'classification_sys': ('Wrong classification.')})       

#########################################
## Profile General 
#########################################
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
    
    #layer_profile_set from ProfileLayer

    ## Classification Fields
    horizon_sequence = models.TextField(blank=True, null=True, db_comment='Horizons sequence of the profile')
    old_classification = models.TextField(blank=True, null=True, db_comment='Old classification of the profile location')
    new_classification = models.TextField(blank=True, null=True, db_comment='New classification of the profile location')
    classification_sys = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, related_name='profilehorizonsequence_classification_sys_set', blank=True, null=True, db_comment='value from p_classification_system ')
    
    ## Genealogy section
    project = models.ForeignKey(Project, models.SET_NULL, blank=True, null=True, related_name='profile_project_set', db_comment='Survey/Project identifier')
    genealogy =  models.OneToOneField(Genealogy, on_delete=models.SET_DEFAULT, default=None, db_comment='Profile Genealogy')
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'profile_general'
        db_table_comment = 'The Soil Profile main table'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        if self.survey_method is not None and self.survey_method.startswith("p_survey_methods."):
            raise ValidationError({'survey_method': ('Wrong classification.')})
        if self.classification_sys is not None and self.classification_sys.startswith("p_classification_system."):
            raise ValidationError({'classification_sys': ('Wrong classification.')})       

#########################################
## Lab Data 
#########################################
class LabData(models.Model):
    ## sample_layer = None for Profiles LabData
    sample_layer = models.ForeignKey(SampleLayer, related_name='labdata_sample_layer_set', on_delete=models.CASCADE, blank=True, null=True)
    designation = models.TextField(db_comment='Layer Designation')
    classif_sys =  models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    texture_class = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)      
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper boundary in cm')
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower boundary in cm')   
    #measurement_lab_data_set from LayerLabDataMeasurement

    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'lab_data'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        # Ensures constraint on model level, raises ValidationError  
        if self.texture_class is not None and self.texture_class.startswith("l_texture_classes"):
            raise ValidationError({'texture_class': ('Wrong classification.')})  
        if self.classif_sys is not None and self.classif_sys.startswith("p_classification_system."):
            raise ValidationError({'classif_sys': ('Wrong classification.')}) 
        if self.upper is None or self.lower is None or self.upper < self.lower:
            raise ValidationError({'upper': ('lower cannot be smaller then upper or a null value.')}) 
   
class LabDataMeasurement(models.Model):
    lab_data = models.ForeignKey(LabData, on_delete=models.CASCADE, related_name='measurement_lab_data_set', db_comment='layer laboratory data ')
    value = models.DecimalField(max_digits=40, decimal_places=20, db_comment='measurement value')
    measure =  models.OneToOneField(LabMeasurement, on_delete=models.SET_DEFAULT, default=None, db_comment='Table LabMeasure')   
    method =  models.OneToOneField(LabMethod, on_delete=models.SET_DEFAULT, default=None, db_comment='Table LabMethod')      
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        unique_together = (('lab_data', 'measure', 'method',),)
        db_table = 'lab_data_measurement'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )

    def clean(self):
        # Ensures constraint on model level, raises ValidationError  
        if self.method is not None and self.measure is not None and self.measure.method_type != self.method.type:
            raise ValidationError({'measure': ('Wrong method type.')})  

#########################################
## Profile Layer
#########################################
class ProfileLayer(models.Model):
    profile = models.ForeignKey(ProfileGeneral, on_delete=models.CASCADE, related_name='layer_profile_set', db_comment='Foreign Key field: profile') 
    designation = models.TextField(db_comment='Horizon designation')
    layer_number = models.SmallIntegerField( validators=[validate_positive], db_comment='layer order in profile')
    upper = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='upper depth in cm')
    lower = models.DecimalField(max_digits=12, decimal_places=2, validators=[validate_positive], db_comment='lower depth in cm')
    homogeneity_part = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='Described parts, by exposed area [%]')
    homogeneity_alluvial_tephra = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Layer composed of several strata of alluvial sediments or of tephra')
    water_saturation = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Types of water saturation')
    water_status = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Soil water status')
    organicmineral = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='organic, organotechnic or mineral layer')
    boundaries_distinctness = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment="Distinctness of the layer's lower boundary")
    boundaries_shape = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    wind_disposition = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Wind deposition')
    texture_class = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Texture class') 
    texture_subclass = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Texture subclass')
    rh_value = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Rh Value')
    initial_weathering = models.DecimalField(max_digits=6 , decimal_places=2 , validators=[validate_percentage], db_comment='Initial weathering abundance')
    soluble_salts = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True, db_comment='ECSE [dS m-1m-1]')
    field_ph_misured_value = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True, db_comment='Potentiometric pH measurement - Measured value')
    field_ph_solution = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Potentiometric pH measurement - Solution and mixing ratio')
    continuity_volume_fractures = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    continuity_average_fractures = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_percentage], blank=True, null=True)
    volcanic_glasses_abundance = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL,blank=True, null=True)
    volcanic_glasses_thixotropy_naf = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True)
    bulk_density = models.DecimalField(max_digits=40, decimal_places=20, blank=True, null=True)
    packing_density = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Estimate the packing density using a knife with a blade approx. 10 cm long')
    parent_material = models.ForeignKey(Taxonomy, on_delete=models.SET_NULL, blank=True, null=True, db_comment='Report the parent material. Use the help of a geological map.')
    note = models.TextField(blank=True, null=True)
    
    remnants = models.OneToOneField(LayerRemnants, on_delete=models.SET_DEFAULT, default=None, db_comment='Remnants of broken-up cemented layers')
    coarse_fragments = models.OneToOneField(LayerCoarseFragments, on_delete=models.SET_DEFAULT, default=None, db_comment='Coarse fragments')
    artefacts = models.OneToOneField(LayerArtefacts, on_delete=models.SET_DEFAULT, default=None, db_comment='Artefacts')
    structure = models.OneToOneField(LayerStructure, on_delete=models.SET_DEFAULT, default=None, db_comment='Structure')
    cracks = models.OneToOneField(LayerCracks, on_delete=models.SET_DEFAULT, default=None, db_comment='Cracks')
    stress_features = models.OneToOneField(LayerStressFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='Stress Features')
    colours = models.OneToOneField(LayerColours, on_delete=models.SET_DEFAULT, default=None, db_comment='Section Colours')
    coatings_bridges = models.OneToOneField(LayerCoatingsBridges, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerCoatingsBridges')
    ribbonlike_accumulations = models.OneToOneField(LayerRibbonlikeAccumulations, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRibbonlikeAccumulations')
    carbonates = models.OneToOneField(LayerCarbonates, on_delete=models.SET_DEFAULT, default=None, db_comment='Section Layer Carbonates')
    gypsum = models.OneToOneField(LayerGypsum, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerGypsum')
    secondary_silicia = models.OneToOneField(LayerSecondarySilica, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerSecondarySilica')
    consistence = models.OneToOneField(LayerConsistence, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerConsistence')
    surface_crusts = models.OneToOneField(LayerSurfaceCrusts, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerSurfaceCrusts')   
    permafrost_features = models.OneToOneField(LayerPermafrostFeatures, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerPermafrostFeatures')   
    organic_carbon = models.OneToOneField(LayerOrganicCarbon, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerOrganicCarbon')   
    roots = models.OneToOneField(LayerRoots, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerRoots')   
    animal_activity = models.OneToOneField(LayerAnimalActivity, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerAnimalActivity')   
    human_alteration = models.OneToOneField(LayerHumanAlterations, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerHumanAlterations')   
    degree_decomposition = models.OneToOneField(LayerDegreeDecomposition, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerDegreeDecomposition')   
    lab_data = models.OneToOneField(LabData, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerLabData')   
    non_matrix_pore = models.OneToOneField(LayerNonMatrixPore, on_delete=models.SET_DEFAULT, default=None, db_comment='LayerNonMatrixPore')   

    def _get_thickness(self):
        "Returns the thickness"
        return self.lower - self.upper
    thickness = property(_get_thickness)   
    
    objects = models.Manager().using('soildatastore')

    class Meta:
        managed = True
        db_table = 'layer'
        permissions = (
            ('access_soildata', 'view_soildata', 'write_soildata'),
        )
        
    def clean(self):
        # Ensures constraint on model level, raises ValidationError
        if self.upper < self.lower:
            raise ValidationError({'upper': ('lower cannot be smaller then upper.')}) 
        if self.water_saturation is not None and self.water_saturation.startswith("l_water_saturation"):
            raise ValidationError({'water_type': ('Wrong classification.')})
        if self.water_status is not None and self.water_status.startswith("l_water_status"):
            raise ValidationError({'water_status': ('Wrong classification.')}) 
        if self.homogeneity_alluvial_tephra is not None and self.homogeneity_alluvial_tephra.startswith("l_alluvial_tephra."):
            raise ValidationError({'homogeneity_alluvial_tephra': ('Wrong classification.')})
        if self.boundaries_distinctness is not None and self.boundaries_distinctness.startswith("l_boundaries."):
            raise ValidationError({'boundaries_distinctness': ('Wrong classification.')})
        if self.boundaries_shape is not None and self.boundaries_shape.startswith("l_shape."):
            raise ValidationError({'boundaries_shape': ('Wrong classification.')})
        if self.organicmineral is not None and self.organicmineral.startswith("l_organic_mineral"):
            raise ValidationError({'organicmineral': ('Wrong classification.')}) 
        if self.wind_disposition is not None and self.wind_disposition.startswith("l_wind"):
            raise ValidationError({'wind_disposition': ('Wrong classification.')}) 
        if self.texture_class is not None and self.texture_class.startswith("l_texture_classes"):
            raise ValidationError({'texture_class': ('Wrong classification.')}) 
        if self.texture_subclass is not None and self.texture_subclass.startswith("l_texture_subclasses"):
            raise ValidationError({'texture_subclass': ('Wrong classification.')}) 
        if self.rh_value is not None and self.rh_value.startswith("l_rh_value"):
            raise ValidationError({'rh_value': ('Wrong classification.')}) 
        if self.field_ph_solution is not None and self.field_ph_solution.startswith("l_potenziometric_measure"):
            raise ValidationError({'field_ph_solution': ('Wrong classification.')}) 
        if self.packing_density is not None and self.packing_density.startswith("l_packing_density"):
            raise ValidationError({'packing_density': ('Wrong classification.')}) 
        if self.parent_material is not None and self.parent_material.startswith("l_type_parent_material"):
            raise ValidationError({'parent_material': ('Wrong classification.')})  


#########################################
## Indicators ...TO DO
######################################### """