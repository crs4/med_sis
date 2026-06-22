import json
import requests
import subprocess
import time
from datetime import datetime
from django.conf import settings
from .models import XLSxUpload, Dataset
import os 
import re
import base64
from osgeo import ogr, osr, gdal
# Enable GDAL/OGR exceptions
gdal.UseExceptions()
# GDAL & OGR memory drivers
GDAL_MEMORY_DRIVER = gdal.GetDriverByName('MEM')
OGR_MEMORY_DRIVER = ogr.GetDriverByName('MEM')


###### XLSs Upload
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
        elif word.startswith('layer-') or word.startswith('point-') or word.startswith('lab-') or word.startswith('surface-') or word.startswith('coarse-'):
            if word.endswith('general'):
                word = word + 's'
            if word in ['point-layer', 'layer-consistence', 'layer-redoximorphic-colour', 'layer-structure', 'layer-non-matrix-pore']:
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
                raise ValueError("Upload is not IN_PROCESS status")
                
            data = xlsx_upload.data
            if not isinstance(data, dict):
                data = json.loads(data)
            #data = file_data
            # Ordine di processamento degli array                              
            processing_order = [
                "LandformTopography",  
                "ClimateAndWeather", 
                "LandUse",  
                "LitterLayer",
                "Surface", 
                "SurfaceUnevenness", 
                "PointGeneral",
                "LayerCoarseFragments",
                "LayerRemnants",
                "LayerArtefacts",
                "LayerNonMatrixPore",
                "LayerCracks",
                "LayerMatrixColours",
                "LayerLithogenicVariegates",
                "LayerRedoximorphic",
                "LayerCoatingsBridges",
                "LayerCarbonates",
                "LayerGypsum",
                "LayerSecondarySilica",
                "LayerConsistence",
                "LayerPermafrost",
                "LayerOrganicCarbon",
                "LayerRoots",
                "LayerAnimalActivity",
                "LayerHumanAlterations",
                "LayerDegreeDecomposition",
                "LabData",
                "PointLayer",
                "LayerStructure"
            ]  


            processing_order_genealogies = [
                "Project"    
            ]

            processing_order_extra_measure = [
                "LabDataExtraMeasure"    
            ]

            processing_order_photos = [
                "Photo"     
            ]

            if xlsx_upload.type == 'XLS_PJ':
                processing_order = processing_order_genealogies

            if xlsx_upload.type == 'XLS_PH':
                processing_order = processing_order_photos 

            if xlsx_upload.type == 'XLS_EM':
                processing_order = processing_order_extra_measure 

            # Processa ogni array nell'ordine specificato
            for model_name in processing_order:
                if model_name in data:
                    self._process_array(model_name, data[model_name], xlsx_upload.operation )
            
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
    
    def _process_array(self, model_name, array_data, operation):
        # Utilizza il metodo per convertire il nome del modello
        endpoint_name = self._model_name_to_endpoint(model_name)
        if model_name == 'Photo' : endpoint_name = 'photos'
        if model_name == 'LabDataExtraMeasure' : endpoint_name = 'lab-data-extra-measures'
        if model_name == 'Project' : endpoint_name = 'projects'
        endpoint = f"{self.base_url}/api/backoffice/{endpoint_name}/"
        for item in array_data:
            _id = item["id"]
            try:
                if operation == 'POST' : 
                    response = requests.post(
                        endpoint, 
                        json=item,
                        headers=self.auth_header
                    )
                else :
                    if operation == 'PATCH' : 
                        response = requests.patch(f"{endpoint}{_id}/", 
                            data=item,
                            headers=self.auth_header
                        )
                    else: 
                        response = requests.put(f"{endpoint}{_id}/", 
                            data=item,
                            headers=self.auth_header
                        )    
                operation_result = {
                    "model": model_name,
                    "element": _id,
                    "msg": response.status_code
                }
                #200 ok with returned obj
                #201 ok created without returned object
                #202 is a preliminary ok without returned object
                #203 ok the proxy erased the returned object
                #204 ok updated/deleted without returned object
                if response.status_code < 200 or response.status_code > 299:
                    errors = 'data error'
                    res = response.json()
                    if  res and res['errors'] :
                        errors = str(res['errors'])
                    error = {
                        "model": model_name,
                        "element": _id,
                        "msg": f"CODE: {str(response.status_code)},MSG: {errors}"
                    }
                    self.report["errors"].append(error)
                    self.report["success"] = False
                else :
                    self.report["operations"].append(operation_result)
                
            except Exception as e:
                error = {
                    "model": model_name,
                    "element": _id,
                    "msg": str(e)  
                }
                self.report["errors"].append(error)
                self.report["success"] = False 

###### Dataset Publishing
class DatasetService:
    def __init__(self):
        # Reset of report data ( create datasets result )
        self.report = {
            "start_time": datetime.now().isoformat(),
            "msgs": [],
            "raster": None,
            "points": None,
            "variogram": None,
            "success": True
        }
        # base URL of APIs
        self.base_url = settings.API_BASE_URL
        # basic authentication  parameters
        self.auth_username = settings.API_USERNAME
        self.auth_password = settings.API_PASSWORD
        self.auth_header = self._get_basic_auth_header()

    def _get_basic_auth_header(self):
        """
        Generates the header for basic authentication
        """
        credentials = f"{self.auth_username}:{self.auth_password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {'Authorization': f'Basic {encoded_credentials}'}
   
    def process_dataset_data(self, dataset_id):
############ EVALUATE PARAMETERS         
        try:
            # get Dataset object
            dataset = Dataset.objects.using('backoffice').get(id=dataset_id) 
            if dataset is not None and dataset.filter is not None:
                if dataset.status == "IN_PROCESS" :
                    filter = dataset.filter
                    if not isinstance(filter, dict):
                        filter = json.loads(filter)
                    #1st dataset: geoJSON filtered points (EPSG:4326)    
                    points = filter['points']
                    #2nd dataset: geoJSON area of interest (EPSG:4326)    
                    aoi = filter['aoi']
                    # 3th dataset geotiff interpolation raster (EPSG:9000) 
                    if dataset.kriging:
                        k_params = dataset.k_params
                        if not isinstance(k_params, dict):
                            k_params = json.loads(k_params)
                        # KRIGING dataset
                        # geoJSON aggreagated points in area of interest (EPSG:4326)    
                        k_data = dataset.k_data
                        if not isinstance(k_data, dict):
                            k_data = json.loads(k_data)
                        k_points = k_params['points']
                        if not isinstance(k_points, dict):
                            k_points = json.loads(k_points)
                        k_model = k_params['model']
                        k_maxdist = k_params['maxDist']
                        k_box = k_params['bbox']
                        k_epsg = k_params['epsg']
                        k_nclasses = k_params['nClasses']
                        k_nskip = k_params['nSkip']
                else  :
                    raise ValueError("Dataset is not IN_PROCESS status")
            else  :
                raise ValueError("Dataset not found")
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage1: errors reading dataset, wrong parameters, exited")
            return self.report
        t = round(time.time() * 1000)
        folder = f"dataset_{dataset_id}_{t}" 
        name = f"dataset_{dataset_id}_{t}"
        base_path = '/tmp/' + folder
        try:
            os.mkdir(base_path)
        except:
            pass
############ GENERATE WORK FILES FROM PARAMETERS        
        try :
            with open(base_path+"/points.json", "w") as outfile:
                json.dump(points, outfile)
            with open(base_path+"/aoi.json", "w") as outfile:
                json.dump(aoi, outfile)
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage2: errors creating files, exited")
            return self.report
        #ogr2ogr -s_srs 'EPSG:4326' -t_srs 'EPSG:32636' kpoints.shp kpoints.json
############ IF KRIGING IS TRUE GENERATES WORK FILES FROM PARAMETERS          
        try :
            if dataset.kriging:
                with open(base_path+"/kpoints.json", "w") as outfile:
                    json.dump(k_points, outfile)
                with open(base_path+"/bbox.json", "w") as outfile:
                    json.dump(k_box, outfile)
            
                # Reproject aggregated poimts and change file format
                pointsSHP = os.path.join( base_path, "kpoints.shp")
                pointsJSON = os.path.join( base_path, "kpoints.json")
                params = f"ogr2ogr -s_srs 'EPSG:4326' -t_srs '{k_epsg}' {pointsSHP} {pointsJSON}"
                subprocess.call([params], shell=True) 
                # Reproject the area of interests and change file format
                aoiJSON = os.path.join( base_path, "aoi.json")
                aoiUTMJSON = os.path.join( base_path, "utmaoi.json")
                params = f"ogr2ogr -s_srs 'EPSG:4326' -t_srs '{k_epsg}' {aoiUTMJSON} {aoiJSON}"
                subprocess.call([params], shell=True) 
                # Reproject the bounding box 
                pathUTMJSON = os.path.join( base_path, "utmbbox.json")
                pathGEOJSON = os.path.join( base_path, "bbox.json")
                params = f"ogr2ogr -s_srs 'EPSG:4326' -t_srs '{k_epsg}' {pathUTMJSON} {pathGEOJSON}"
                subprocess.call([params], shell=True)                
                with open(base_path+"/utmbbox.json", "r") as file:
                    utmBox = json.load(file)
                    feature = utmBox['features'][0]
                    north = feature['bbox'][3]
                    south = feature['bbox'][1]
                    east = feature['bbox'][2]
                    west = feature['bbox'][0]
                    size = north - south
                    if size < east - west:
                        size = east - west
                    # Tiff size: 2000 x 2000 pixels
                    # cell_size is in meters
                    cell_size = size / 2000.0
                predictionGRD = os.path.join( base_path, "prediction")
                varianceGRD = os.path.join( base_path, "variance")  
                # SAGA_CMD  
                saga_cmd =  f"saga_cmd statistics_kriging 0 -POINTS {pointsSHP} -FIELD value -VAR_MODEL '{k_model}' -VAR_NCLASSES {k_nclasses} " 
                saga_cmd += f" -TARGET_USER_XMIN {west} -TARGET_USER_XMAX {east} -TARGET_USER_YMIN {south} -TARGET_USER_YMAX {north} " 
                saga_cmd += f" -TARGET_USER_SIZE {cell_size} -VAR_MAXDIST {k_maxdist}  -VAR_NSKIP {k_nskip} " 
                saga_cmd += f" -PREDICTION {predictionGRD} -VARIANCE {varianceGRD} " 
                subprocess.call([saga_cmd], shell=True) 
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage3: errors in elaborating kriging interpolation, exited")
            return self.report

############ IF KRIGING GENERATE AND VALIDATE GEOTIFF          
        try :    
            if dataset.kriging:
                output = f"{base_path}/prediction.tif"
                output2 = f"{base_path}/prediction_clip.tif" 
                # 1. change saga grid format to GeoTiff
                #gdal_translate -of GTiff                 
                cmd = f"gdal_translate -of GTiff -ot Float32 -co COMPRESS=DEFLATE -co PREDICTOR=3 {predictionGRD}.sdat {output}"
                subprocess.call([cmd], shell=True) 
                
                cmd = f"gdalwarp -cutline {aoiUTMJSON} -crop_to_cutline -overwrite {output} {output2}"
                subprocess.call([cmd], shell=True)  
                ##CLEAN
                f = base_path+"/points.json"
                f2 = base_path+"/aoi.json"
                f3 = base_path+"/kpoints.json"
                f4 = base_path+"/bbox.json"
                f5 = base_path+"/kpoints.shp"
                f6 = base_path+"/utmaoi.json"
                f7 = base_path+"/utmbbox.json"
                f8 = base_path+"/bbox.json"
        except Exception as e:
            self.report["success"] = False
            self.report["errors"].append("Stage4: wrong Geotiff reading interpolation, exited")
            return self.report
        
############ PUBLISHING POINTS DATASET
        #1st dataset: filtered points (EPSG:4326) geoJSON base_path+"/"+name+"_points.json"    
        try :
            url = f"{self.base_url}/api/v2/uploads/upload/"
            files= [
                ('base_file', ( name +'_points.json',open(base_path+'/points.json','r'), 'application/json')),
                ('json_file', ( name +'_points.json',open(base_path+'/points.json','r'), 'application/json'))
            ]
            response = requests.post( url, files=files, headers=self.auth_header)
            if response.status_code == 200:
                res = response.json()
                if res.execution_id is not None :
                    #monitoring task
                    go = True
                    while go:
                        urlTask = f"{self.base_url}/api/v2/executionrequest/{res.execution_id}" 
                        responseTask = requests.get( urlTask, headers=self.auth_header)
                        if responseTask.status_code == 200:
                            resTask = responseTask.json()
                            if resTask.geonode_resource is not None : 
                                geonode_points_id = resTask.geonode_resource
                            if resTask.status == 'finished' or resTask.status == 'failed':
                                go = False    
                        else :
                            go = False
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage5: errors creating points dataset, exited")
            return self.report
############ PUBLISHING AOI DATASET        
        #2nd dataset: area of interest (EPSG:4326) geoJSON base_path+"/"+name+"_aoi.json"
        try :
            url = f"{self.base_url}/api/v2/uploads/upload/"
            #style = f"/geoserver_data/data/workspaces/geonode/styles/{data.source}.sld"
            files= [
                # ('sld_file',('name +'_aoi.sld',open('...indicatorSLDFilepath.sld','rb'),'application/octet-stream')),
                ('base_file', ( name +'_aoi.json',open(base_path+'/aoi.json','r'), 'application/json')),
                ('json_file', ( name +'_aoi.json',open(base_path+'/aoi.json','r'), 'application/json'))
            ]
            response = requests.post( url, files=files, headers=self.auth_header )
            if response.status_code == 200:
                res = response.json()
                if res.execution_id is not None :
                    # upload monitoring task
                    go = True
                    while go:
                        urlTask = f"{self.base_url}/api/v2/executionrequest/{res.execution_id}" 
                        responseTask = requests.get( urlTask, headers=self.auth_header)
                        if responseTask.status_code == 200:
                            resTask = responseTask.json()
                            if resTask.geonode_resource is not None : 
                                geonode_aoi_id = resTask.geonode_resource
                            if resTask.status == 'finished' or resTask.status == 'failed':
                                go = False    
                        else :
                            go = False
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage6: errors creating aoi dataset, exited")
            return self.report
############ PUBLISHING INTERPOLATION RASTER DATASET
        #3th dataset: interpolation raster - geotiff base_path+"/"+name+"_prediction.tif"
        try :
            if dataset.kriging:
                url = f"{self.base_url}/api/v2/uploads/upload/"
                files= [
                    ('base_file', ( name+'_prediction.tif',open(base_path+'/prediction.tif','rb'), 'image/tiff')),
                    ('tif_file', ( name+'_prediction.tif',open(base_path+'/prediction.tif','rb'), 'image/tiff'))
                ]
                response = requests.post( url, files=files, headers=self.auth_header)
                if response.status_code == 200:
                    res = response.json()
                    if res.execution_id is not None :
                        #monitoring task
                        go = True
                        while go:
                            urlTask = f"{self.base_url}/api/v2/executionrequest/{res.execution_id}" 
                            responseTask = requests.get( urlTask, headers=self.auth_header)
                            if responseTask.status_code == 200:
                                resTask = responseTask.json()
                                if resTask.geonode_resource is not None : 
                                    geonode_prediction_id = resTask.geonode_resource
                                if resTask.status == 'finished' or resTask.status == 'failed':
                                    go = False    
                            else :
                                go = False
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage7: errors creating prediction raster dataset, exited")
            return self.report

############ METADATA geonode_points_id, geonode_aoi_id, geonode_prediction_id
        try:
            url = f"{self.base_url}/api/v2/datasets/{geonode_points_id}"
            data = {
                "title": f"Filter: {dataset.id} source: {dataset.source}, date: {dataset.date}",
                "abstract": f"Filter {dataset.id} executed on source {dataset.source} executed in date:{dataset.date}",
                "category": "geoscientificInformation",
                "keywords": "pippo"
            }
            response = requests.patch( url, headers=self.auth_header, json=data)
            #if response.status_code == 200:
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage8: errors creating prediction raster dataset, exited")
            return self.report

############ FINALIZE
        self.report["success"] = True
        self.report["msgs"].append("Stage9: datasets successfully published ")
        with open(base_path+"/report.json", "w") as outfile:
            json.dump(self.report, outfile)    
        return self.report
           
#### for all soil indicators data in JSON format
# typename, name, abstract, type 
# dataset.source === soil indicator typename 
# geoserver_data/data/workspaces/geonode/styles/typename.sld
# 
# geoserver_data/data/workspaces/geonode/backoffice/typename            
        
    