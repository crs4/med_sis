from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from backoffice.models import *
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
import re
from datetime import datetime

from rest_framework import serializers
from decimal import Decimal, ROUND_DOWN



class DecimalTruncationSerializerMixin:
    """
    Mixin per serializer che tronca automaticamente i campi decimali
    prima della validazione DRF
    """
    
    def _truncate_decimal_value(self, value, decimal_places):
        """Tronca un valore decimale"""
        if value is None:
            return None
        
        try:
            if not isinstance(value, Decimal):
                decimal_value = Decimal(str(value))
            else:
                decimal_value = value
            
            if decimal_places == 0:
                quantizer = Decimal('1')
            else:
                quantizer = Decimal('0.1') ** decimal_places
            
            return decimal_value.quantize(quantizer, rounding=ROUND_DOWN)
        except:
            return value  # Se fallisce, restituisce il valore originale
    
    def _get_model_decimal_fields(self):
        """Ottiene i campi decimali dal modello associato"""
        if not hasattr(self.Meta, 'model'):
            return {}
        
        decimal_fields = {}
        for field in self.Meta.model._meta.get_fields():
            if hasattr(field, 'decimal_places') and hasattr(field, 'max_digits'):
                decimal_fields[field.name] = field.decimal_places
        
        return decimal_fields
    
    def to_internal_value(self, data):
        """
        Override per troncare i valori decimali prima della validazione DRF
        """
        # Ottieni i campi decimali del modello
        decimal_fields = self._get_model_decimal_fields()
        
        # Se data è un dizionario, crea una copia per non modificare l'originale
        if isinstance(data, dict):
            truncated_data = data.copy()
            
            # Tronca tutti i campi decimali
            for field_name, decimal_places in decimal_fields.items():
                if field_name in truncated_data:
                    original_value = truncated_data[field_name]
                    truncated_value = self._truncate_decimal_value(original_value, decimal_places)
                    truncated_data[field_name] = truncated_value
        else:
            truncated_data = data
        
        # Chiama il to_internal_value del parent con i dati troncati
        return super().to_internal_value(truncated_data)




class DateFormatSerializerMixin:
    """
    Mixin per convertire automaticamente i campi date dal formato ISO timestamp
    al formato date semplice (YYYY-MM-DD).
    
    Converte valori come "1996-10-01T00:00:00.000Z" in "1996-10-01"
    """
    
    def to_internal_value(self, data):
        """
        Converte i campi date dal formato ISO timestamp al formato date prima della validazione
        """
        if isinstance(data, dict):
            # Crea una copia dei dati per evitare modifiche al dizionario originale
            data = data.copy()
            
            # Ottieni tutti i campi date del serializer
            date_fields = self._get_date_fields()
            
            for field_name in date_fields:
                if field_name in data and data[field_name]:
                    data[field_name] = self._convert_iso_to_date(data[field_name])
        
        return super().to_internal_value(data)
    
    def _get_date_fields(self):
        """
        Identifica tutti i campi di tipo DateField nel serializer
        """
        date_fields = []
        
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.DateField):
                date_fields.append(field_name)
        
        return date_fields
    
    def _convert_iso_to_date(self, value):
        """
        Converte un valore dal formato ISO timestamp al formato date (YYYY-MM-DD)
        
        Args:
            value: Il valore da convertire (può essere stringa o già un oggetto date/datetime)
        
        Returns:
            str: Data nel formato YYYY-MM-DD o il valore originale se non convertibile
        """
        if not isinstance(value, str):
            return value
        
        # Pattern per riconoscere il formato ISO con timestamp
        # Esempi: "1996-10-01T00:00:00.000Z", "2023-12-25T14:30:00Z", "2024-01-15T10:45:30.123Z"
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?Z?$'
        
        if re.match(iso_pattern, value):
            try:
                # Rimuovi la 'Z' finale se presente
                clean_value = value.rstrip('Z')
                
                # Parse della data ISO
                if '.' in clean_value:
                    # Con millisecondi
                    dt = datetime.fromisoformat(clean_value)
                else:
                    # Senza millisecondi
                    dt = datetime.fromisoformat(clean_value)
                
                # Restituisci solo la parte della data nel formato YYYY-MM-DD
                return dt.strftime('%Y-%m-%d')
                
            except ValueError:
                # Se il parsing fallisce, restituisci il valore originale
                pass
        
        return value

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

    def create(self, validated_data):
        """
        Override del metodo create per avviare automaticamente l'elaborazione
        dopo la creazione dell'oggetto
        """

        instance = super().create(validated_data)
        instance.start_processing()
        return instance

class ProfileGeneralSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
        
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
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LandformTopographySerializer(serializers.ModelSerializer):
    class Meta:
        model = LandformTopography
        fields = '__all__'
        #read_only_fields = ('id',)
    
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
        #read_only_fields = ('id',)

class SurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surface
        fields = '__all__'
        #read_only_fields = ('id',)

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
        #read_only_fields = ('id',)
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
        #read_only_fields = ('id',)
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
        #read_only_fields = ('id',)
        def create(self, validated_data):
            try:
                instance = NotCultivated(**validated_data)
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

class LabDataSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = LabData
        fields = '__all__'
        #read_only_fields = ('id',)

class LitterLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LitterLayer
        fields = '__all__'
        #read_only_fields = ('id',)

class SurfaceCracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfaceCracks
        fields = '__all__'
        ##read_only_fields = ('id',)

class CoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoarseFragments
        fields = '__all__'
        #read_only_fields = ('code',)

class SurfaceUnevennessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfaceUnevenness
        fields = '__all__'
        #read_only_fields = ('id',)

class ProfileLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLayer
        fields = '__all__'
        #read_only_fields = ('id',)

class LayerRemnantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRemnants 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerCoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoarseFragments 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerArtefactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerArtefacts 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerCracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCracks
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerStressFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerStressFeatures 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerMatrixColoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerMatrixColours 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerTextureColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerTextureColour 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerRedoximorphicFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphicFeatures 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerLithogenicVariegatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerLithogenicVariegates
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerRedoximorphicColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphicColour 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerCoatingsBridgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoatingsBridges 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerRibbonlikeAccumulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRibbonlikeAccumulations 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerCarbonatesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LayerCarbonates 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerGypsumSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerGypsum
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerSecondarySilicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerSecondarySilica 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerConsistenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerConsistence 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerSurfaceCrustsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerSurfaceCrusts 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerPermafrostFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerPermafrostFeatures 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerOrganicCarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerOrganicCarbon
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerRootsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRoots 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerAnimalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerAnimalActivity 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerHumanAlterationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerHumanAlterations 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerDegreeDecompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerDegreeDecomposition 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class  LayerNonMatrixPoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerNonMatrixPore
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class LayerStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerStructure 
        fields = '__all__'
    
    def validate(self, data):
        """
        Validazione personalizzata per controllare l'unicità prima del salvataggio
        """
        layer = data.get('layer')
        level = data.get('level')
        
        # Controlla se esiste già una combinazione layer-level (quando level non è None)
        if level is not None:
            # Esclude l'istanza corrente se stiamo aggiornando
            queryset = LayerStructure.objects.filter(layer=layer, level=level)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'layer': f"Esiste già una struttura con layer '{layer}' e level '{level}'"
                })
        
        return data
    
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            # Fallback nel caso la validazione preventiva non abbia catturato tutto
            raise serializers.ValidationError({
                'non_field_errors': [
                    f"Errore di integrità del database: {str(e)}"
                ]
            })
    
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'non_field_errors': [
                    f"Errore di integrità del database: {str(e)}"
                ]
            })        
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class IndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente

class GeoDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoDataset 
        fields = '__all__'
        #read_only_fields = ('id',)  # Il codice è generato automaticamente
