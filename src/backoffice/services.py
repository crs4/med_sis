import json
import requests
import subprocess
import time
from datetime import datetime
from django.conf import settings
from .models import XLSxUpload, Dataset, BaseDataset
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
            "aoi": None,
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
   
    def _get_style_for_raster(self, max, min):
        """
        Generates the style for the raster
        """
        step = (max - min )/4
        ramp = [ min, max-3*step, max-2*step, max-step, max ]

        style =  '<?xml version="1.0" encoding="UTF-8"?>\n'
        style += '<StyledLayerDescriptor version="1.0.0"\n' 
        style += '          xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"\n' 
        style += '          xmlns="http://www.opengis.net/sld"\n' 
        style += '          xmlns:ogc="http://www.opengis.net/ogc"\n' 
        style += '          xmlns:xlink="http://www.w3.org/1999/xlink"\n' 
        style += '          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
        style += '    <NamedLayer>\n'
        style += '      <Name>prediction_raster</Name>\n'
        style += '      <UserStyle>\n' 
        style += '          <Title>Raster of prediction</Title>\n' 
        style += '          <Abstract>Raster of prediction</Abstract>\n' 
        style += '          <FeatureTypeStyle>\n'  
        style += '          <Rule>\n'
        style += '              <Name>Prediction_raster</Name>\n'
        style += '              <Title>Prediction raster</Title>\n'
        style += '              <RasterSymbolizer>\n' 
        style += '                  <ChannelSelection>\n'
        style += '                      <GrayChannel>\n'
        style += '                          <SourceChannelName>1</SourceChannelName>\n'
        style += '                      </GrayChannel>\n'
        style += '                  </ChannelSelection>\n'
        style += '                  <ColorMap type="ramp">\n'  
        color = None
        for x in ramp:
            if color is None : color = '#d7191c'
            elif color == '#d7191c' : color = '#fdae61'
            elif color == '#fdae61' : color = '#ffffbf'
            elif color == '#ffffbf' : color = '#abdda4'
            elif color == '#abdda4' : color = '#2b83ba'
            style += f"                    <ColorMapEntry label=\"{x}\" quantity=\"{x}\" color=\"{color}\"/>\n"
        style += '                  </ColorMap>\n'
        style += '              </RasterSymbolizer>\n'
        style += '          </Rule>\n'
        style += '        </FeatureTypeStyle>\n'
        style += '      </UserStyle>\n'
        style += '    </NamedLayer>\n'
        style += '</StyledLayerDescriptor>\n'
        return style

    def _manageTask( self, url, files ):
        geonode_resource_id = None
        response = requests.post( url, files=files, headers=self.auth_header )
        if response.status_code >= 200 and response.status_code < 300:
            res = response.json()
            if res["execution_id"] is not None :
                #monitoring task
                go = True
                while go:
                    urlTask = f"{self.base_url}/api/v2/executionrequest/{res['execution_id']}" 
                    responseTask = requests.get( urlTask, headers=self.auth_header)
                    if responseTask.status_code >= 200 and responseTask.status_code < 300:
                        resTask = (responseTask.json())['request']
                        if resTask['geonode_resource'] is not None : 
                            geonode_resource_id = resTask['geonode_resource']
                        if resTask['status'] == 'finished' or resTask['status'] == 'failed':
                            go = False 
                    else :
                        go = False
                return geonode_resource_id
    
    def _writeReport( self, base_path ):
        with open(base_path+"/report.json", "w") as outfile:
            json.dump(self.report, outfile)

    def process_dataset_data(self, dataset_id):
############ EVALUATE PARAMETERS         
        if True:
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
        #except Exception as e:
        #    self.report["success"] = False
        #    self.report["msgs"].append("Stage1: errors reading datasets, wrong parameters, exited")
        #    return self.report
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
            self.report["msgs"].append("Stage1: Temporary folder with data created")
            with open(base_path+"/points.json", "w") as outfile:
                json.dump(points, outfile)
            with open(base_path+"/aoi.json", "w") as outfile:
                json.dump(aoi, outfile)
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage2: errors creating files, exited")
            self._writeReport(base_path)
            return self.report
        self.report["msgs"].append("Stage1: points.json and aoi.json files created")
            
############ IF KRIGING IS TRUE GENERATES WORK FILES FROM PARAMETERS          
        try :
            if dataset.kriging:
                with open(base_path+"/kpoints.json", "w") as outfile:
                    json.dump(k_points, outfile)
                with open(base_path+"/bbox.json", "w") as outfile:
                    json.dump(k_box, outfile)
                self.report["msgs"].append("Stage3 (Kriging): k_points.json and k_box.json files created")
                   
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
                self.report["msgs"].append("Stage3 (Kriging): k_points.shp, utmaoi.json and utmbbox.json files created")
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
                self.report["msgs"].append("Stage3 (Kriging): ordinary kriging")
                self.report["msgs"].append(f"Stage3 (Kriging): {saga_cmd}")               
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage3 (Kriging): Errors in elaborating kriging interpolation, exited")
            return self.report

############ IF KRIGING GENERATE AND VALIDATE GEOTIFF          
        try :    
            if dataset.kriging:
                output = f"{base_path}/prediction.tif"
                output2 = f"{base_path}/prediction_clip.tif" 

                # 1. change saga grid format to GeoTiff
                #gdal_translate -of GTiff                 
                cmd = f"gdal_translate -of GTiff -ot Float32 -co 'COMPRESS=LZW' -co 'PREDICTOR=1' {predictionGRD}.sdat {output}"
                subprocess.call([cmd], shell=True) 
                
                cmd = f"gdalwarp -co 'COMPRESS=LZW' -co 'PREDICTOR=1' -cutline {aoiUTMJSON} -crop_to_cutline -overwrite {output} {output2}"
                subprocess.call([cmd], shell=True)  
                self.report["msgs"].append("Stage4 (Kriging): Tiff and Aoi clipped Tiff files created")        
        except Exception as e:
            self.report["success"] = False
            self.report["errors"].append("Stage4 (Kriging): wrong data reading Geotiff, exited")
            self._writeReport(base_path)
            return self.report
        
############ PUBLISHING POINTS DATASET
        base_path_sld = '/geoserver_data/data/workspaces/geonode/styles/'
        #1st dataset: filtered points (EPSG:4326) geoJSON base_path+"/"+name+"_points.json"    
        try :
            typename = dataset.src_typename
            typename = typename[8:]
            url = f"{self.base_url}/api/v2/uploads/upload/"
            files= [
                ('base_file', ( name +'_points.json',open(base_path+'/points.json','r'), 'application/json')),
                ('json_file', ( name +'_points.json',open(base_path+'/points.json','r'), 'application/json')),
                ('sld_file',  ( name + '_points.sld',  open(base_path_sld+typename+'.sld','rb'),'application/octet-stream'))
            ]
            geonode_points_id = self._manageTask(url,files)
            if geonode_points_id is not None:
                self.report["msgs"].append(f"Stage5 (Publishing): points dataset published: {geonode_points_id} ")
                self.report["points"] = geonode_points_id
            else: 
                self.report["msgs"].append("Stage5 (Publishing): errors, points dataset not published")
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage5: errors creating points dataset, exited")
            self._writeReport(base_path)
            return self.report
############ PUBLISHING AOI DATASET 
# styles location: /geoserver_data/data/workspaces/geonode/styles/
# typename of source -> typename.sld         
        #2nd dataset: area of interest (EPSG:4326) geoJSON base_path+"/"+name+"_aoi.json"
        try:
            url = f"{self.base_url}/api/v2/uploads/upload/"
            #style = f"/geoserver_data/data/workspaces/geonode/styles/{data.source}.sld"
            files= [
                ('base_file', ( name + '_aoi.json', open(base_path+'/aoi.json','r'), 'application/json')),
                ('json_file', ( name + '_aoi.json', open(base_path+'/aoi.json','r'), 'application/json')),
                ('sld_file',  ( name + '_aoi.sld',  open(base_path_sld+'areas.sld','rb'),'application/octet-stream'))
            ]
            geonode_aoi_id = self._manageTask(url,files)
            if geonode_aoi_id is not None:
                self.report["msgs"].append("Stage6 (Publishing): AOI dataset published")
                self.report["aoi"] = geonode_aoi_id
            else: 
                self.report["msgs"].append("Stage6 (Publishing): errors, AOI dataset not published")    
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage6: errors creating aoi dataset, exited")
            self._writeReport(base_path)
            return self.report
        
############ PUBLISHING INTERPOLATION RASTER DATASET
        #3th dataset: interpolation raster - geotiff base_path+"/"+name+"_prediction.tif"
        try :
            if dataset.kriging:
                prediction_tif = gdal.Open(f"{base_path}/prediction_clip.tif")
                srcband = prediction_tif.GetRasterBand(1)
                # Get raster statistics
                stats = srcband.GetStatistics(True, True)
                min = stats[0]
                max = stats[1]
                style = self._get_style_for_raster(max, min)
                with open(base_path+"/raster.sld", "w") as outfile:
                    outfile.write(style)
                url = f"{self.base_url}/api/v2/uploads/upload/"
                files= [
                    ('base_file', ( name + '_prediction.tif',open(base_path+'/prediction_clip.tif','rb'), 'image/tiff')),
                    ('tif_file', ( name + '_prediction.tif',open(base_path+'/prediction_clip.tif','rb'), 'image/tiff')),
                    ('sld_file',  ( name + '_prediction.sld',  open(base_path + '/raster.sld','rb'),'application/octet-stream'))
                ]
                geonode_prediction_id = self._manageTask(url,files)
                if geonode_prediction_id is not None:
                    self.report["msgs"].append("Stage7 (Kriging - Publishing): interpolation raster dataset published")
                    self.report["raster"] = geonode_prediction_id
                else: 
                    self.report["msgs"].append("Stage7 (Kriging - Publishing): errors, interpolation raster dataset not published")               
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage7 (Kriging - Publishing): errors creating prediction raster dataset, exited")
            self._writeReport(base_path)
            return self.report

############ METADATA geonode_points_id, geonode_aoi_id, geonode_prediction_id
        try:
            url = f"{self.base_url}/api/v2/datasets/{geonode_points_id}"
            mdata = {
                "title": f"{name}-POINTS",
                "abstract": f"Filter {dataset.id} executed on source {dataset.source} executed in date:{dataset.date}",
                "category": "geoscientificInformation",
            }
            response = requests.patch( url, data=mdata, headers=self.auth_header, )
            if response.status_code >= 200 and response.status_code < 300:
                self.report["msgs"].append("Stage8 (Metadata - Publishing): metadata for points dataset published")
            else: 
                self.report["msgs"].append("Stage8 (Metadata - Publishing): metadata not published")
            
        except Exception as e:
            self.report["success"] = False
            self.report["msgs"].append("Stage8: errors metadata for points dataset not published")
            self._writeReport(base_path)
            return self.report
            
############ FINALIZE
        cmd = f"rm -r {base_path}"
        subprocess.call([cmd], shell=True) 
        self.report["success"] = True
        self.report["msgs"].append("Stage9: datasets successfully published ")
        self.report["msgs"].append("Stage10: temporary folder removed ")
        
        return self.report
           
class BaseDatasetService:
    def __init__(self):
        # Reset of report data ( create datasets result )
        self.report = {
            "start_time": datetime.now().isoformat(),
            "msgs": [],
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
   
    def process_base_dataset_data(self, _id):
############ EVALUATE PARAMETERS         
        try: 
            # get BaseDataset object
            dataset = BaseDataset.objects.using('backoffice').get(code=_id) 
            if dataset is not None :
                if dataset.status == "IN_PROCESS" :
############ EXECUTE UPDATE LAYERS
                    cmd = f"python manage.py updatelayers -s backoffice -f {dataset.code}"
                    subprocess.call([cmd], shell=True) 
                    self.report["msgs"].append(f"Update Layer {dataset.code} done")                      
                                                        
############ CHANGE METADATA 
                    url = f"{self.base_url}/api/v2/datasets/?filter%7Balternate%7D=geonode:{dataset.code}&format=json"
                    response = requests.get( url, headers=self.auth_header ) 
                    if response.status_code >= 200 and response.status_code < 300:
                        geonode_datasets = (response.json())["datasets"]
                        geonode_dataset =  geonode_datasets[0]
                        mdata = {
                            "title": dataset.name,
                            "abstract": dataset.abstract,
                        }
                        topic = None
                        if dataset.type == "soil_biological_health" : 
                            topic = { "identifier": "soil_biological_health", "gn_description":"Soil Biological Health" }
                        if dataset.type == "soil_physical_health" :
                            topic = { "identifier": "soil_physical_health", "gn_description":"Soil Physical Health" }
                        if dataset.type == "soil_chemical_health" :
                            topic = { "identifier": "soil_chemical_health", "gn_description":"Soil Chemical Health" }
                        if dataset.type == "points_soil_data" : 
                            topic = { "identifier": "points_soil_data", "gn_description":"Points Soil Data" }
                        if topic:
                            mdata['category'] = topic;    
                        if geonode_dataset['pk'] is not None:
                            dataset.geonode_id = geonode_dataset['pk']
                            url = f"{self.base_url}/api/v2/datasets/{geonode_dataset['pk']}"
                            response2 = requests.patch( url, json=mdata, headers=self.auth_header )
                            if response2.status_code >= 200 and response2.status_code < 300:
                                self.report["msgs"].append(f"metadata added to the dataset {geonode_dataset['pk']}")                      
                            else:
                                self.report["msgs"].append(f"error writing metadata in the dataset {geonode_dataset['pk']}")
                            self.report["geonode"] = dataset.geonode_id
                            self.report["success"] = True
                            return self.report
                else  :
                    raise ValueError("Dataset is not IN_PROCESS status")
            else  :
                raise ValueError("Dataset not found")
        except Exception as e:
            self.report["msgs"].append("Error " + str(e))
            self.report["success"] = False 
            return self.report

class HydroPtfModelService:
    def __init__(self):
        # Reset of report data ( create datasets result )
        self.report = {
            "start_time": datetime.now().isoformat(),
            "msgs": [],
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
          
    def process_hydro_ptf_model(self, _id):
        return 

class HydroPtfModelElaboration:
    def __init__(self):
        # Reset of report data ( create datasets result )
        self.report = {
            "start_time": datetime.now().isoformat(),
            "msgs": [],
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
    
    def process_hydro_ptf_elaboration(self, _id):
        return 
                         