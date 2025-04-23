from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from backoffice.models import ProfileGeneral, Taxonomy, Project, Genealogy, LandformTopography, ClimateAndWeather, Surface, LandUse, Cultivated
from .serializers import ProfileGeneralSerializer, TaxonomySerializer, ProjectSerializer, GenealogySerializer, LandformTopographySerializer, ClimateAndWeatherSerializer, SurfaceSerializer, LandUseSerializer, CultivatedSerializer
from rest_framework import serializers

# Create your views here.

class ProfileGeneralViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare i profili del suolo.
    """
    queryset = ProfileGeneral.objects.all()
    serializer_class = ProfileGeneralSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ProfileGeneral.objects.all()
        
        # Filtri per codice e data
        code = self.request.query_params.get('code', None)
        date = self.request.query_params.get('date', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        # Filtri per posizione
        lat = self.request.query_params.get('lat', None)
        lon = self.request.query_params.get('lon', None)
        location_name = self.request.query_params.get('location_name', None)
        
        # Filtri per elevazione
        elevation_min = self.request.query_params.get('elevation_min', None)
        elevation_max = self.request.query_params.get('elevation_max', None)
        
        # Filtri per progetto e classificazione
        project = self.request.query_params.get('project', None)
        classification_sys = self.request.query_params.get('classification_sys', None)
        
        # Filtri per uso del suolo
        land_use = self.request.query_params.get('land_use', None)
        corine = self.request.query_params.get('corine', None)
        
        # Filtri per clima
        climate_koppen = self.request.query_params.get('climate_koppen', None)
        ecozone_shultz = self.request.query_params.get('ecozone_shultz', None)
        
        # Applicazione dei filtri
        if code:
            queryset = queryset.filter(code=code)
        if date:
            queryset = queryset.filter(date=date)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if lat:
            queryset = queryset.filter(lat_wgs84=lat)
        if lon:
            queryset = queryset.filter(lon_wgs84=lon)
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
        if land_use:
            queryset = queryset.filter(landuse__land_use=land_use)
        if corine:
            queryset = queryset.filter(landuse__corine=corine)
        if climate_koppen:
            queryset = queryset.filter(climate_weather__climate_koppen=climate_koppen)
        if ecozone_shultz:
            queryset = queryset.filter(climate_weather__ecozone_shultz=ecozone_shultz)
            
        return queryset

class TaxonomyViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le tassonomie.
    """
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer
    permission_classes = [permissions.IsAuthenticated]

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
        super_category = self.request.query_params.get('super', None)
        if super_category is not None:
            queryset = queryset.filter(super=super_category)
            
        return queryset

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare i progetti.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

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
        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description__icontains=description)
            
        return queryset

class GenealogyViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le genealogie.
    """
    queryset = Genealogy.objects.all()
    serializer_class = GenealogySerializer
    permission_classes = [permissions.IsAuthenticated]

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
            
        # Filtro per data
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(date=date)
            
        return queryset

class LandformTopographyViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le caratteristiche topografiche del terreno.
    """
    queryset = LandformTopography.objects.all()
    serializer_class = LandformTopographySerializer
    permission_classes = [permissions.IsAuthenticated]

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
            gradient_upslope = self.request.query_params.get('gradient_upslope', None)
            if gradient_upslope is not None:
                queryset = queryset.filter(gradient_upslope=gradient_upslope)
                
            # Filtro per gradiente in discesa
            gradient_downslope = self.request.query_params.get('gradient_downslope', None)
            if gradient_downslope is not None:
                queryset = queryset.filter(gradient_downslope=gradient_downslope)
                
            # Filtro per forma del pendio
            slope_shape = self.request.query_params.get('slope_shape', None)
            if slope_shape is not None:
                queryset = queryset.filter(slope_shape=slope_shape)
                
            # Filtro per posizione del profilo
            profile_position = self.request.query_params.get('profile_position', None)
            if profile_position is not None:
                queryset = queryset.filter(profile_position=profile_position)
                
            return queryset

class ClimateAndWeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le informazioni climatiche e meteorologiche.
    """
    queryset = ClimateAndWeather.objects.all()
    serializer_class = ClimateAndWeatherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra le informazioni climatiche e meteorologiche in base ai parametri di query.
        """
        queryset = ClimateAndWeather.objects.all()
        
        # Filtro per classificazione climatica di Köppen
        climate_koppen = self.request.query_params.get('climate_koppen', None)
        if climate_koppen is not None:
            queryset = queryset.filter(climate_koppen=climate_koppen)
            
        # Filtro per ecozona di Shultz
        ecozone_shultz = self.request.query_params.get('ecozone_shultz', None)
        if ecozone_shultz is not None:
            queryset = queryset.filter(ecozone_shultz=ecozone_shultz)
            
        # Filtro per stagione
        season = self.request.query_params.get('season', None)
        if season is not None:
            queryset = queryset.filter(season=season)
            
        # Filtro per condizioni meteorologiche attuali
        current_weather = self.request.query_params.get('current_weather', None)
        if current_weather is not None:
            queryset = queryset.filter(current_weather=current_weather)
            
        # Filtro per condizioni meteorologiche passate
        past_weather = self.request.query_params.get('past_weather', None)
        if past_weather is not None:
            queryset = queryset.filter(past_weather=past_weather)
            
        # Filtro per regime di temperatura del suolo
        soil_temp_regime = self.request.query_params.get('soil_temp_regime', None)
        if soil_temp_regime is not None:
            queryset = queryset.filter(soil_temp_regime=soil_temp_regime)
            
        # Filtro per regime di umidità del suolo
        soil_moist_regime = self.request.query_params.get('soil_moist_regime', None)
        if soil_moist_regime is not None:
            queryset = queryset.filter(soil_moist_regime=soil_moist_regime)
            
        return queryset

class SurfaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le caratteristiche della superficie.
    """
    queryset = Surface.objects.all()
    serializer_class = SurfaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filtra le caratteristiche della superficie in base ai parametri di query.
        """
        queryset = Surface.objects.all()
        
        # Filtro per area delle croste superficiali
        surface_crusts_area = self.request.query_params.get('surface_crusts_area', None)
        if surface_crusts_area is not None:
            queryset = queryset.filter(surface_crusts_area=surface_crusts_area)
            
        # Filtro per forma del terreno modellato
        patterned_ground_form = self.request.query_params.get('patterned_ground_form', None)
        if patterned_ground_form is not None:
            queryset = queryset.filter(patterned_ground_form=patterned_ground_form)
            
        # Filtro per alterazione tecnica della superficie
        technical_surface_alteration = self.request.query_params.get('technical_surface_alteration', None)
        if technical_surface_alteration is not None:
            queryset = queryset.filter(technical_surface_alteration=technical_surface_alteration)
            
        # Filtro per nome della formazione rocciosa
        bedrock_formation_name = self.request.query_params.get('bedrock_formation_name', None)
        if bedrock_formation_name is not None:
            queryset = queryset.filter(bedrock_formation_name__icontains=bedrock_formation_name)
            
        # Filtro per litologia del substrato roccioso
        bedrock_lithology = self.request.query_params.get('bedrock_lithology', None)
        if bedrock_lithology is not None:
            queryset = queryset.filter(bedrock_lithology=bedrock_lithology)
            
        # Filtro per area coperta da affioramenti
        outcrops_area_covered = self.request.query_params.get('outcrops_area_covered', None)
        if outcrops_area_covered is not None:
            queryset = queryset.filter(outcrops_area_covered=outcrops_area_covered)
            
        # Filtro per profondità della falda acquifera
        ground_water_depth = self.request.query_params.get('ground_water_depth', None)
        if ground_water_depth is not None:
            queryset = queryset.filter(ground_water_depth=ground_water_depth)
            
        # Filtro per acqua sopra la superficie
        water_above_surface = self.request.query_params.get('water_above_surface', None)
        if water_above_surface is not None:
            queryset = queryset.filter(water_above_surface=water_above_surface)
            
        # Filtro per condizioni di drenaggio dell'acqua
        water_drainage_condition = self.request.query_params.get('water_drainage_condition', None)
        if water_drainage_condition is not None:
            queryset = queryset.filter(water_drainage_condition=water_drainage_condition)
            
        # Filtro per tipo di repellenza all'acqua
        water_repellence_type = self.request.query_params.get('water_repellence_type', None)
        if water_repellence_type is not None:
            queryset = queryset.filter(water_repellence_type=water_repellence_type)
            
        # Filtro per ventifatti del deserto
        desert_ventifacts = self.request.query_params.get('desert_ventifacts', None)
        if desert_ventifacts is not None:
            queryset = queryset.filter(desert_ventifacts=desert_ventifacts)
            
        # Filtro per vernice del deserto
        desert_varnish = self.request.query_params.get('desert_varnish', None)
        if desert_varnish is not None:
            queryset = queryset.filter(desert_varnish=desert_varnish)
            
        return queryset

class LandUseViewSet(viewsets.ModelViewSet):
    """
    API endpoint che permette di visualizzare e modificare le informazioni sull'uso del suolo.
    """
    queryset = LandUse.objects.all()
    serializer_class = LandUseSerializer
    permission_classes = [permissions.IsAuthenticated]

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

class CultivatedViewSet(viewsets.ModelViewSet):
    queryset = Cultivated.objects.all()
    serializer_class = CultivatedSerializer
    permission_classes = [permissions.IsAuthenticated]
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
        cultivation_type = self.request.query_params.get('cultivation_type', None)
        actual_species = self.request.query_params.get('actual_species', None)
        last_species = self.request.query_params.get('last_species', None)
        
        if cultivation_type:
            queryset = queryset.filter(cultivation_type=cultivation_type)
        if actual_species:
            queryset = queryset.filter(actual_species1=actual_species) | \
                      queryset.filter(actual_species2=actual_species) | \
                      queryset.filter(actual_species3=actual_species)
        if last_species:
            queryset = queryset.filter(last_species1=last_species) | \
                      queryset.filter(last_species2=last_species) | \
                      queryset.filter(last_species3=last_species)
            
        return queryset
