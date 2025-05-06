from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from backoffice.models import *
#ProfileGeneral, Taxonomy, Project, Genealogy, LandformTopography, ClimateAndWeather, Surface, LandUse, Cultivated
from .serializers import *
#ProfileGeneralSerializer, TaxonomySerializer, ProjectSerializer, GenealogySerializer, LandformTopographySerializer, ClimateAndWeatherSerializer, SurfaceSerializer, LandUseSerializer, CultivatedSerializer
from rest_framework import serializers
from rest_framework_gis.filters import InBBoxFilter

###########################
## Uilities 
###########################
class TaxonomyViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le tassonomie.
    """
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le tassonomie in base ai parametri di query.
        """
        queryset = Taxonomy.objects.all()
        
        # Filtro per nome della tassonomia
        taxonomy = self.request.query_params.get('taxonomy', None)
        if taxonomy is not None:
            queryset = queryset.filter(taxonomy=taxonomy)
            
        # Filtro per nome
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
            
        # Filtro per super categoria
        super_cat = self.request.query_params.get('super_cat', None)
        if super_cat is not None:
            queryset = queryset.filter(super_cat=super_cat)
            
        return queryset

class LabMethodViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le tassonomie.
    """
    queryset = LabMethod.objects.all()
    serializer_class = LabMethodSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le tassonomie in base ai parametri di query.
        """
        queryset = Taxonomy.objects.all()
        
        # Filtro per nome della tassonomia
        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)
            
        # Filtro per nome
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
            
        return queryset

class LabMeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le tassonomie.
    """
    queryset = LabMeasurement.objects.all()
    serializer_class = LabMeasurementSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le tassonomie in base ai parametri di query.
        """
        queryset = LabMeasurement.objects.all()
        
        # Filtro per nome della tassonomia
        method = self.request.query_params.get('method', None)
        if method is not None:
            queryset = queryset.filter(method=method)
            
        # Filtro per nome
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
               
        return queryset

###########################
## XLSx Uploads
###########################

class XLSxUploadViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di gestire gli upload.
    """
    queryset = XLSxUpload.objects.all()
    serializer_class = XLSxUploadSerializer
    list_serializer_class = XLSxUploadListSerializer
    permission_classes = [permissions.IsAdminUser ]


    def get_queryset(self):
        """
        Filtra le tassonomie in base ai parametri di query.
        """
        queryset = XLSxUpload.objects.all()
        
        # Filtro per tipo di upload
        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)
            
        # Filtro per date
        _from = self.request.query_params.get('from', None)
        _to = self.request.query_params.get('to', None)
        if _from is not None:
            queryset = queryset.filter(date__gte=_from)
        if _to is not None:
            queryset = queryset.filter(date__lte=_to)
        
        # Filtro per user
        editor = self.request.query_params.get('editor', None)
        if editor is not None:
            queryset = queryset.filter(editor=editor)
            
        return queryset

class XSLxSheetConfViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = XSLxSheetConf.objects.all()
    serializer_class = XSLxSheetConfSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = XSLxSheetConf.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        type = self.request.query_params.get('type', None)
        if code is not None:
            queryset = queryset.filter(type=type)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
            
        return queryset

class XSLxMappingViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = XSLxMapping.objects.all()
    serializer_class = XSLxMappingSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = XSLxMapping.objects.all()
        
        # Filtro per codice
        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        model = self.request.query_params.get('model', None)
        if model is not None:
            queryset = queryset.filter(model=model)
        sheet = self.request.query_params.get('sheet', None)
        if sheet is not None:
            queryset = queryset.filter(sheet=sheet)     
        return queryset

###########################
# Profile\Samples Genealogy
###########################

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare i progetti.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra i progetti in base ai parametri di query.
        """
        queryset = Project.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
            
        # Filtro per titolo
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
            
        # Filtro per descrizione
        descr = self.request.query_params.get('description', None)
        if descr is not None:
            queryset = queryset.filter(descr__icontains=descr)
            
        return queryset

class GenealogyViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = Genealogy.objects.all()
    serializer_class = GenealogySerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le genealogie in base ai parametri di query.
        """
        queryset = Genealogy.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
            
        # Filtro per progetto
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(project=project)
            
        # Filtro per date
        _from = self.request.query_params.get('from', None)
        _to = self.request.query_params.get('to', None)
        if _from is not None:
            queryset = queryset.filter(date__gte=_from)
        if _to is not None:
            queryset = queryset.filter(date__lte=_to)    
        return queryset

###########################
# Profile General
###########################

class ProfileGeneralViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare i profili del suolo.
    """
    queryset = ProfileGeneral.objects.all()
    serializer_class = ProfileGeneralSerializer
    list_serializer_class = ProfileGeneralListSerializer
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter,)
    bbox_filter_include_overlapping = True # Optional
    permission_classes = [permissions.IsAdminUser ]
    
    
    def get_queryset(self):
        queryset = ProfileGeneral.objects.all()
        # Filtri per codice e data
        code = self.request.query_params.get('code', None)
        date = self.request.query_params.get('date', None)
        _from = self.request.query_params.get('from', None)
        _to = self.request.query_params.get('to', None)

        # Filtri per location_name
        location_name = self.request.query_params.get('location_name', None)
        
        # Filtri per elevazione
        elevation_min = self.request.query_params.get('elevation_min', None)
        elevation_max = self.request.query_params.get('elevation_max', None)
        
        # Filtri per progetto e classificazione
        project = self.request.query_params.get('project', None)
        classification_sys = self.request.query_params.get('classification_sys', None)
        
        # Filtri per note
        text = self.request.query_params.get('note', None)
        if text is not None:
            queryset = queryset.filter(notes__icontains=text)
        
        # Applicazione dei filtri
        if code:
            queryset = queryset.filter(code=code)
        if date:
            queryset = queryset.filter(date=date)
        if _from:
            queryset = queryset.filter(date__gte=_from)
        if _to:
            queryset = queryset.filter(date__lte=_to)
        if location_name:
            queryset = queryset.filter(location_name__icontains=location_name)
        if elevation_min:
            queryset = queryset.filter(elevation_m_asl__gte=elevation_min)
        if elevation_max:
            queryset = queryset.filter(elevation_m_asl__lte=elevation_max)
        if project:
            queryset = queryset.filter(project=project)
        if classification_sys:
            queryset = queryset.filter(classification_sys=classification_sys)
            
        return queryset
    
class LandformTopographyViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le caratteristiche topografiche del terreno.
    """
    queryset = LandformTopography.objects.all()
    serializer_class = LandformTopographySerializer
    permission_classes = [permissions.IsAdminUser ]

    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # Formatta gli errori nel formato {"campo": "messaggio violazione validazione"}
            errors = {}
            for field, error_messages in serializer.errors.items():
                errors[field] = error_messages[0] if error_messages else ""
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            # Formatta gli errori nel formato richiesto
            errors = {}
            for field, error_messages in serializer.errors.items():
                errors[field] = error_messages[0] if error_messages else ""
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST) """       

    def get_queryset(self):
            """
            Filtra le caratteristiche topografiche in base ai parametri di query.
            """
            queryset = LandformTopography.objects.all()
            
            # Filtro per gradiente in salita
            grad_slope = self.request.query_params.get('grad_slope', None)
            if grad_slope is not None:
                queryset = queryset.filter(grad_ups__gte=grad_slope)
                queryset = queryset.filter(grad_downs__lte=grad_slope)
                
            # Filtro per forma del pendio
            slope_shp_min = self.request.query_params.get('slope_shp_min', None)
            slope_shp_max = self.request.query_params.get('slope_shp_min', None)
            if slope_shp_min is not None:
                queryset = queryset.filter(slope_shape__lte=slope_shp_max)
            if slope_shp_max is not None:
                queryset = queryset.filter(slope_shape__gte=slope_shp_min)
                
            # Filtro per posizione del profilo
            position = self.request.query_params.get('position', None)
            if position is not None:
                queryset = queryset.filter(position=position)

            # Filtro per landform1
            landform1 = self.request.query_params.get('landform1', None)
            if landform1 is not None:
                queryset = queryset.filter(landform1=landform1)
            
            # Filtro per landform2
            landform2 = self.request.query_params.get('landform2', None)
            if landform2 is not None:
                queryset = queryset.filter(landform2=landform2)

            # Filtro per landform1_activity
            activity1 = self.request.query_params.get('activity1', None)
            if activity1 is not None:
                queryset = queryset.filter(activity1=activity1)
            
            # Filtro per landform2_activity
            activity2 = self.request.query_params.get('activity2', None)
            if activity2 is not None:
                queryset = queryset.filter(activity2=activity2)

            # Filtro per geomorphic_description
            text = self.request.query_params.get('geo_descr', None)
            if text is not None:
                queryset = queryset.filter(geo_descr__icontains=text)
            text = self.request.query_params.get('note', None)
            if text is not None:
                queryset = queryset.filter(notes__icontains=text)
            
            return queryset
 
class ClimateAndWeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le informazioni climatiche e meteorologiche.
    """
    queryset = ClimateAndWeather.objects.all()
    serializer_class = ClimateAndWeatherSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le informazioni climatiche e meteorologiche in base ai parametri di query.
        """
        queryset = ClimateAndWeather.objects.all()
        
        # Filtro per classificazione climatica di Köppen
        clim_koppen = self.request.query_params.get('clim_koppen', None)
        if clim_koppen is not None:
            queryset = queryset.filter(clim_koppen=clim_koppen)
            
        # Filtro per ecozona di Shultz
        eco_shultz = self.request.query_params.get('eco_shultz', None)
        if eco_shultz is not None:
            queryset = queryset.filter(eco_shultz=eco_shultz)
            
        # Filtro per stagione
        season = self.request.query_params.get('season', None)
        if season is not None:
            queryset = queryset.filter(season=season)
            
        # Filtro per condizioni meteorologiche attuali
        curr_weath = self.request.query_params.get('curr_weath', None)
        if curr_weath is not None:
            queryset = queryset.filter(curr_weath=curr_weath)
            
        # Filtro per condizioni meteorologiche passate
        past_weath = self.request.query_params.get('past_weath', None)
        if past_weath is not None:
            queryset = queryset.filter(past_weath=past_weath)
            
        # Filtro per regime di temperatura del suolo
        soil_temp = self.request.query_params.get('soil_temp', None)
        if soil_temp is not None:
            queryset = queryset.filter(soil_temp=soil_temp)
            
        # Filtro per regime di umidità del suolo
        soil_moist = self.request.query_params.get('soil_moist', None)
        if soil_moist is not None:
            queryset = queryset.filter(soil_moist=soil_moist)
            
        return queryset

class CultivatedViewSet(viewsets.ModelViewSet):
    queryset = Cultivated.objects.all()
    serializer_class = CultivatedSerializer
    permission_classes = [permissions.IsAdminUser ]
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except serializers.ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        """
    def get_queryset(self):
        queryset = Cultivated.objects.all()
        type = self.request.query_params.get('type', None)
        actual = self.request.query_params.get('actual', None)
        last = self.request.query_params.get('last', None)
        area_min = self.request.query_params.get('area_min', None)
        area_max = self.request.query_params.get('area_max', None)
        prod_tech = self.request.query_params.get('prod_tech', None)
        rotation = self.request.query_params.get('rotation', None)
        _from = self.request.query_params.get('cessation_from', None)
        _to = self.request.query_params.get('cessation_to', None)
        if area_min:
            queryset = queryset.filter(area__gte=area_min)
        if area_max:
            queryset = queryset.filter(area__lte=area_max)
        if type:
            queryset = queryset.filter(type=type)
        if actual:
            queryset = queryset.filter(actual1=actual) | \
                      queryset.filter(actual2=actual) | \
                      queryset.filter(actual3=actual)
        if last:
            queryset = queryset.filter(last1=last) | \
                      queryset.filter(last2=last) | \
                      queryset.filter(last3=last)
        if rotation:
            queryset = queryset.filter(rotation1=rotation) | \
                      queryset.filter(rotation2=rotation) | \
                      queryset.filter(rotation3=rotation)
        if prod_tech:
            queryset = queryset.filter(prod1_tech=prod_tech) | \
                      queryset.filter(prod2_tech=prod_tech) | \
                      queryset.filter(prod3_tech=prod_tech)
        if _from:
            queryset = queryset.filter(cessation__gte=_from)
        if _to:
            queryset = queryset.filter(cessation__lte=_to)    
        return queryset

class LandUseViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le informazioni sull'uso del suolo.
    """
    queryset = LandUse.objects.all()
    serializer_class = LandUseSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le informazioni sull'uso del suolo in base ai parametri di query.
        """
        queryset = LandUse.objects.all()
        
        # Filtro per uso del suolo
        land_use = self.request.query_params.get('land_use', None)
        if land_use is not None:
            queryset = queryset.filter(land_use=land_use)
            
        # Filtro per classificazione Corine
        corine = self.request.query_params.get('corine', None)
        if corine is not None:
            queryset = queryset.filter(corine=corine)
            
        return queryset

class NotCultivatedViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = Genealogy.objects.all()
    serializer_class = NotCultivatedSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = NotCultivated.objects.all()
        code = self.request.query_params.get('code', None)
        veget1 = self.request.query_params.get('veget1', None)
        veget2 = self.request.query_params.get('veget2', None)
        veget3 = self.request.query_params.get('veget3', None)
        avg_height_min = self.request.query_params.get('avg_height_min', None)
        avg_height_max = self.request.query_params.get('avg_height_max', None)
        max_height_min = self.request.query_params.get('max_height_min', None)
        max_height_max = self.request.query_params.get('max_height_max', None)
        area_min = self.request.query_params.get('area_min', None)
        area_max = self.request.query_params.get('area_min', None)
        specie = self.request.query_params.get('specie', None)
        
        # Filtro per codice
        if code is not None:
            queryset = queryset.filter(code=code)   
        if area_min:
            queryset = queryset.filter(vegetation_area__gte=area_min)
        if area_max:
            queryset = queryset.filter(vegetation_area__lte=area_max)
        if avg_height_min:
            queryset = queryset.filter(avg_height__gte=avg_height_min)
        if avg_height_max:
            queryset = queryset.filter(avg_height__lte=avg_height_max)
        if max_height_min:
            queryset = queryset.filter(max_height__gte=max_height_min)
        if max_height_max:
            queryset = queryset.filter(max_height__lte=max_height_max)
        if veget1:
            queryset = queryset.filter(veget1=veget1)
        if veget2:
            queryset = queryset.filter(veget2=veget2)
        if veget3:
            queryset = queryset.filter(veget3=veget3)
        if specie:
            queryset = queryset.filter(species1=specie) | \
                      queryset.filter(species2=specie) | \
                      queryset.filter(species3=specie)
        return queryset
    
class SurfaceViewSet(viewsets.ModelViewSet):
    """ 
    API endpoint che permette di visualizzare e modificare le caratteristiche della superficie.
    """
    queryset = Surface.objects.all()
    serializer_class = SurfaceSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le caratteristiche della superficie in base ai parametri di query.
        """
        queryset = Surface.objects.all()
        
        code = self.request.query_params.get('code', None)
        crust_area_min = self.request.query_params.get('crust_area_min', None)
        crust_area_max = self.request.query_params.get('crust_area_max', None)
        outc_area_min = self.request.query_params.get('outc_area_min', None)
        outc_area_max = self.request.query_params.get('outc_area_max', None)
        ground_form = self.request.query_params.get('ground_form', None)
        tech_alter = self.request.query_params.get('tech_alter', None)
        bedr_form = self.request.query_params.get('bedr_form', None)
        bedr_lith = self.request.query_params.get('bedr_lith', None)
        outc_dist_min = self.request.query_params.get('outc_dist_min', None)
        outc_dist_max = self.request.query_params.get('outc_dist_max', None)
        outc_size_min = self.request.query_params.get('outc_size_min', None)
        outc_size_max = self.request.query_params.get('outc_size_max', None)
        ground_wat_min = self.request.query_params.get('ground_wat_min', None)
        ground_wat_max = self.request.query_params.get('ground_wat_max', None)
        desert_var_min = self.request.query_params.get('desert_var_min', None)
        desert_var_max = self.request.query_params.get('desert_var_max', None)
        desert_ven_min = self.request.query_params.get('desert_ven_min', None)
        desert_ven_max = self.request.query_params.get('desert_ven_max', None)
        wat_above = self.request.query_params.get('wat_above', None)
        wat_repell = self.request.query_params.get('wat_repell', None)
        wat_drain = self.request.query_params.get('wat_drain', None)
        
        if code is not None:
            queryset = queryset.filter(code=code)   
        if crust_area_min:
            queryset = queryset.filter(crust_area__gte=crust_area_min)
        if crust_area_max:
            queryset = queryset.filter(crust_area__lte=crust_area_max)
        if outc_area_min:
            queryset = queryset.filter(outc_area__gte=outc_area_min)
        if outc_area_max:
            queryset = queryset.filter(outc_area__lte=outc_area_max)
        if outc_dist_min:
            queryset = queryset.filter(outc_dist__gte=outc_dist_min)
        if outc_dist_max:
            queryset = queryset.filter(outc_dist__lte=outc_dist_max)
        if outc_size_min:
            queryset = queryset.filter(outc_size__gte=outc_size_min)
        if outc_size_max:
            queryset = queryset.filter(outc_size__lte=outc_size_max)
        if ground_wat_min:
            queryset = queryset.filter(ground_wat__gte=ground_wat_min)
        if ground_wat_max:
            queryset = queryset.filter(ground_wat__lte=ground_wat_min)
        if desert_ven_min:
            queryset = queryset.filter(desert_ven__gte=desert_ven_min)
        if desert_ven_max:
            queryset = queryset.filter(desert_ven__lte=desert_ven_max)
        if desert_var_min:
            queryset = queryset.filter(desert_var__gte=desert_var_min)
        if desert_var_max:
            queryset = queryset.filter(desert_var__lte=desert_var_max)
        if ground_form is not None:
            queryset = queryset.filter(ground_form=ground_form)
        if tech_alter is not None:
            queryset = queryset.filter(tech_alter=tech_alter)
        if bedr_form is not None:
            queryset = queryset.filter(bedr_form__icontains=bedr_form)
        if bedr_lith is not None:
            queryset = queryset.filter(bedr_lith=bedr_lith)
        if wat_above is not None:
            queryset = queryset.filter(wat_above=wat_above)
        if wat_drain is not None:
            queryset = queryset.filter(wat_drain=wat_drain)
        if wat_repell is not None:
            queryset = queryset.filter(wat_repell=wat_repell)
        
        return queryset

class SurfaceCracksViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = SurfaceCracks.objects.all()
    serializer_class = SurfaceCracksSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = SurfaceCracks.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        width1 = self.request.query_params.get('width1', None)
        if width1 is not None:
            queryset = queryset.filter(width1=width1)
        dist1 = self.request.query_params.get('dist1', None)
        if dist1 is not None:
            queryset = queryset.filter(dist1=dist1)
        spat_arr1 = self.request.query_params.get('spat_arr1', None)
        if spat_arr1 is not None:
            queryset = queryset.filter(spat_arr1=spat_arr1)
        persist1 = self.request.query_params.get('persist1', None)
        if persist1 is not None:
            queryset = queryset.filter(persist1=persist1)
        width2 = self.request.query_params.get('width2', None)
        if width2 is not None:
            queryset = queryset.filter(width2=width2)
        dist2 = self.request.query_params.get('dist2', None)
        if dist2 is not None:
            queryset = queryset.filter(dist2=dist2)
        spat_arr2 = self.request.query_params.get('spat_arr2', None)
        if spat_arr2 is not None:
            queryset = queryset.filter(spat_arr2=spat_arr2)
        persist2 = self.request.query_params.get('persist2', None)
        if persist2 is not None:
            queryset = queryset.filter(persist2=persist2)
            
            
        return queryset

class LitterLayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = LitterLayer.objects.all()
    serializer_class = LitterLayerSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LitterLayer.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        avg_thick_min = self.request.query_params.get('avg_thick_min', None)
        avg_thick_max = self.request.query_params.get('avg_thick_max', None)
        if avg_thick_min:
            queryset = queryset.filter(avg_thick__gte=avg_thick_min)
        if avg_thick_max:
            queryset = queryset.filter(avg_thick__lte=avg_thick_max)
        area_min = self.request.query_params.get('area_min', None)
        area_max = self.request.query_params.get('area_max', None)
        if area_min:
            queryset = queryset.filter(area__gte=area_min)
        if area_max:
            queryset = queryset.filter(area__lte=area_max)
        max_thick_min = self.request.query_params.get('max_thick_min', None)
        max_thick_max = self.request.query_params.get('max_thick_max', None)
        if max_thick_min:
            queryset = queryset.filter(max_thick_min__gte=max_thick_min)
        if max_thick_max:
            queryset = queryset.filter(max_thick_min__lte=max_thick_max)
        return queryset

class SurfaceUnevennessViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = SurfaceUnevenness.objects.all()
    serializer_class = SurfaceUnevennessSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = SurfaceUnevenness.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        position = self.request.query_params.get('position', None)
        if position is not None:
            queryset = queryset.filter(position=position)
        nat_type = self.request.query_params.get('nat_type', None)
        if nat_type is not None:
            queryset = queryset.filter(nat_type=nat_type)
        hum_type1 = self.request.query_params.get('hum_type1', None)
        if hum_type1 is not None:
            queryset = queryset.filter(hum_type1=hum_type1)
        hum_type_2 = self.request.query_params.get('hum_type_2', None)
        if hum_type_2 is not None:
            queryset = queryset.filter(hum_type_2=hum_type_2)
        ero_type = self.request.query_params.get('ero_type', None)
        if ero_type is not None:
            queryset = queryset.filter(ero_type=ero_type)
        ero_degree = self.request.query_params.get('ero_degree', None)
        if ero_degree is not None:
            queryset = queryset.filter(ero_degree=ero_degree)
        ero_activity = self.request.query_params.get('ero_activity', None)
        if ero_activity is not None:
            queryset = queryset.filter(ero_activity=ero_activity)
        nat_avg_h_min = self.request.query_params.get('nat_avg_h_min', None)
        nat_avg_h_max = self.request.query_params.get('nat_avg_h_max', None)
        if nat_avg_h_min:
            queryset = queryset.filter(nat_avg_h__gte=nat_avg_h_min)
        if nat_avg_h_max:
            queryset = queryset.filter(nat_avg_h__lte=nat_avg_h_max)
        nat_elev_min = self.request.query_params.get('nat_elev_min', None)
        nat_elev_max = self.request.query_params.get('nat_elev_max', None)
        if nat_elev_min:
            queryset = queryset.filter(nat_elev__gte=nat_elev_min)
        if nat_elev_max:
            queryset = queryset.filter(nat_elev__lte=nat_elev_max)
        nat_dist_min = self.request.query_params.get('nat_dist_min', None)
        nat_dist_max = self.request.query_params.get('nat_dist_max', None)
        if nat_dist_min:
            queryset = queryset.filter(nat_dist__gte=nat_dist_min)
        if nat_dist_max:
            queryset = queryset.filter(nat_dist__lte=nat_dist_max)
        hum_ter_h_min = self.request.query_params.get('hum_ter_h_min', None)
        hum_ter_h_max = self.request.query_params.get('hum_ter_h_max', None)
        if hum_ter_h_min:
            queryset = queryset.filter(hum_ter_h__gte=hum_ter_h_min)
        if hum_ter_h_max:
            queryset = queryset.filter(hum_ter_h__lte=hum_ter_h_max)
        hum_noter_h_min = self.request.query_params.get('hum_noter_h_min', None)
        hum_noter_h_max = self.request.query_params.get('hum_noter_h_max', None)
        if hum_noter_h_min:
            queryset = queryset.filter(hum_noter_h__gte=hum_noter_h_min)
        if hum_noter_h_max:
            queryset = queryset.filter(hum_noter_h__lte=hum_noter_h_max)
        human_noter_w_min = self.request.query_params.get('human_noter_w_min', None)
        human_noter_w_max = self.request.query_params.get('human_noter_w_max', None)
        if human_noter_w_min:
            queryset = queryset.filter(human_noter_w__gte=human_noter_w_min)
        if human_noter_w_max:
            queryset = queryset.filter(human_noter_w__lte=human_noter_w_max)
        hum_noter_d_min = self.request.query_params.get('hum_noter_d_min', None)
        hum_noter_d_max = self.request.query_params.get('hum_noter_d_max', None)
        if hum_noter_d_min:
            queryset = queryset.filter(hum_noter_d__gte=hum_noter_d_min)
        if hum_noter_d_max:
            queryset = queryset.filter(hum_noter_d__lte=hum_noter_d_max)
        ero_area_min = self.request.query_params.get('ero_area_min', None)
        ero_area_max = self.request.query_params.get('ero_area_max', None)
        if ero_area_min:
            queryset = queryset.filter(ero_area__gte=ero_area_min)
        if ero_area_max:
            queryset = queryset.filter(ero_area__lte=ero_area_max)
        



        return queryset

class CoarseFragmentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare CoarseFragments.
    """
    queryset = CoarseFragments.objects.all()
    serializer_class = CoarseFragmentsSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        queryset = CoarseFragments.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
        total_area_min = self.request.query_params.get('total_area_min', None)
        total_area_max = self.request.query_params.get('total_area_max', None)
        if total_area_min:
            queryset = queryset.filter(total_area__gte=total_area_min)
        if total_area_max:
            queryset = queryset.filter(total_area__lte=total_area_max)
        class1_size = self.request.query_params.get('class1_size', None)
        if class1_size:
            queryset = queryset.filter(class1_size=class1_size)
        class2_size = self.request.query_params.get('class2_size', None)
        if class2_size:
            queryset = queryset.filter(class2_size=class2_size)
        class3_size = self.request.query_params.get('class3_size', None)
        if class3_size:
            queryset = queryset.filter(class3_size=class3_size)
        
        return queryset
###########################
# Profile Layer
###########################

class ProfileLayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = Genealogy.objects.all()
    serializer_class = ProfileLayerSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = ProfileLayer.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)

        # Filtro per codice
        profile = self.request.query_params.get('profile', None)
        if profile is not None:
            queryset = queryset.filter(profile=profile)

        # Filtro per codice
        number = self.request.query_params.get('number', None)
        if number is not None:
            queryset = queryset.filter(number=number)
        
        # Filtro per codice
        design = self.request.query_params.get('design', None)
        if design is not None:
            queryset = queryset.filter(design=design)
          
        depth = self.request.query_params.get('depth', None)
        if depth:
            queryset = queryset.filter(upper__lte=depth)
        if depth:
            queryset = queryset.filter(lower__gte=depth)
        
        return queryset

#########################################
## Lab Data 
#########################################

class LabDataMeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = Genealogy.objects.all()
    serializer_class = LabDataMeasurementSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LabDataMeasurement.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
            
        return queryset

class LabDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = LabData.objects.all()
    serializer_class = LabDataSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LabData.objects.all()
        
        # Filtro per codice
        code = self.request.query_params.get('code', None)
        if code is not None:
            queryset = queryset.filter(code=code)
            
        return queryset




