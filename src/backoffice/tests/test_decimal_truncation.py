#from django.test import TestCase
import unittest
from decimal import Decimal

import sys
import os
import django

# Aggiungi i path necessari per il progetto Django
sys.path.append('/Users/ppalla/opt/my_geo')
sys.path.append('/Users/ppalla/opt/my_geo/src')

# Configura l'ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's4m_catalogue.settings')
django.setup()

from django.conf import settings

# Importa i dati di prova

# Modifica temporaneamente solo l'host e la porta del database
original_db_config = settings.DATABASES['backoffice'].copy()
settings.DATABASES['backoffice'].update({
    'HOST': '127.0.0.1',  # indirizzo IP dell'host
    'PORT': '5432',       # porta mappata nel docker-compose
    'USER': 'backoffice_user',
    'PASSWORD': 'backoffice_pwd',
    'NAME': 'backoffice'
})

from backoffice.models import LabData, Taxonomy

class DecimalTruncationMixinTest(unittest.TestCase):
    def setUp(self):
        # Creiamo un'istanza di Taxonomy per i campi ForeignKey
        try:
            self.taxonomy = Taxonomy.objects.get(id='lab_data_classification.U')
        except Taxonomy.DoesNotExist:
            # Se non esiste, creane una per i test
            self.taxonomy = Taxonomy.objects.create(
                id='lab_data_classification.U',
                code='test_code',
                description='Test Description'
            )

    def test_decimal_truncation(self):
        """
        Test che verifica la troncatura dei decimali nel modello LabData
        """
        # Creiamo un'istanza di LabData con valori decimali che hanno più cifre decimali del consentito
        lab_data = LabData(
            id='TEST001',
            # Test con gravel che ha decimal_places=6
            gravel=Decimal('12.123456789'),
            # Test con sand che ha decimal_places=10
            sand=Decimal('45.12345678901234'),
            # Test con ph_h2o che ha decimal_places=10
            ph_h2o=Decimal('7.12345678901234'),
            # Aggiungiamo alcuni campi ForeignKey per evitare errori di validazione
            cls_sys=self.taxonomy,
            texture=self.taxonomy
        )

        # Eseguiamo la validazione
        lab_data.full_clean()
        lab_data.save()

        # Ricarichiamo l'oggetto dal database
        saved_lab_data = LabData.objects.get(id='TEST001')

        # Verifichiamo che i valori siano stati troncati correttamente
        self.assertEqual(saved_lab_data.gravel, Decimal('12.123456'))  # 6 decimali
        self.assertEqual(saved_lab_data.sand, Decimal('45.1234567890'))  # 10 decimali
        self.assertEqual(saved_lab_data.ph_h2o, Decimal('7.1234567890'))  # 10 decimali

    def test_decimal_truncation_with_null_values(self):
        """
        Test che verifica il comportamento con valori nulli
        """
        lab_data = LabData(
            id='TEST002',
            gravel=None,
            sand=None,
            ph_h2o=None,
            cls_sys=self.taxonomy,
            texture=self.taxonomy
        )

        # La validazione non dovrebbe sollevare eccezioni
        lab_data.full_clean()
        lab_data.save()

        # Ricarichiamo l'oggetto dal database
        saved_lab_data = LabData.objects.get(id='TEST002')

        # Verifichiamo che i valori nulli siano stati preservati
        self.assertIsNone(saved_lab_data.gravel)
        self.assertIsNone(saved_lab_data.sand)
        self.assertIsNone(saved_lab_data.ph_h2o)

    def test_decimal_truncation_with_invalid_values(self):
        """
        Test che verifica il comportamento con valori non validi
        """
        lab_data = LabData(
            id='TEST003',
            gravel='not_a_number',  # Valore non valido
            cls_sys=self.taxonomy,
            texture=self.taxonomy
        )

        # La validazione dovrebbe sollevare un'eccezione
        with self.assertRaises(Exception):
            lab_data.full_clean()

    def tearDown(self):
        pass
        """Pulizia dopo ogni test"""
        # Rimuovi i dati di test creati
        #LabData.objects.filter(id__startswith='TEST').delete()         

if __name__ == '__main__':
    unittest.main() 