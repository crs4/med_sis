import unittest
#from django.test import TestCase
import os
import django
import sys

# Aggiungi i path necessari per il progetto Django
sys.path.append('/usr/src/s4m_catalogue')

# Configura l'ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's4m_catalogue.settings')
django.setup()

from backoffice.services import XLSxUploadService

class TestXLSxUploadService(unittest.TestCase):
    def setUp(self):
        self.service = XLSxUploadService()

    def test_model_name_to_endpoint(self):
        # Lista di modelli da testare
        test_cases = [
            "LandformTopography",
            "ClimateAndWeather",
            "Cultivated",
            "LandUse",
            "Surface",
            "CoarseFragments",
            "SurfaceCracks",
            "SurfaceUnevenness",
            "ProfileGeneral",
            "LayerCoarseFragments",
            "LayerNonMatrixPore",
            "LayerCracks",
            "LayerMatrixColours",
            "LayerCoatingsBridges",
            "LayerCarbonates",
            "LayerPermafrostFeatures",
            "LayerOrganicCarbon",
            "LayerRoots",
            "LayerDegreeDecomposition",
            "LayerStressFeatures",
            "LayerAnimalActivity",
            "LabData",
            "ProfileLayer",
            "LayerStructure"
        ]

        # Risultati attesi
        expected_results = [
            "landform-topographies",
            "climate-and-weathers",
            "cultivated",
            "land-uses",
            "surfaces",
            "coarse-fragments",
            "surface-cracks",
            "surface-unevennesses",
            "profile-generals",
            "layer-coarse-fragments",
            "layer-non-matrix-pores",
            "layer-cracks",
            "layer-matrix-colours",
            "layer-coatings-bridges",
            "layer-carbonates",
            "layer-permafrost-features",
            "layer-organic-carbons",
            "layer-roots",
            "layer-degree-decompositions",
            "layer-stress-features",
            "layer-animal-activities",
            "lab-data",
            "profile-layers",
            "layer-structures"
        ]

        # Test per ogni caso
        for model_name, expected_endpoint in zip(test_cases, expected_results):
            with self.subTest(model_name=model_name):
                result = self.service._model_name_to_endpoint(model_name)
                self.assertEqual(result, expected_endpoint, 
                    f"Errore nella conversione di {model_name}. Atteso: {expected_endpoint}, Ottenuto: {result}")

if __name__ == '__main__':
    unittest.main() 