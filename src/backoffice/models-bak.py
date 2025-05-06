
  
"""
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
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'sample_layer'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
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
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'sample_general'
        db_table_comment = 'The Soil Sample main table'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
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

    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'lab_data'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
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
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        unique_together = (('lab_data', 'measure', 'method',),)
        db_table = 'lab_data_measurement'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
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
    
    objects = models.Manager().using('backoffice')

    class Meta:
        managed = True
        db_table = 'layer'
        permissions = (
            ('access_backoffice', 'Can access backoffice data'),
            ('view_backoffice', 'Can view backoffice data'),
            ('write_backoffice', 'Can write backoffice data'),
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
######################################### 
"""