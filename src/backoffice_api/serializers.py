from rest_framework import serializers
from backoffice.models import (
    ProfileGeneral, ProfileLayer, Taxonomy, Project, Genealogy,
    LandformTopography, ClimateAndWeather, Surface, LandUse, Cultivated
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProfileGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileGeneral
        fields = '__all__'
        #read_only_fields = ('code',)  # Il codice è generato automaticamente

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'
        read_only_fields = ('code',)  # Il codice è generato automaticamente

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # read_only_fields = ('code',)  # Commentato per rendere code scrivibile

class GenealogySerializer(serializers.ModelSerializer):
    class Meta:
        model = Genealogy
        fields = '__all__'
        read_only_fields = ('code',)  # Il codice è generato automaticamente

class LandformTopographySerializer(serializers.ModelSerializer):
    class Meta:
        model = LandformTopography
        fields = '__all__'
    
    
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

class SurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surface
        fields = '__all__'

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