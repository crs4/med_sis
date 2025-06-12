from django.db import models
from decimal import Decimal, ROUND_DOWN, InvalidOperation
from django.core.exceptions import ValidationError


class DecimalTruncationMixin:
    """
    Mixin che tronca automaticamente tutti i campi DecimalField
    al numero di cifre decimali specificato nel campo, PRIMA della validazione
    """
    
    def _truncate_decimal(self, value, decimal_places):
        """
        Tronca un valore decimale al numero specificato di cifre decimali
        
        Args:
            value: Il valore da troncare
            decimal_places: Numero di cifre decimali da mantenere
            
        Returns:
            Decimal troncato o None se value è None
        """
        if value is None:
            return None
        
        try:
            # Converte in Decimal se non lo è già
            if not isinstance(value, Decimal):
                # Usa str() per evitare problemi di precisione con float
                decimal_value = Decimal(str(value))
            else:
                decimal_value = value
            
            # Calcola il quantizer per la troncatura
            if decimal_places == 0:
                quantizer = Decimal('1')
            else:
                quantizer = Decimal('0.1') ** decimal_places
            
            # Tronca (non arrotonda) usando ROUND_DOWN
            truncated = decimal_value.quantize(quantizer, rounding=ROUND_DOWN)
            
            return truncated
            
        except (ValueError, InvalidOperation, TypeError) as e:
            # Se la conversione fallisce, rilancia come ValidationError
            raise ValidationError(f'Impossibile convertire il valore "{value}" in decimale: {e}')
    
    def _get_decimal_fields(self):
        """
        Restituisce tutti i campi DecimalField del modello con le loro configurazioni
        
        Returns:
            Lista di dizionari con informazioni sui campi decimali
        """
        decimal_fields = []
        
        for field in self._meta.get_fields():
            if isinstance(field, models.DecimalField):
                decimal_fields.append({
                    'name': field.name,
                    'decimal_places': field.decimal_places,
                    'max_digits': field.max_digits
                })
        
        return decimal_fields
    
    def _apply_decimal_truncation(self):
        """
        Applica la troncatura a tutti i campi decimali.
        Questo metodo viene chiamato prima di qualsiasi validazione.
        """
        for field_info in self._get_decimal_fields():
            field_name = field_info['name']
            decimal_places = field_info['decimal_places']
            
            # Ottieni il valore corrente del campo
            current_value = getattr(self, field_name, None)
            
            if current_value is not None:
                try:
                    truncated_value = self._truncate_decimal(current_value, decimal_places)
                    setattr(self, field_name, truncated_value)
                except ValidationError:
                    # Re-rilancia ValidationError con il nome del campo
                    raise ValidationError({
                        field_name: f'Valore non valido per il campo {field_name}: "{current_value}"'
                    })
    
    def clean(self):
        """
        Override del metodo clean per applicare la troncatura PRIMA della validazione
        """
        # PRIMA: Applica la troncatura decimale
        self._apply_decimal_truncation()
        
        # DOPO: Esegui la validazione standard con i valori già troncati
        super().clean()
    
    def full_clean(self, exclude=None, validate_unique=True):
        """
        Override di full_clean per garantire che la troncatura avvenga
        prima di qualsiasi tipo di validazione
        """
        # PRIMA: Applica la troncatura decimale
        self._apply_decimal_truncation()
        
        # DOPO: Esegui la validazione completa con i valori già troncati
        super().full_clean(exclude=exclude, validate_unique=validate_unique)
    
    def save(self, *args, **kwargs):
        """
        Override del save per garantire che la troncatura e validazione
        avvengano prima del salvataggio
        """
        # Se non è stata chiamata full_clean(), la chiamiamo
        # (che includerà automaticamente la troncatura)
        if not hasattr(self, '_state') or not getattr(self, '_clean_called', False):
            self.full_clean()
        
        # Salva con i valori già troncati e validati
        super().save(*args, **kwargs)


