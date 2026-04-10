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
import logging

# Configura il logger
logger = logging.getLogger(__name__)

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
    
    def update(self, instance, validated_data):
        """
        Override del metodo update per riavviare l'elaborazione
        se vengono modificati i dati o l'operazione.
        """
        # Esegui l'aggiornamento standard dei campi
        instance = super().update(instance, validated_data)
        
        # Controlla se sono stati modificati campi che richiedono un riprocessamento
        # (es. 'data' o 'operation'). Se modifico il titolo non deve riprocessare.
        # L'if il task solo se vengono modificati i campi che richiedono un ri-processamento.
        if 'data' in validated_data and 'operation' in validated_data:
            
            # start_processing in models.py controlla: if self.status == "UPLOADED"
            # Se l'oggetto era già stato processato (es. status "IMPORT_SUCCESS" o "IMPORT_WITH_ERRORS"), 
            # start_processing fallisce. Dobbiamo forzare lo stato a "UPLOADED".
            instance.status = "UPLOADED"
            
            # Pulisci eventuali report precedenti se necessario per chiarezza
            instance.report = {} 
            
            instance.save(using='backoffice')
            
            # Avvia il processo
            started = instance.start_processing()
            
            # Opzionale: Loggare se il processo non è partito per qualche motivo
            if not started:
                logger.error(
                    f"Impossible to restart processing for upload ID {instance.id}. "
                    f"Current status: {instance.status}. "
                    "Check Celery configuration or model constraints."
                )
                # Opzionale: Aggiungere un warning nel report dell'oggetto
                instance.report = {"warning": "Processing task failed to start automatically upon update."}
                instance.save(using='backoffice')

        return instance

###########################
# Projects
###########################
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
###########################
# Point General
###########################
class PointGeneralSerializer(DecimalTruncationSerializerMixin, DateFormatSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = PointGeneral
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
# Point Layer
###########################

class PointLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointLayer
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
               
class LayerMatrixColoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerMatrixColours 
        fields = '__all__'
        
class LayerRedoximorphicSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerRedoximorphic 
        fields = '__all__'

class LayerLithogenicVariegatesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LayerLithogenicVariegates
        fields = '__all__'

class LayerCoatingsBridgesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerCoatingsBridges 
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

class  LayerPermafrostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayerPermafrost
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
        # Controlla se esiste già una combinazione Point-layer-level (quando level non è None)
        if level is not None:
            # Esclude l'istanza corrente se stiamo aggiornando
            queryset = LayerStructure.objects.filter(layer=layer, level=level)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError({
                    'layer': f"There is already a structure at level '{level}'   in layer '{layer}' "
                })
        else:
            raise serializers.ValidationError({
                'level': f"level is mandatory field"
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
## Requests 
#########################################

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request 
        fields = '__all__'
        read_only_fields = ('id',)   
    
    def update(self, instance, validated_data):
        """
        Override to start elaboration if status or fields are changed
        """
        # standard update
        instance = super().update(instance, validated_data)
        
        # 
        # (es. 'data' o 'operation'). Se modifico il titolo non deve riprocessare.
        # L'if il task solo se vengono modificati i campi che richiedono un ri-processamento.
        if 'status' in validated_data and 'kriging' in validated_data:
            # start_processing in models.py controlla: 
            # if self.status == "VALIDATED" and self.kriging == true --> interpolate and publish
            # if self.status == "VALIDATED" and self.kriging == false --> publish
            # if self.status == "CREATED" and self.kriging == true --> preprocess
            instance.save(using='backoffice')
            
            # Avvia il processo
            started = instance.start_processing()
            
            # Opzionale: Loggare se il processo non è partito per qualche motivo
            if not started:
                logger.error(
                    f"Impossible to restart processing for Request ID {instance.id}. "
                    f"Current status: {instance.status}. "
                    "Check Celery configuration or model constraints."
                )
                # Opzionale: Aggiungere un warning nel report dell'oggetto
                instance.status="ERRORS"
                instance.save(using='backoffice')

        return instance

#########################################
## Photos 
#########################################

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo 
        fields = '__all__' 

#########################################
## LabDataExtraMeasure 
#########################################

class LabDataExtraMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabDataExtraMeasure 
        fields = '__all__' 

#########################################
## Taxonomies 
#########################################

class TaxonomyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxonomyValue 
        fields = '__all__' 

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy 
        fields = '__all__' 

  
