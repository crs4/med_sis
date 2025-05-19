from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from backoffice.models import *
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class XSLxSheetConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = XSLxSheetConf
        fields = '__all__'
        #read_only_fields = ('code',)  # Commentato per rendere code scrivibile

class XSLxMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = XSLxMapping
        fields = '__all__'
        #read_only_fields = ('code',)  # Commentato per rendere code scrivibile

class XLSxUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = XLSxUpload
        fields = '__all__'
        #read_only_fields = ('code',)  # Commentato per rendere code scrivibile


class ProfileGeneralSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = ProfileGeneral
        fields = '__all__'

"""
class ProfileGeneralListSerializer(GeoFeatureModelSerializer):
    point = GeometrySerializerMethodField()

    def get_point(self, obj):
        return Point(obj.lon_wgs84, obj.lat_wgs84)
        
    class Meta:
        model = ProfileGeneral
        geo_field = "point"
        auto_bbox = True
        fields = ( 'code', 'location', 'lat_wgs84', 'lon_wgs84',
                    'date', 'gps', 'surveyors','elev_m_asl','elev_dem',
                    'survey_m','notes','project','cls_sys' )

"""
      
class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # read_only_fields = ('code',)  # Commentato per rendere code scrivibile

class GenealogySerializer(serializers.ModelSerializer):
    class Meta:
        model = Genealogy
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LandformTopographySerializer(serializers.ModelSerializer):
    class Meta:
        model = LandformTopography
        fields = '__all__'
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        """
        Override del metodo create per catturare ValidationError dal modello
        """
        try:
            instance = LandformTopography(**validated_data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def update(self, instance, validated_data):
        """
        Override del metodo update per catturare ValidationError dal modello
        """
        try:
            # Aggiorniamo i campi dell'istanza
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Validiamo prima di salvare
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
 
class ClimateAndWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateAndWeather
        fields = '__all__'
        read_only_fields = ('id',)

class SurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surface
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data):
        """
        Override del metodo create per catturare ValidationError dal modello
        """
        try:
            instance = Surface(**validated_data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def update(self, instance, validated_data):
        """
        Override del metodo update per catturare ValidationError dal modello
        """
        try:
            # Aggiorniamo i campi dell'istanza
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            
            # Validiamo prima di salvare
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)        
    """ 
    def validate(self, data):
        errors = {}
        
        # Validazione dei campi numerici
        for field_name in ['surface_crusts_area', 'outcrops_area_covered', 'desert_ventifacts', 'desert_varnish']:
            value = data.get(field_name)
            if value is not None:
                try:
                    if value < 0 or value > 100:
                        errors[field_name] = [_('Il campo %(field)s deve essere compreso tra 0 e 100') % {'field': field_name}]
                except (TypeError, ValueError):
                    errors[field_name] = [_('Il campo %(field)s deve essere un numero valido') % {'field': field_name}]

        # Validazione del campo ground_water_depth
        value = data.get('ground_water_depth')
        if value is not None:
            try:
                if value < 0:
                    errors['ground_water_depth'] = [_('Il campo ground_water_depth deve essere positivo')]
            except (TypeError, ValueError):
                errors['ground_water_depth'] = [_('Il campo ground_water_depth deve essere un numero valido')]

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
            value = data.get(field_name)
            if value is not None and str(value).startswith(prefix):
                if field_name not in errors:
                    errors[field_name] = []
                errors[field_name].append(_('Classificazione errata per il campo %(field)s') % {'field': field_name})

        if errors:
            raise serializers.ValidationError(errors)
        
        return data

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            if hasattr(e, 'detail'):
                raise serializers.ValidationError(e.detail)
            raise e """

class LandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandUse
        fields = '__all__'
        read_only_fields = ('id',)
    """
    def validate(self, data):
        errors = {}
        
        # Validazione dei campi ForeignKey
        taxonomy_validations = {
            'land_use': 'p_land_use.',
            'corine': 'p_corine.'
        }

        for field_name, prefix in taxonomy_validations.items():
            value = data.get(field_name)
            if value is not None and str(value).startswith(prefix):
                if field_name not in errors:
                    errors[field_name] = []
                errors[field_name].append(_('Classificazione errata per il campo %(field)s') % {'field': field_name})

        if errors:
            raise serializers.ValidationError(errors)
        
        return data
    """    

    def create(self, validated_data):
        try:
            instance = LandUse(**validated_data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)           

class CultivatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultivated
        fields = '__all__'
        read_only_fields = ('id',)
    """
    def validate(self, data):
        errors = {}
        
        # Validazione dei campi ForeignKey
        taxonomy_validations = {
            'cultivation_type': 'p_cultivation_type.',
            'spec_prod_tech1': 'p_productivity_techniques.',
            'spec_prod_tech2': 'p_productivity_techniques.',
            'spec_prod_tech3': 'p_productivity_techniques.'
        }

        for field_name, prefix in taxonomy_validations.items():
            value = data.get(field_name)
            if value is not None and str(value).startswith(prefix):
                if field_name not in errors:
                    errors[field_name] = []
                errors[field_name].append(_('Classificazione errata per il campo %(field)s') % {'field': field_name})

        # Validazione dei campi numerici
        if 'cultivation_cover_by_area' in data:
            try:
                value = data['cultivation_cover_by_area']
                if value is not None and (value < 0 or value > 100):
                    errors['cultivation_cover_by_area'] = [_('Il campo deve essere compreso tra 0 e 100')]
            except (TypeError, ValueError):
                errors['cultivation_cover_by_area'] = [_('Il campo deve essere un numero valido')]

        # Validazione delle regole di business
        if data.get('cultivation_cessation') is not None:
            if data.get('last_species1') is None or data.get('actual_species1') is not None:
                errors['cultivation_cessation'] = [_('cultivation_cessation error no dominant last specie present or actual dominant specie.')]

        if data.get('last_species1') is not None:
            if data.get('cultivation_cessation') is None or data.get('actual_species1') is not None:
                errors['last_species1'] = [_('last_species1 error no cultivation_cessation or actual specie present.')]

        if data.get('last_species2') is not None:
            if data.get('last_species1') is None or data.get('actual_species2') is not None:
                errors['last_species2'] = [_('last_species2 error no dominant last specie or second actual specie present.')]

        if data.get('last_species3') is not None:
            if data.get('last_species2') is None or data.get('actual_species3') is not None:
                errors['last_species3'] = [_('last_species3 error no second last specie or third actual specie present.')]

        if errors:
            raise serializers.ValidationError(errors)
        
        return data
    """
    def create(self, validated_data):
        try:
            instance = Cultivated(**validated_data)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.full_clean()
            instance.save()
            return instance
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        
class NotCultivatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotCultivated
        fields = '__all__'
        read_only_fields = ('id',)

class LabDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabData
        fields = '__all__'
        read_only_fields = ('id',)

class LitterLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LitterLayer
        fields = '__all__'
        read_only_fields = ('id',)

class SurfaceCracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfaceCracks
        fields = '__all__'
        read_only_fields = ('id',)

class CoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoarseFragments
        fields = '__all__'
        read_only_fields = ('code',)

class SurfaceUnevennessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfaceUnevenness
        fields = '__all__'
        read_only_fields = ('id',)

class ProfileLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLayer
        fields = '__all__'
        read_only_fields = ('id',)

class LayerRemnantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRemnants 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerCoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoarseFragments 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerArtefactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerArtefacts 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerCracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCracks
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerStressFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerStressFeatures 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerMatrixColoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerMatrixColours 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerTextureColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerTextureColour 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerRedoximorphicFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphicFeatures 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerLithogenicVariegatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerLithogenicVariegates
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerRedoximorphicColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphicColour 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerCoatingsBridgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoatingsBridges 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerRibbonlikeAccumulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRibbonlikeAccumulations 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerCarbonatesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LayerCarbonates 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerGypsumSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerGypsum
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerSecondarySilicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerSecondarySilica 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerConsistenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerConsistence 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerSurfaceCrustsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerSurfaceCrusts 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerPermafrostFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerPermafrostFeatures 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerOrganicCarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerOrganicCarbon
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerRootsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRoots 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerAnimalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerAnimalActivity 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerHumanAlterationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerHumanAlterations 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerDegreeDecompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerDegreeDecomposition 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerNonMatrixPoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerNonMatrixPore
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerStructure 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class IndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente

class GeoDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoDataset 
        fields = '__all__'
        read_only_fields = ('id',)  # Il codice è generato automaticamente
