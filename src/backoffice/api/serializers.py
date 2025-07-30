from rest_framework import serializers
from backoffice.models import *
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
import re
from datetime import datetime

from rest_framework import serializers
from decimal import Decimal, ROUND_DOWN

###########################
## Mixin
########################### 
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
    
###########################
## XLSx Uploads
###########################      
    
class XLSxUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = XLSxUpload
        fields = '__all__'
        read_only_fields = ('id',)  
    
    
    def create(self, validated_data):
        """
        Override del metodo create per avviare automaticamente l'elaborazione
        dopo la creazione dell'oggetto
        """

        instance = super().create(validated_data)
        instance.start_processing()
        return instance
   
###########################
# Profile\Monitorings Genealogy
###########################

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
###########################
# Profile General
###########################
class ProfileGeneralSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = ProfileGeneral
        fields = '__all__'

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
    
class LandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandUse
        fields = '__all__'
        
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

class LitterLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LitterLayer
        fields = '__all__'

class SurfaceCracksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SurfaceCracks
        fields = '__all__'
       
class CoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoarseFragments
        fields = '__all__'
        
class SurfaceUnevennessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurfaceUnevenness
        fields = '__all__'
       
###########################
## Lab Data 
###########################
class LabDataSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = LabData
        fields = '__all__'

###########################
# Profile Layer
###########################

class ProfileLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileLayer
        fields = '__all__'

class LayerRemnantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRemnants 
        fields = '__all__'
    
class LayerCoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoarseFragments 
        fields = '__all__'
        
class LayerArtefactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerArtefacts 
        fields = '__all__'
    
class LayerCracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCracks
        fields = '__all__'
        
class LayerStressFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerStressFeatures 
        fields = '__all__'
        
class LayerMatrixColoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerMatrixColours 
        fields = '__all__'
      
class LayerCoarserTexturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoarserTextured 
        fields = '__all__'
        
class LayerRedoximorphicFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphicFeatures 
        fields = '__all__'

class LayerLithogenicVariegatesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LayerLithogenicVariegates
        fields = '__all__'
        
class LayerRedoximorphicColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphicColour 
        fields = '__all__'

class LayerCoatingsBridgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoatingsBridges 
        fields = '__all__'
    
class LayerRibbonlikeAccumulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRibbonlikeAccumulations 
        fields = '__all__'
    
class LayerCarbonatesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = LayerCarbonates 
        fields = '__all__'
        
class LayerGypsumSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerGypsum
        fields = '__all__'

class LayerSecondarySilicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerSecondarySilica 
        fields = '__all__'
    
class LayerConsistenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerConsistence 
        fields = '__all__'
  
class LayerPermafrostFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerPermafrostFeatures 
        fields = '__all__'
        
class LayerOrganicCarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerOrganicCarbon
        fields = '__all__'
    
class LayerRootsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRoots 
        fields = '__all__'
    
class LayerAnimalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerAnimalActivity 
        fields = '__all__'
    
class  LayerHumanAlterationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerHumanAlterations 
        fields = '__all__'
    
class  LayerDegreeDecompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerDegreeDecomposition 
        fields = '__all__'
    
class  LayerNonMatrixPoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerNonMatrixPore
        fields = '__all__'
        
class  LayerStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerStructure 
        fields = '__all__'
    
    def validate(self, data):
        """
        Validazione personalizzata per controllare l'unicità prima del salvataggio
        """
        layer = data.get('layer')
        level = data.get('level')
        
        # Controlla se esiste già una combinazione profile-layer-level (quando level non è None)
        if level is not None:
            # Esclude l'istanza corrente se stiamo aggiornando
            queryset = LayerStructure.objects.filter(layer=layer, level=level)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'layer': f"There is already a structure at level '{level}' in layer '{layer}' "
                })
        else:
            raise serializers.ValidationError({
                'level': f"level is a mandatory field"
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

class LayerSurfaceCrustsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerSurfaceCrusts 
        fields = '__all__'


#########################################
## Indicators 
#########################################

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator  
        fields = '__all__'
        read_only_fields = ('id',)  

#########################################
## Requests 
#########################################

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request 
        fields = '__all__'
        read_only_fields = ('id',)  

###########################
# Monitoring General
###########################
class MonitoringGeneralSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MonitoringGeneral
        fields = '__all__'

class MonitoringLandformTopographySerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLandformTopography
        fields = '__all__'
    
    def create(self, validated_data):
        """
        Override del metodo create per catturare ValidationError dal modello
        """
        try:
            instance = MonitoringLandformTopography(**validated_data)
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
 
class MonitoringClimateAndWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringClimateAndWeather
        fields = '__all__'     

class MonitoringSurfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringSurface
        fields = '__all__'
        
    def create(self, validated_data):
        """
        Override del metodo create per catturare ValidationError dal modello
        """
        try:
            instance = MonitoringSurface(**validated_data)
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
    
class MonitoringLandUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLandUse
        fields = '__all__'
        
    def create(self, validated_data):
        try:
            instance = MonitoringLandUse(**validated_data)
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

class MonitoringCultivatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringCultivated
        fields = '__all__'
        
    def create(self, validated_data):
        try:
            instance = MonitoringCultivated(**validated_data)
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
        
class MonitoringNotCultivatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringNotCultivated
        fields = '__all__'
    def create(self, validated_data):
        try:
            instance = MonitoringNotCultivated(**validated_data)
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

class MonitoringLitterLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLitterLayer
        fields = '__all__'

class MonitoringSurfaceCracksSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MonitoringSurfaceCracks
        fields = '__all__'
       
class MonitoringCoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringCoarseFragments
        fields = '__all__'
        
class MonitoringSurfaceUnevennessSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringSurfaceUnevenness
        fields = '__all__'

class MonitoringSurfaceCrustsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringSurfaceCrusts 
        fields = '__all__'

###########################
## Lab Data 
###########################
class MonitoringLabDataSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = MonitoringLabData
        fields = '__all__'

###########################
# Profile Layer
###########################

class MonitoringLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayer
        fields = '__all__'

class MonitoringLayerRemnantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerRemnants 
        fields = '__all__'
    
class MonitoringLayerCoarseFragmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerCoarseFragments 
        fields = '__all__'
        
class MonitoringLayerArtefactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerArtefacts 
        fields = '__all__'
    
class MonitoringLayerCracksSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerCracks
        fields = '__all__'
        
class MonitoringLayerStressFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerStressFeatures 
        fields = '__all__'
        
class MonitoringLayerMatrixColoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerMatrixColours 
        fields = '__all__'
        
class MonitoringLayerCoarserTexturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerCoarserTextured 
        fields = '__all__'
        
class MonitoringLayerRedoximorphicFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerRedoximorphicFeatures 
        fields = '__all__'

class MonitoringLayerLithogenicVariegatesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MonitoringLayerLithogenicVariegates
        fields = '__all__'
        
class MonitoringLayerRedoximorphicColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerRedoximorphicColour 
        fields = '__all__'

class MonitoringLayerCoatingsBridgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerCoatingsBridges 
        fields = '__all__'
    
class MonitoringLayerRibbonlikeAccumulationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerRibbonlikeAccumulations 
        fields = '__all__'
    
class MonitoringLayerCarbonatesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MonitoringLayerCarbonates 
        fields = '__all__'
        
class MonitoringLayerGypsumSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerGypsum
        fields = '__all__'

class MonitoringLayerSecondarySilicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerSecondarySilica 
        fields = '__all__'
    
class MonitoringLayerConsistenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerConsistence 
        fields = '__all__'
    
class MonitoringLayerPermafrostFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerPermafrostFeatures 
        fields = '__all__'
        
class MonitoringLayerOrganicCarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerOrganicCarbon
        fields = '__all__'
    
class MonitoringLayerRootsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerRoots 
        fields = '__all__'
    
class MonitoringLayerAnimalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerAnimalActivity 
        fields = '__all__'
    
class  MonitoringLayerHumanAlterationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerHumanAlterations 
        fields = '__all__'
    
class  MonitoringLayerDegreeDecompositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerDegreeDecomposition 
        fields = '__all__'
    
class  MonitoringLayerNonMatrixPoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerNonMatrixPore
        fields = '__all__'
        
class  MonitoringLayerStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLayerStructure 
        fields = '__all__'
    
    def validate(self, data):
        """
        Validazione personalizzata per controllare l'unicità prima del salvataggio
        """
        layer = data.get('layer')
        level = data.get('level')
        
        # Controlla se esiste già una combinazione profile-layer-level (quando level non è None)
        if level is not None:
            # Esclude l'istanza corrente se stiamo aggiornando
            queryset = MonitoringLayerStructure.objects.filter(layer=layer, level=level)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'layer': f"There is already a structure at level '{level}' in layer '{layer}' "
                })
        else:
            raise serializers.ValidationError({
                'level': f"level is a mandatory field"
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


#########################################
## Indicators 
#########################################

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator  
        fields = '__all__'
        read_only_fields = ('id',)  

#########################################
## Requests 
#########################################

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request 
        fields = '__all__'
        read_only_fields = ('id',)  

  