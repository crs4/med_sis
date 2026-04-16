from django.shortcuts import render
from django.http import Http404
from django.forms.models import model_to_dict
from django.core.management import call_command
from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.response import Response
from backoffice.models import *
from .serializers import *
import logging
import traceback

logger = logging.getLogger(__name__)

class UpdateLayersViewSet(viewsets.ViewSet):
    """
    API endpoint to run the updatelayers command on demand.
    """
    permission_classes = [permissions.IsAdminUser]

    def create(self, request):
        store = request.data.get("store") or "backoffice"
        skip_flag = request.data.get("skip_geonode_registered", True)
        skip_geonode_registered = str(skip_flag).lower() not in ["false", "0", "no"]

        logger.info(
            f"API for updatelayers - store: {store}, "
            f"skip_geonode_registered: {skip_geonode_registered}"
        )

        try:
            call_command(
                "updatelayers",
                store=store,
                skip_geonode_registered=skip_geonode_registered,
            )
            logger.info(f" updatelayers success for store '{store}'")
            return Response(
                {
                    "detail": (
                        f"updatelayers success for store '{store}'. "
                        f"skip_geonode_registered={skip_geonode_registered}"
                    )
                },
                status=status.HTTP_200_OK,
            )
        except SystemExit as exc:
            # Il comando updatelayers può sollevare SystemExit in caso di errori
            error_msg = str(exc) if exc.code != 0 else "Errors executing in updatelayers"
            logger.error(f"Errors in updatelayers (SystemExit): {error_msg}")
            logger.error(traceback.format_exc())
            return Response(
                {
                    "detail": (
                        f"Errors: {error_msg}. Open the log for further details. "
                    ),
                    "error_type": "SystemExit",
                    "store": store,
                    "skip_geonode_registered": skip_geonode_registered,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:
            error_traceback = traceback.format_exc()
            logger.error(f"Errore durante updatelayers: {str(exc)}")
            logger.error(error_traceback)
            
            # Estrai informazioni utili dall'errore
            error_summary = str(exc)
            if "No module named 'imp'" in error_traceback:
                error_summary = (
                    "Errore di compatibilità Python 3.12: il modulo 'imp' è stato rimosso. "
                    "Questo è un problema noto con GeoNode/pycsw. "
                    "Prova con skip_geonode_registered=true per evitare la registrazione in GeoNode."
                )
            elif "TypeError" in error_traceback and "NoneType" in error_traceback:
                error_summary = (
                    "Errore durante la registrazione in GeoNode: identificatore mancante o None. "
                    "Prova con skip_geonode_registered=true per evitare la registrazione in GeoNode."
                )
            
            return Response(
                {
                    "detail": error_summary,
                    "error_type": type(exc).__name__,
                    "store": store,
                    "skip_geonode_registered": skip_geonode_registered,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class XLSxUploadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit XLSxUpload.
    """
    queryset = XLSxUpload.objects.all()
    serializer_class = XLSxUploadSerializer
    permission_classes = [permissions.IsAdminUser ]
    
    def get_queryset(self):
        """
        Filtra 
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

        # Filtro per status
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset
    
    def list(self, request):
        queryset = XLSxUpload.objects.all()
        serializer = XLSxUploadSerializer(queryset, many=True)
        for item in serializer.data:
            item.pop('data')
            item.pop('report')
        return Response(serializer.data)
    
###########################
# Projects for Genealogy
###########################
class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Projects metadata.
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
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
            
        # Filtro per titolo
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
            
        # Filtro per descrizione
        descr = self.request.query_params.get('description', None)
        if descr is not None:
            queryset = queryset.filter(descr__icontains=descr)
            
        return queryset

###########################
# Point General
###########################
class PointGeneralViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Project Soil Point Data General Info.
    """
    queryset = PointGeneral.objects.all()
    serializer_class = PointGeneralSerializer
    permission_classes = [permissions.IsAdminUser ]
    
    
    def get_queryset(self):
        queryset = PointGeneral.objects.all()
        # Filtri per codice e data
        date = self.request.query_params.get('date', None)
        _from = self.request.query_params.get('from', None)
        _to = self.request.query_params.get('to', None)

        # Filtri per location_name
        location = self.request.query_params.get('location', None)
        
        # Filtri per elevazione
        elev_min = self.request.query_params.get('elev_min', None)
        elev_max = self.request.query_params.get('elev_max', None)
        
        # Filtri per progetto e classificazione
        project = self.request.query_params.get('project', None)
        cls_sys = self.request.query_params.get('cls_sys', None)
        
        # Filtri per note
        text = self.request.query_params.get('note', None)
        if text is not None:
            queryset = queryset.filter(notes__icontains=text)
        
        # Applicazione dei filtri
        if date:
            queryset = queryset.filter(date=date)
        if _from:
            queryset = queryset.filter(date__gte=_from)
        if _to:
            queryset = queryset.filter(date__lte=_to)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if elev_min:
            queryset = queryset.filter(elev_m_asl__gte=elev_min)
        if elev_max:
            queryset = queryset.filter(elev_m_asl__lte=elev_max)
        if project:
            queryset = queryset.filter(project=project)
        if cls_sys:
            queryset = queryset.filter(cls_sys=cls_sys)
            
        return queryset

    def delete(self):
        prj =self.request.query_params.get('prj')
        if prj:
            queryset = PointGeneral.objects.all().filter(project=prj)
            queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
       
class LandformTopographyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Land form and topography.
    """
    queryset = LandformTopography.objects.all()
    serializer_class = LandformTopographySerializer
    permission_classes = [permissions.IsAdminUser ]

    
    def get_queryset(self):
            """
            Filtra le caratteristiche topografiche in base ai parametri di query.
            """
            queryset = LandformTopography.objects.all()
            
            id = self.request.query_params.get('id', None)
            if id is not None:
                queryset = queryset.filter(id=id)
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
            
            
            return queryset
 
class ClimateAndWeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Climate And Weather data.
    """
    queryset = ClimateAndWeather.objects.all()
    serializer_class = ClimateAndWeatherSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le informazioni climatiche e meteorologiche in base ai parametri di query.
        """
        queryset = ClimateAndWeather.objects.all()
        
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
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

class LandUseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Land Use data.
    """
    queryset = LandUse.objects.all()
    serializer_class = LandUseSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le informazioni sull'uso del suolo in base ai parametri di query.
        """
        queryset = LandUse.objects.all()
        
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        land_use = self.request.query_params.get('land_use', None)
        if land_use is not None:
            queryset = queryset.filter(land_use=land_use)
            
        # Filtro per classificazione Corine
        corine = self.request.query_params.get('corine', None)
        if corine is not None:
            queryset = queryset.filter(corine=corine)
            
        return queryset
    
class SurfaceViewSet(viewsets.ModelViewSet):
    """ 
    API endpoint that allows you to view and edit Surface data.
    """
    queryset = Surface.objects.all()
    serializer_class = SurfaceSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le caratteristiche della superficie in base ai parametri di query.
        """
        queryset = Surface.objects.all()
        
        id = self.request.query_params.get('id', None)
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
        
        if id is not None:
            queryset = queryset.filter(id=id)
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

class SurfaceUnevennessViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Surface Unevenness data.
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
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
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

###########################
# Point Layer
###########################

class PointLayerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer descriptions data.
    """
    queryset = PointLayer.objects.all()
    serializer_class = PointLayerSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = PointLayer.objects.all()
        
        # Filtro per codice
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        # Filtro per codice
        point = self.request.query_params.get('point', None)
        if point is not None:
            queryset = queryset.filter(point=point)

        # Filtro per codice
        number = self.request.query_params.get('number', None)
        if number is not None:
            queryset = queryset.filter(number=number)
        
        # Filtro per codice
        horizon = self.request.query_params.get('horizon', None)
        if horizon is not None:
            queryset = queryset.filter(horizon=horizon)
          
        # Filtro per codice
        project = self.request.query_params.get('project', None)
        if project is not None:
            queryset = queryset.filter(project=project)
        
        return queryset

class LayerRemnantsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Remnants data.
    """
    queryset = LayerRemnants.objects.all()
    serializer_class = LayerRemnantsSerializer 
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerRemnants.objects.all()
        return queryset
    
class LayerCoarseFragmentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Coarse Fragments data.
    """
    queryset = LayerCoarseFragments.objects.all()
    serializer_class = LayerCoarseFragmentsSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerCoarseFragments.objects.all()
        return queryset

class LayerArtefactsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Artefacts data.
    """
    queryset = LayerArtefacts.objects.all()
    serializer_class = LayerArtefactsSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerArtefacts.objects.all()
        return queryset

class LayerSecondarySilicaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Secondary Silica data.
    """
    queryset = LayerSecondarySilica.objects.all()
    serializer_class = LayerSecondarySilicaSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerSecondarySilica.objects.all()
        return queryset

class LayerGypsumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Gypsum data.
    """
    queryset = LayerGypsum.objects.all()
    serializer_class = LayerGypsumSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerGypsum.objects.all()
        return queryset

class LayerCarbonatesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Carbonates data.
    """
    queryset = LayerCarbonates.objects.all()
    serializer_class = LayerCarbonatesSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerCarbonates.objects.all()
        return queryset
    
class LayerCoatingsBridgesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Coatings Bridges  data.
    """
    queryset = LayerCoatingsBridges.objects.all()
    serializer_class = LayerCoatingsBridgesSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerCoatingsBridges.objects.all()
        return queryset

class LayerRedoximorphicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Redoximorphic data.
    """
    queryset = LayerRedoximorphic.objects.all()
    serializer_class = LayerRedoximorphicSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerRedoximorphic.objects.all()
        return queryset

class LayerLithogenicVariegatesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Lithogenic Variegates data.
    """
    queryset = LayerLithogenicVariegates.objects.all()
    serializer_class = LayerLithogenicVariegatesSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerLithogenicVariegates.objects.all()
        return queryset

class LayerMatrixColoursViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Matrix Colours data.
    """
    queryset = LayerMatrixColours.objects.all()
    serializer_class = LayerMatrixColoursSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerMatrixColours.objects.all()
        return queryset

class LayerCracksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Cracks data.
    """
    queryset = LayerCracks.objects.all()
    serializer_class = LayerCracksSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerCracks.objects.all()
        return queryset

class LayerStructureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Structure data.
    """
    queryset = LayerStructure.objects.all()
    serializer_class = LayerStructureSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerStructure.objects.all()

        # Filtro per codice
        id = self.request.query_params.get('id', None)
        layer = self.request.query_params.get('layer', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        if layer is not None:
            queryset = queryset.filter(layer=layer)
            
        return queryset

class LayerNonMatrixPoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer NonMatrix Pore data.
    """
    queryset = LayerNonMatrixPore.objects.all()
    serializer_class = LayerNonMatrixPoreSerializer
    permission_classes = [permissions.IsAdminUser ]

class LayerDegreeDecompositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Degree Decomposition data.
    """
    queryset = LayerDegreeDecomposition.objects.all()
    serializer_class = LayerDegreeDecompositionSerializer
    permission_classes = [permissions.IsAdminUser ]

class LayerHumanAlterationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Human Alterations data.
    """
    queryset = LayerHumanAlterations.objects.all()
    serializer_class = LayerHumanAlterationsSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerHumanAlterations.objects.all()
        return queryset

class LayerAnimalActivityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Animal Activity data.
    """
    queryset = LayerAnimalActivity.objects.all()
    serializer_class = LayerAnimalActivitySerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerAnimalActivity.objects.all()
        return queryset

class LayerRootsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Roots data.
    """
    queryset = LayerRoots.objects.all()
    serializer_class = LayerRootsSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerRoots.objects.all()
        return queryset

class LayerOrganicCarbonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Organic Carbon.
    """
    queryset = LayerOrganicCarbon.objects.all()
    serializer_class = LayerOrganicCarbonSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerOrganicCarbon.objects.all()
        return queryset

class LayerPermafrostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Permafrost.
    """
    queryset = LayerPermafrost.objects.all()
    serializer_class = LayerPermafrostSerializer 
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerPermafrost.objects.all()
        return queryset

class LayerConsistenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Layer Consistence.
    """
    queryset = LayerConsistence.objects.all()
    serializer_class = LayerConsistenceSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LayerConsistence.objects.all()
        return queryset

#########################################
## Lab Data 
#########################################

class LabDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit Laboratory data.
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
        id = self.request.query_params.get('id', None)
        pt = self.request.query_params.get('point', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        if pt is not None:
            queryset = queryset.filter(point=pt)
            
        return queryset

#########################################
## Datasets 
#########################################   
class DatasetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit XLSxUpload.
    """
    queryset = Dataset.objects.all() 
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAdminUser ]
    
    def get_queryset(self):
        """
        Filtra 
        """
        queryset = XLSxUpload.objects.all()
        
        # Name Filter 
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)
            
        # User name Filter
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(user=user)

        # User email Filter
        user_email = self.request.query_params.get('email', None)
        if user_email is not None:
            queryset = queryset.filter(user_email=user_email)

        # Status Filter
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)

        return queryset
    
    def list(self, request):
        queryset = Dataset.objects.all()
        serializer = DatasetSerializer(queryset, many=True)
        for item in serializer.data:
            item.pop('filter')
            item.pop('points')
            item.pop('k_variogram')
            item.pop('k_data')
        return Response(serializer.data)
    
#########################################
## Photos 
#########################################
   
class PhotoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit photos metadata.
    """
    queryset = Photo.objects.all() 
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = Photo.objects.all()

        # Filtro per codice
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        return queryset

#########################################
## LabDataExtraMeasure 
#########################################
class LabDataExtraMeasureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit laboratory extra measures data.
    """
    queryset = LabDataExtraMeasure.objects.all() 
    serializer_class = LabDataExtraMeasureSerializer  
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = LabDataExtraMeasure.objects.all()

        # Filtro per codice
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        t = self.request.query_params.get('labdata', None)
        if t is not None:
            queryset = queryset.filter(labdata=t)
        m = self.request.query_params.get('measure', None)
        if m is not None:
            queryset = queryset.filter(measure=m)
        p = self.request.query_params.get('point', None)
        if p is not None:
            queryset = queryset.filter(point=p)
 
        return queryset
#########################################
## Taxonomy 
#########################################
   
class TaxonomyValueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit classes of taxonomies .
    """
    queryset = TaxonomyValue.objects.all() 
    serializer_class = TaxonomyValueSerializer  
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = TaxonomyValue.objects.all()

        # Filtro per codice
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)
        t = self.request.query_params.get('taxonomy', None)
        if t is not None:
            queryset = queryset.filter(taxonomy=t)

        return queryset
    
class TaxonomyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows you to view and edit taxonomies.
    """
    queryset = Taxonomy.objects.all() 
    serializer_class = TaxonomySerializer
    permission_classes = [permissions.IsAdminUser ]

    def get_queryset(self):
        """
        Filtra le X in base ai parametri di query.
        """
        queryset = Taxonomy.objects.all()

        # Filtro per codice
        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        return queryset

