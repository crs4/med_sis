import json
import requests
from datetime import datetime
from django.conf import settings
from .models import XLSxUpload
import re
import base64

# Quick Tests ##
file_data = None
#with open('/Users/ppalla/opt/my_geo/src/backoffice/files/mini-data.json', 'r') as f:
#    file_data = json.load(f)

######

class XLSxUploadService:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.report = {
            "start_time": datetime.now().isoformat(),
            "operations": [],
            "errors": [],
            "success": True
        }
        # Configurazione dell'autenticazione basic
        self.auth_username = settings.API_USERNAME
        self.auth_password = settings.API_PASSWORD
        self.auth_header = self._get_basic_auth_header()

    def _get_basic_auth_header(self):
        """
        Genera l'header di autenticazione basic
        """
        credentials = f"{self.auth_username}:{self.auth_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {'Authorization': f'Basic {encoded_credentials}'}

    def _model_name_to_endpoint(self, model_name):
        """
        Converte il nome del modello da CamelCase a formato endpoint plurale 
        seguendo le convenzioni di Django REST Framework.
        
        Args:
            model_name (str): Nome del modello in CamelCase (es. "LandformTopography")
            
        Returns:
            str: Nome convertito in formato endpoint plurale (es. "landform-topographies")
        """
        # Converte da CamelCase a snake_case
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', model_name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1)
        snake_case = s2.lower()
        
        # Applica le regole di pluralizzazione
        return self._pluralize(snake_case)
    
    def _pluralize(self, word):
        """
        Pluralizza una parola seguendo le regole inglesi di base
        utilizzate da Django REST Framework.
        
        Args:
            word (str): Parola al singolare
            
        Returns:
            str: Parola al plurale
        """
        # Regole di pluralizzazione inglese
        if word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
            # city -> cities, category -> categories
            return word[:-1] + 'ies'
        elif word.startswith('layer-') or word.startswith('profile-') or word.startswith('lab-') or word.startswith('surface-') or word.startswith('coarse-'):
            if word.endswith('general'):
                word = re.split('[-_]', word)[0] + 's'
            if word in ['profile-layer', 'layer-structure', 'layer-non-matrix-pore']:
                word = word + 's'
            return word
        elif word.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z')):
            # class -> classes, box -> boxes
            return word + 'es'
        elif word.endswith('f'):
            # leaf -> leaves
            return word[:-1] + 'ves'
        elif word.endswith('fe'):
            # knife -> knives
            return word[:-2] + 'ves'
        elif word.endswith('o') and len(word) > 1 and word[-2] not in 'aeiou':
            # hero -> heroes, potato -> potatoes
            return word + 'es'
        elif word.endswith('ed'):
            # cultivated -> cultivated
            return word
        else:
            # regola generale: aggiunge 's'
            return word + 's'
    def process_uploaded_data(self, xlsx_upload_id):
        try:
            # Recupera l'oggetto XLSxUpload
            xlsx_upload = XLSxUpload.objects.using('backoffice').get(id=xlsx_upload_id)
            
            if xlsx_upload.status != "IN_PROCESS":
                raise ValueError("L'upload non è in stato UPLOADED")
                
            data = xlsx_upload.data
            #data = file_data
            # Ordine di processamento degli array
            processing_order = [
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
            
            # Processa ogni array nell'ordine specificato
            for model_name in processing_order:
                if model_name in data:
                    self._process_array(model_name, data[model_name])
            
            # Aggiorna lo stato e il report
            xlsx_upload.status = "IMPORT_SUCCESS" if not self.report["errors"] else "IMPORT_WITH_ERROR"
            xlsx_upload.report = self.report
            xlsx_upload.save(using='backoffice')
            
            return self.report
            
        except Exception as e:
            self.report["success"] = False
            self.report["errors"].append(str(e))
            xlsx_upload.status = "CRITICAL_ERROR"
            xlsx_upload.report = self.report
            xlsx_upload.save(using='backoffice')
            return self.report
    
    def _process_array(self, model_name, array_data):
        # Utilizza il metodo per convertire il nome del modello
        endpoint_name = self._model_name_to_endpoint(model_name)
        endpoint = f"{self.base_url}/api/backoffice/{endpoint_name}/"
        
        for item in array_data:
            try:
                response = requests.post(
                    endpoint, 
                    json=item,
                    headers=self.auth_header
                )
                operation_result = {
                    "model": model_name,
                    "data": item,
                    "status_code": response.status_code,
                    "response": response.json() if response.status_code == 200 or response.status_code == 201 else None
                }
                
                if response.status_code != 201 and response.status_code != 200:
                    self.report["errors"].append(f"Errore nell'importazione di {model_name}: {response.text}")
                    self.report["success"] = False
                
                self.report["operations"].append(operation_result)
                
            except Exception as e:
                self.report["errors"].append(f"Errore nell'importazione di {model_name}: {str(e)}")
                self.report["success"] = False 