
"""Read-only JSON-LD endpoints for MED-SIS soil observations."""

import json
import re
from urllib.parse import quote
from decimal import Decimal, ROUND_DOWN
from collections import defaultdict
from django.core.paginator import Paginator, EmptyPage

from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Exists, OuterRef

from backoffice.models import PointGeneral, VocabularyMapping, TaxonomyValue, PointLayer, LabData, Property, Procedure, ProcedureMapping

class LDTaxonomyValueView(View):
    """JSON-LD representation of a MED-SIS taxonomy value."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, taxonomy_id, value):

        taxonomy_value = get_object_or_404(
            TaxonomyValue.objects.using('backoffice'),
            pk=f'{taxonomy_id}:{value}',
        )

        document = {
            '@context': _ld_context(
                **{
                    'skos': 'http://www.w3.org/2004/02/skos/core#',
                    'xsd': 'http://www.w3.org/2001/XMLSchema#',
                }
            ),
            '@id': (
                f'medsis:ldtaxonomy-value/'
                f'{quote(taxonomy_id, safe="")}/'
                f'{quote(value, safe="")}/'
            ),
            '@type': 'skos:Concept',
            'skos:notation': {
                '@value': taxonomy_value.value,
                '@type': 'xsd:string',
            },
        }

        if taxonomy_value.descr:
            document['skos:definition'] = {
                '@value': taxonomy_value.descr,
                '@language': 'en',
            }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )


GLOSIS_LAND_USE_VOCABULARY = 'glosis-results-landUseClass'
GLOSIS_LAND_USE_VERSION = '1.9.9'

SAND_PROCEDURES = {
    'BH': 'glosis-proc:pSAProcedure-hydrometer-unkdisp',
    'LD': 'glosis-proc:pSAProcedure-laser-unkdisp',
    'PR': 'glosis-proc:pSAProcedure-pipette-unkdisp',
    'SV': 'local',
}

SILT_PROCEDURES = {
    code: uri
    for code, uri in SAND_PROCEDURES.items()
    if code in ('BH', 'LD', 'PR')
}

SAND_PROPERTIES = {
    'sand': 'glosis-cl:properties/textSandPropertyCode-Sa_ISO',
    'v-c-sand': 'glosis-cl:properties/textSandPropertyCode-vcSa_ISSS',
    'c-sand': 'coarseSand-ISO11277',
    'm-sand': 'glosis-cl:properties/textSandPropertyCode-mSa_ISSS',
    'f-sand': 'fineSand-ISO11277',
    'v-f-sand': 'glosis-cl:properties/textSandPropertyCode-vfSa_ISSS',
}

SILT_PROPERTIES = {
    'silt': 'glosis-cl:properties/textSiltPropertyCode-Si_ISO',
    'c-silt': 'glosis-cl:properties/textSiltPropertyCode-cSi_ISO',
    'f-silt': 'glosis-cl:properties/textSiltPropertyCode-fSi_ISO',
}

CLAY_PROCEDURES = SILT_PROCEDURES

MN_ZN_CU_PROCEDURES = {
    'DBF': 'local',
    'DBIA': 'local',
    'DBIM': 'local',

    'DF': 'glosis-proc:extractableElementsProcedure-Extr_dtpa',
    'DIA': 'glosis-proc:extractableElementsProcedure-Extr_dtpa',
    'DIM': 'glosis-proc:extractableElementsProcedure-Extr_dtpa',

    'EF': 'glosis-proc:extractableElementsProcedure-Extr_edta',
    'EIA': 'glosis-proc:extractableElementsProcedure-Extr_edta',
    'EIM': 'glosis-proc:extractableElementsProcedure-Extr_edta',

    'NAF': 'glosis-proc:extractableElementsProcedure-Extr_hno3',
    'NAIA': 'glosis-proc:extractableElementsProcedure-Extr_hno3',
    'NAIM': 'glosis-proc:extractableElementsProcedure-Extr_hno3',
}

MN_ZN_CU_PROPERTIES = {
    'mn': 'glosis-cl:properties/physioChemicalPropertyCode-Manext',
    'zn': 'glosis-cl:properties/physioChemicalPropertyCode-Zinext',
    'cu': 'glosis-cl:properties/physioChemicalPropertyCode-Copext',
}

def _coordinate_token(value):
    """Truncate (never round) WGS84 decimal degrees to five places."""
    truncated = Decimal(str(value)).quantize(
        Decimal('0.00001'),
        rounding=ROUND_DOWN,
    )
    return format(truncated, '.5f').replace('-', 'm').replace('.', '_')

def _plot_identifier(point):
    return (
        f'plot_lat{_coordinate_token(point.lat_wgs84)}'
        f'_lon{_coordinate_token(point.lon_wgs84)}'
    )

def _ld_context(**prefixes):
    base_url = getattr(
        settings, 'BACKOFFICE_API_BASE_URL', None
    )

    if not base_url:
        raise RuntimeError(
            'BACKOFFICE_API_BASE_URL is not configured'
        )

    return {
        'medsis': base_url.rstrip('/') + '/',
        **prefixes,
    }

def _lab_feature_of_interest(lab):
    horizon = (
        PointLayer.objects.using('backoffice')
        .filter(
            labdata_id=lab.pk,
            point_id=lab.point_id,
            point__project='SOILS4MED',
        )
        .first()
    )

    if horizon is not None:
        horizon_id = quote(str(horizon.pk), safe='@')
        return f'medsis:ldhorizon/{horizon_id}/'

    if (
        lab.horizon is None
        and lab.upper is not None
        and lab.lower is not None
    ):
        lab_id = quote(str(lab.pk), safe='@')
        return f'medsis:ldlayer/{lab_id}/'

    raise Http404(
        'No horizon or layer associated with laboratory data'
    )

class LandUseObservationView(View):
    """GET /api/backoffice/ldobservation/<profile_id>/land-use/"""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, profile_id):
        point = get_object_or_404(
            PointGeneral.objects.using('backoffice')
            .select_related('landuse__use'),
            pk=profile_id,
            project='SOILS4MED',
        )

        if (
            not point.landuse_id
            or point.landuse is None
            or not point.landuse.use_id
        ):
            raise Http404('Land-use observation not found')

        taxonomy_value = point.landuse.use

        if (
            taxonomy_value.role != TaxonomyValue.ValueRole.CONCEPT
            or taxonomy_value.taxonomy_id != 'USES'
        ):
            raise Http404('Land-use observation not found')

        mapping = (
            VocabularyMapping.objects.using('backoffice')
            .select_related('external_term')
            .filter(
                taxonomy_value_id=taxonomy_value.pk,
                relation=VocabularyMapping.Relation.EXACT,
                status=VocabularyMapping.Status.VERIFIED,
                external_term__vocabulary=GLOSIS_LAND_USE_VOCABULARY,
                external_term__version=GLOSIS_LAND_USE_VERSION,
            )
            .first()
        )

        if mapping is None:
            raise Http404('Verified land-use mapping not found')

        base_url = getattr(settings, 'BACKOFFICE_API_BASE_URL', None)

        if not base_url:
            raise RuntimeError(
                'BACKOFFICE_API_BASE_URL is not configured'
            )

        base_url = base_url.rstrip('/') + '/'

        observation_uri = f'medsis:ldobservation/{point.pk}/land-use/'
        plot_uri = f'medsis:ldplot/{_plot_identifier(point)}/'
        
        document = {
            '@context': {
                **_ld_context(
                    **{
                        'sosa': 'http://www.w3.org/ns/sosa/',
                        'glosis-sp': 'http://w3id.org/glosis/model/siteplot/',
                        'xsd': 'http://www.w3.org/2001/XMLSchema#',
                    }
                ),
                'hasFeatureOfInterest': {
                    '@id': 'sosa:hasFeatureOfInterest',
                    '@type': '@id',
                },
                'observedProperty': {
                    '@id': 'sosa:observedProperty',
                    '@type': '@id',
                },
                'hasResult': {
                    '@id': 'sosa:hasResult',
                    '@type': '@id',
                },
                'resultTime': {
                    '@id': 'sosa:resultTime',
                    '@type': 'xsd:dateTime',
                },
            },
            '@id': observation_uri,
            '@type': [
                'sosa:Observation',
                'glosis-sp:LandUseClass',
            ],
            'hasFeatureOfInterest': plot_uri,
            'observedProperty': 'glosis-sp:landUseClassProperty',
            'hasResult': mapping.external_term.uri,
        }

        if point.date is not None:
            # Conventional time: only the date is stored.
            document['resultTime'] = (
                f'{point.date.isoformat()}T00:00:00'
            )

        return HttpResponse(
            json.dumps(document, ensure_ascii=False, indent=2),
            content_type='application/ld+json; charset=utf-8',
        )

class LDPlotView(View):
    """Return a GloSIS GL_Plot as JSON-LD."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, plot_id):

        # Validate the identifier before querying the database.
        pattern = (
            r'^plot_lat(m?\d+_\d{5})'
            r'_lon(m?\d+_\d{5})$'
        )

        if not re.fullmatch(pattern, plot_id):
            raise Http404('Invalid Plot identifier')

        # Find all SOILS4MED profiles sharing this Plot.
        # Compare identifiers after truncation, not raw floats.
        points = PointGeneral.objects.using(
            'backoffice'
        ).filter(
            project='SOILS4MED'
        ).only(
            'id', 'lat_wgs84', 'lon_wgs84'
        ).order_by('id')

        matching_points = [
            point for point in points
            if _plot_identifier(point) == plot_id
        ]

        if not matching_points:
            raise Http404('Plot not found')

        base_url = getattr(
            settings, 'BACKOFFICE_API_BASE_URL', None
        )

        if not base_url:
            raise RuntimeError(
                'BACKOFFICE_API_BASE_URL is not configured'
            )

        base_url = base_url.rstrip('/') + '/'

        plot_uri = f'medsis:ldplot/{plot_id}/'
        geometry_uri = f'medsis:ldplot/{plot_id}/geometry'

        profile_uris = [
            f'medsis:ldprofile/{quote(point.pk, safe="")}/'
            for point in matching_points
        ]
        
        # Coordinates of the first matching point.
        # Use the same five-decimal truncation as the Plot ID.
        point = matching_points[0]

        latitude = (
            _coordinate_token(point.lat_wgs84).replace('m', '-').replace('_', '.')
        )
        longitude = (
            _coordinate_token(point.lon_wgs84).replace('m', '-').replace('_', '.')
        )

        wkt = (
            '<http://www.opengis.net/def/crs/OGC/1.3/CRS84> '
            f'POINT({longitude} {latitude})'
        )

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'glosis-sp': 'http://w3id.org/glosis/model/siteplot/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                        'geo': 'http://www.opengis.net/ont/geosparql#',
                    }
                ),
                'profile': {
                    '@id': 'iso28258:Plot.profile',
                    '@type': '@id',
                },
                'hasGeometry': {
                    '@id': 'geo:hasGeometry',
                    '@type': '@id',
                },
            },
            '@graph': [
                {
                    '@id': plot_uri,
                    '@type': 'glosis-sp:GL_Plot',
                    'profile': profile_uris,
                    'hasGeometry': geometry_uri,
                },
                {
                    '@id': geometry_uri,
                    '@type': 'geo:Geometry',
                    'geo:asWKT': {
                        '@type': 'geo:wktLiteral',
                        '@value': wkt,
                    },
                },
            ],
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

class LDPlotListView(View):
    """Return a paginated JSON-LD collection of GloSIS Plots."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request):
        try:
            page_size = int(request.GET.get('page_size', 50))
            page_number = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404('Invalid pagination parameters')

        if not 1 <= page_size <= 200 or page_number < 1:
            raise Http404('Invalid pagination parameters')

        points = (
            PointGeneral.objects.using('backoffice')
            .filter(project='SOILS4MED')
            .only('id', 'lat_wgs84', 'lon_wgs84')
            .order_by('id')
        )

        # Group profiles by their Plot identifier.
        plots = defaultdict(list)

        for point in points.iterator():
            plot_id = _plot_identifier(point)

            if plot_id is not None:
                plots[plot_id].append(point.pk)

        # Pagination must operate on distinct Plots.
        plot_ids = sorted(plots.keys())

        paginator = Paginator(plot_ids, page_size)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            raise Http404('Page not found')

        members = []

        for plot_id in page.object_list:
            profile_uris = [
                f'medsis:ldprofile/{quote(str(point_id), safe="")}/'
                for point_id in plots[plot_id]
            ]

            members.append({
                '@id': f'medsis:ldplot/{plot_id}/',
                '@type': 'glosis-sp:GL_Plot',
                'rdfs:label': plot_id,
                'profile': profile_uris,
            })

        def page_uri(number):
            return (
                f'medsis:ldplots/'
                f'?page={number}&page_size={page_size}'
            )

        view = {
            '@id': page_uri(page.number),
            '@type': 'hydra:PartialCollectionView',
            'hydra:first': {'@id': page_uri(1)},
            'hydra:last': {
                '@id': page_uri(paginator.num_pages)
            },
        }

        if page.has_previous():
            view['hydra:previous'] = {
                '@id': page_uri(page.previous_page_number())
            }

        if page.has_next():
            view['hydra:next'] = {
                '@id': page_uri(page.next_page_number())
            }

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'hydra': 'http://www.w3.org/ns/hydra/core#',
                        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                        'glosis-sp': 'http://w3id.org/glosis/model/siteplot/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                    }
                ),
                'profile': {
                    '@id': 'iso28258:Plot.profile',
                    '@type': '@id',
                },
            },
            '@id': 'medsis:ldplots/',
            '@type': 'hydra:Collection',
            'hydra:totalItems': paginator.count,
            'hydra:member': members,
            'hydra:view': view,
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

class LDProfileView(View):
    """Return a GloSIS GL_Profile as JSON-LD."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, profile_id):
        point = get_object_or_404(
            PointGeneral.objects.using('backoffice'),
            pk=profile_id,
            project='SOILS4MED',
        )

        base_url = getattr(
            settings, 'BACKOFFICE_API_BASE_URL', None
        )
        if not base_url:
            raise RuntimeError(
                'BACKOFFICE_API_BASE_URL is not configured'
            )

        base_url = base_url.rstrip('/') + '/'

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'glosis-pr': 'http://w3id.org/glosis/model/profile/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                    }
                ),
                'plot': {
                    '@reverse': 'iso28258:Plot.profile',
                    '@type': '@id',
                },
            },
            '@id': f'medsis:ldprofile/{point.pk}/',
            '@type': 'glosis-pr:GL_Profile',
            'plot': (
                f'medsis:ldplot/{_plot_identifier(point)}/'
            ),
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

class LDProfileListView(View):
    """Return a paginated JSON-LD collection of GloSIS Profiles."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request):
        try:
            page_size = int(request.GET.get('page_size', 50))
            page_number = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404('Invalid pagination parameters')

        if not 1 <= page_size <= 200 or page_number < 1:
            raise Http404('Invalid pagination parameters')

        points = (
            PointGeneral.objects.using('backoffice')
            .filter(project='SOILS4MED')
            .only('id', 'lat_wgs84', 'lon_wgs84')
            .order_by('id')
        )

        paginator = Paginator(points, page_size)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            raise Http404('Page not found')

        profile_ids = [point.pk for point in page.object_list]

        layers_by_profile = {
            profile_id: []
            for profile_id in profile_ids
        }

        layers = (
            LabData.objects.using('backoffice')
            .filter(
                point_id__in=profile_ids,
                point__project='SOILS4MED',
                horizon__isnull=True,
                upper__isnull=False,
                lower__isnull=False,
                pointlayer__isnull=True,
            )
            .only('id', 'point_id')
            .order_by('id')
        )

        for layer in layers:
            layers_by_profile[layer.point_id].append(
                f'medsis:ldlayer/{quote(str(layer.pk), safe="@")}/'
            )

        horizons_by_profile = {
            profile_id: []
            for profile_id in profile_ids
        }

        horizons = (
            PointLayer.objects.using('backoffice')
            .filter(
                point_id__in=profile_ids,
                point__project='SOILS4MED',
            )
            .only('id', 'point_id')
            .order_by('id')
        )

        for horizon in horizons:
            horizons_by_profile[horizon.point_id].append(
                f'medsis:ldhorizon/{quote(str(horizon.pk), safe="@")}/'
            )

        members = []

        for point in page.object_list:
            plot_id = _plot_identifier(point)

            member = {
                '@id': (
                    f'medsis:ldprofile/'
                    f'{quote(str(point.pk), safe="")}/'
                ),
                '@type': 'glosis-pr:GL_Profile',
                'rdfs:label': str(point.pk),
                'plot': f'medsis:ldplot/{plot_id}/',
            }

            profile_layers = layers_by_profile[point.pk]

            profile_horizons = horizons_by_profile[point.pk]

            if profile_horizons:
                member['horizons'] = profile_horizons

            if profile_layers:
                member['layers'] = profile_layers

            members.append(member)

        def page_uri(number):
            return (
                f'medsis:ldprofiles/'
                f'?page={number}&page_size={page_size}'
            )

        view = {
            '@id': page_uri(page.number),
            '@type': 'hydra:PartialCollectionView',
            'hydra:first': {
                '@id': page_uri(1),
            },
            'hydra:last': {
                '@id': page_uri(paginator.num_pages),
            },
        }

        if page.has_previous():
            view['hydra:previous'] = {
                '@id': page_uri(page.previous_page_number()),
            }

        if page.has_next():
            view['hydra:next'] = {
                '@id': page_uri(page.next_page_number()),
            }

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'hydra': 'http://www.w3.org/ns/hydra/core#',
                        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                        'glosis-pr': 'http://w3id.org/glosis/model/profile/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                    }
                ),
                'plot': {
                    '@reverse': 'iso28258:Plot.profile',
                    '@type': '@id',
                },
                'layers': {
                    '@reverse': 'iso28258:ProfileElement.elementOfProfile',
                    '@type': '@id',
                },
                'horizons': {
                    '@reverse': 'iso28258:ProfileElement.elementOfProfile',
                    '@type': '@id',
                },
            },
            '@id': 'medsis:ldprofiles/',
            '@type': 'hydra:Collection',
            'hydra:totalItems': paginator.count,
            'hydra:member': members,
            'hydra:view': view,
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )
    
def _depth_quantity(value):
    """Return a depth in centimetres as a QUDT QuantityValue."""
    if value is None:
        return None

    return {
        '@type': 'qudt:QuantityValue',
        'qudt:numericValue': {
            '@value': value,
            '@type': 'xsd:decimal',
        },
        'qudt:unit': {
            '@id': 'unit:CentiM',
        },
        'qudt:hasQuantityKind': {
            '@id': 'quantitykind:Depth',
        },
    }
class LDHorizonView(View):
    """Return a GloSIS GL_Horizon as JSON-LD."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, horizon_id):
        horizon = get_object_or_404(
            PointLayer.objects.using('backoffice')
            .select_related('point')
            .filter(point__project='SOILS4MED'),
            pk=horizon_id,
        )

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                        'qudt': 'http://qudt.org/schema/qudt/',
                        'unit': 'http://qudt.org/vocab/unit/',
                        'quantitykind': 'http://qudt.org/vocab/quantitykind/',
                        'xsd': 'http://www.w3.org/2001/XMLSchema#',
                        'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                    }
                ),
                'elementOfProfile': {
                    '@id': 'iso28258:ProfileElement.elementOfProfile',
                    '@type': '@id',
                },
            },
            '@id': f'medsis:ldhorizon/{quote(horizon.pk, safe="@")}/',
            '@type': 'glosis-lh:GL_Horizon',
            'elementOfProfile': (
                f'medsis:ldprofile/{quote(horizon.point_id, safe="@")}/'
            ),
        }

        designation = (horizon.horizon or '').strip()

        if designation and designation != '?':
            document['rdfs:label'] = designation
            document['rdfs:comment'] = {
                '@value': (
                    'The label represents the pedological horizon designation recorded in MED-SIS.'
                ),
                '@language': 'en',
            }

        if horizon.number is not None:
            document['iso28258:ProfileElement.order'] = {
                '@value': int(horizon.number),
                '@type': 'xsd:integer',
            }

        if horizon.upper is not None:
            document['iso28258:ProfileElement.upperDepth'] = (
                _depth_quantity(horizon.upper)
            )

        if horizon.lower is not None:
            document['iso28258:ProfileElement.lowerDepth'] = (
                _depth_quantity(horizon.lower)
            )
        # Horizon designation will be added after verifying
        # the corresponding GloSIS property.

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )    
class LDHorizonListView(View):
    """Return a paginated JSON-LD collection of GloSIS Horizons."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request):
        try:
            page_size = int(request.GET.get('page_size', 50))
            page_number = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404('Invalid pagination parameters')

        if not 1 <= page_size <= 200 or page_number < 1:
            raise Http404('Invalid pagination parameters')

        horizons = (
            PointLayer.objects.using('backoffice')
            .filter(point__project='SOILS4MED')
            .only('id', 'point_id', 'horizon', 'number')
            .order_by('id')
        )

        paginator = Paginator(horizons, page_size)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            raise Http404('Page not found')

        members = []

        for horizon in page.object_list:
            horizon_uri = (
                f'medsis:ldhorizon/'
                f'{quote(str(horizon.pk), safe="@")}/'
            )

            profile_uri = (
                f'medsis:ldprofile/'
                f'{quote(str(horizon.point_id), safe="@")}/'
            )

            member = {
                '@id': horizon_uri,
                '@type': 'glosis-lh:GL_Horizon',
                'elementOfProfile': profile_uri,
            }

            designation = (horizon.horizon or '').strip()

            if designation and designation != '?':
                member['rdfs:label'] = designation

            if horizon.number is not None:
                member['iso28258:ProfileElement.order'] = {
                    '@value': int(horizon.number),
                    '@type': 'xsd:integer',
                }

            members.append(member)

        def page_uri(number):
            return (
                f'medsis:ldhorizons/'
                f'?page={number}&page_size={page_size}'
            )

        view = {
            '@id': page_uri(page.number),
            '@type': 'hydra:PartialCollectionView',
            'hydra:first': {
                '@id': page_uri(1),
            },
            'hydra:last': {
                '@id': page_uri(paginator.num_pages),
            },
        }

        if page.has_previous():
            view['hydra:previous'] = {
                '@id': page_uri(page.previous_page_number()),
            }

        if page.has_next():
            view['hydra:next'] = {
                '@id': page_uri(page.next_page_number()),
            }

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'hydra': 'http://www.w3.org/ns/hydra/core#',
                        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
                        'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                        'xsd': 'http://www.w3.org/2001/XMLSchema#',
                    }
                ),
                'elementOfProfile': {
                    '@id': 'iso28258:ProfileElement.elementOfProfile',
                    '@type': '@id',
                },
            },
            '@id': 'medsis:ldhorizons/',
            '@type': 'hydra:Collection',
            'hydra:totalItems': paginator.count,
            'hydra:member': members,
            'hydra:view': view,
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )    
class LDLayerView(View):
    """Return a GloSIS GL_Layer as JSON-LD."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, layer_id):
        layer = get_object_or_404(
            LabData.objects.using('backoffice')
            .filter(
                point__project='SOILS4MED',
                horizon__isnull=True,
                upper__isnull=False,
                lower__isnull=False,
                pointlayer__isnull=True,
            ),
            pk=layer_id,
        )
        
        document = {
            '@context': {
                **_ld_context(
                    **{
                        'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                        'qudt': 'http://qudt.org/schema/qudt/',
                        'unit': 'http://qudt.org/vocab/unit/',
                        'quantitykind': 'http://qudt.org/vocab/quantitykind/',
                        'xsd': 'http://www.w3.org/2001/XMLSchema#',
                    }
                ),
                'elementOfProfile': {
                    '@id': 'iso28258:ProfileElement.elementOfProfile',
                    '@type': '@id',
                },
            },
            '@id': f'medsis:ldlayer/{quote(layer.pk, safe="@")}/',
            '@type': 'glosis-lh:GL_Layer',
            'elementOfProfile': (
                f'medsis:ldprofile/{quote(layer.point_id, safe="@")}/'
            ),
            'iso28258:ProfileElement.upperDepth': (
                _depth_quantity(layer.upper)
            ),
            'iso28258:ProfileElement.lowerDepth': (
                _depth_quantity(layer.lower)
            ),
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

class LDLayerListView(View):
    """Return a paginated JSON-LD collection of GloSIS Layers."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request):
        try:
            page_size = int(request.GET.get('page_size', 50))
            page_number = int(request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise Http404('Invalid pagination parameters')

        if not 1 <= page_size <= 200 or page_number < 1:
            raise Http404('Invalid pagination parameters')

        layers = (
            LabData.objects.using('backoffice')
            .filter(
                point__project='SOILS4MED',
                horizon__isnull=True,
                upper__isnull=False,
                lower__isnull=False,
                pointlayer__isnull=True,
            )
            .only('id', 'point_id')
            .order_by('id')
        )

        paginator = Paginator(layers, page_size)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            raise Http404('Page not found')

        members = []

        for layer in page.object_list:
            member = {
                '@id': (
                    f'medsis:ldlayer/'
                    f'{quote(str(layer.pk), safe="@")}/'
                ),
                '@type': 'glosis-lh:GL_Layer',
                'elementOfProfile': (
                    f'medsis:ldprofile/'
                    f'{quote(str(layer.point_id), safe="@")}/'
                ),
            }

            members.append(member)

        def page_uri(number):
            return (
                f'medsis:ldlayers/'
                f'?page={number}&page_size={page_size}'
            )

        view = {
            '@id': page_uri(page.number),
            '@type': 'hydra:PartialCollectionView',
            'hydra:first': {
                '@id': page_uri(1),
            },
            'hydra:last': {
                '@id': page_uri(paginator.num_pages),
            },
        }

        if page.has_previous():
            view['hydra:previous'] = {
                '@id': page_uri(page.previous_page_number()),
            }

        if page.has_next():
            view['hydra:next'] = {
                '@id': page_uri(page.next_page_number()),
            }

        document = {
            '@context': {
                **_ld_context(
                    **{
                        'hydra': 'http://www.w3.org/ns/hydra/core#',
                        'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                        'iso28258': 'http://w3id.org/glosis/model/iso28258/2013/',
                    }
                ),
                'elementOfProfile': {
                    '@id': 'iso28258:ProfileElement.elementOfProfile',
                    '@type': '@id',
                },
            },
            '@id': 'medsis:ldlayers/',
            '@type': 'hydra:Collection',
            'hydra:totalItems': paginator.count,
            'hydra:member': members,
            'hydra:view': view,
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )
    
LAB_OBSERVATIONS = {
    'ph-h2o': {
        'value_field': 'ph_h2o',
        'method_field': 'met_ph_h2o',
        'observation_class': 'glosis-lh:PH',
        'observed_property':
            'glosis-cl:properties/physioChemicalPropertyCode-pH',
        'procedure_prefix': 'pHProcedure-',
        'generic_procedure': 'pHH2O',
        'method_taxonomy': 'EL_CONDUCTIVITY_PH_METHODS',
        'procedures': {
            'OF': 'pHH2O_ratio1-5',
            'OO': 'pHH2O_ratio1-1',
            'OP': 'pHH2O_ratio1-2.5',
            'OT': 'pHH2O_ratio1-2',
            'SP': 'pHH2O_sat',
        },
        'result_class': 'glosis-lh:PHValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:PH',
    },
    'ph-kcl': {
        'value_field': 'ph_kcl',
        'method_field': 'met_ph_kcl',
        'observation_class': 'glosis-lh:PH',
        'observed_property':
            'glosis-cl:properties/physioChemicalPropertyCode-pH',
        'procedure_prefix': 'pHProcedure-',
        'generic_procedure': 'pHKCl',
        'method_taxonomy': 'EL_CONDUCTIVITY_PH_METHODS',
        'procedures': {
            'OF': 'pHKCl_ratio1-5',
            'OO': 'pHKCl_ratio1-1',
            'OP': 'pHKCl_ratio1-2.5',
            'OT': 'pHKCl_ratio1-2',
            'SP': 'pHKCl_sat',
        },
        'result_class': 'glosis-lh:PHValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:PH',
    },
    'ph-ccl': {
        'value_field': 'ph_ccl',
        'method_field': 'met_ph_ccl',
        'observation_class': 'glosis-lh:PH',
        'observed_property':
            'glosis-cl:properties/physioChemicalPropertyCode-pH',
        'procedure_prefix': 'pHProcedure-',
        'generic_procedure': 'pHCaCl2',
        'method_taxonomy': 'EL_CONDUCTIVITY_PH_METHODS',
        'procedures': {
            'OF': 'pHCaCl2_ratio1-5',
            'OO': 'pHCaCl2_ratio1-1',
            'OP': 'pHCaCl2_ratio1-2.5',
            'OT': 'pHCaCl2_ratio1-2',
            'SP': 'pHCaCl2_sat',
        },
        'result_class': 'glosis-lh:PHValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:PH',
    },
    'el-cond': {
        'value_field': 'el_cond',
        'method_field': 'met_el_cond',
        'observation_class': 'glosis-lh:ElectricalConductivity',
        'observed_property':
            'glosis-cl:properties/physioChemicalPropertyCode-Eleccond',
        'result_class': 'glosis-lh:ElectricalConductivityValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:DeciS-PER-M',
        'procedure_prefix': 'electricalConductivityProcedure-',
        'generic_procedure': None,
        'method_taxonomy': 'EL_CONDUCTIVITY_PH_METHODS',
        'procedures': {
            'OO': 'EC_ratio1-1',
            'OT': 'EC_ratio1-2',
            'OP': 'EC_ratio1-2.5',
            'OF': 'EC_ratio1-5',
            'SP': 'ECe_sat',
        },
    },
    'hy-cond': {
        'value_field': 'hy_cond',
        'method_field': 'met_hy_cond',
        'method_taxonomy': 'HYDRAULIC_CONDUCTIVITY_METHODS',
        'observation_class': 'glosis-lh:HydraulicConductivity',
        'observed_property':
            'glosis-cl:properties/physioChemicalPropertyCode-Hydcond',
        'result_class': 'glosis-lh:HydraulicConductivityValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:CentiM-PER-HR',
        'procedure_prefix': '',
        'generic_procedure': None,
        'procedures': {
            'CP': 'local',
            'DT': 'local',
            'HA': 'local',
            'IN': 'local',
            'PD': 'local',
        },
    },
}

MN_ZN_CU_FIELDS = {
    'mn': ('mn', 'met_mn'),
    'zn': ('zn', 'met_zn'),
    'cu': ('cu', 'met_cu'),
}

SAND_FIELDS = {
    'sand': 'sand',
    'v-c-sand': 'v_c_sand',
    'c-sand': 'c_sand',
    'm-sand': 'm_sand',
    'f-sand': 'f_sand',
    'v-f-sand': 'v_f_sand',
}

SILT_FIELDS = {
    'silt': 'silt',
    'c-silt': 'c_silt',
    'f-silt': 'f_silt',
}

CLAY_FIELDS = {
    'clay': 'clay',
}




for parameter, (value_field, method_field) in MN_ZN_CU_FIELDS.items():
    LAB_OBSERVATIONS[parameter] = {
        'value_field': value_field,
        'method_field': method_field,
        'method_taxonomy': 'MN_ZN_CU_METHODS',
        'observation_class': None,
        'observed_property': MN_ZN_CU_PROPERTIES[parameter],
        'result_class': 'qudt:QuantityValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:MilliGM-PER-KiloGM',
        'procedures': MN_ZN_CU_PROCEDURES,
        'generic_procedure': None,
        'procedure_prefix': '',
    }

for parameter, value_field in SAND_FIELDS.items():
    LAB_OBSERVATIONS[parameter] = {
        'value_field': value_field,
        'method_field': 'met_sand',
        'method_taxonomy': 'SAND_CONTENT_METHODS',
        'observation_class': 'glosis-lh:SandFractionTexture',
        'observed_property': SAND_PROPERTIES[parameter],
        'result_class': 'glosis-lh:SandFractionTextureValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:PERCENT',
        'procedures': SAND_PROCEDURES,
        'generic_procedure': None,
        'procedure_prefix': '',
    }

for parameter, value_field in SILT_FIELDS.items():
    LAB_OBSERVATIONS[parameter] = {
        'value_field': value_field,
        'method_field': 'met_silt',
        'method_taxonomy': 'SILT_CLAY_CONTENT_METHODS',
        'observation_class': 'glosis-lh:SiltFractionTexture',
        'observed_property': SILT_PROPERTIES[parameter],
        'result_class': 'glosis-lh:SiltFractionTextureValue',
        'result_datatype': 'xsd:float',
        'unit': 'unit:PERCENT',
        'procedures': SILT_PROCEDURES,
        'generic_procedure': None,
        'procedure_prefix': '',
    }

LAB_OBSERVATIONS['clay'] = {
    'value_field': 'clay',
    'method_field': 'met_clay',
    'method_taxonomy': 'SILT_CLAY_CONTENT_METHODS',
    'observation_class': 'glosis-lh:ClayFractionTexture',
    'observed_property': 'glosis-cl:properties/textClayPropertyCode-Cl',
    'result_class': 'glosis-lh:ClayFractionTextureValue',
    'result_datatype': 'xsd:float',
    'unit': 'unit:PERCENT',
    'procedures': SILT_PROCEDURES,
    'generic_procedure': None,
    'procedure_prefix': '',
}

LAB_OBSERVATIONS['gravel'] = {
    'value_field': 'gravel',
    'method_field': None,
    'method_taxonomy': None,
    'observation_class': 'sosa:Observation',
    'observed_property': 'medsis:property/gravelContent/',
    'result_class': 'qudt:QuantityValue',
    'result_datatype': 'xsd:float',
    'unit': 'unit:PERCENT',
    'procedures': {},
    'generic_procedure': None,
    'procedure_prefix': '',
}

LAB_OBSERVATIONS['bulk-dens'] = {
    'value_field': 'bulk_dens',
    'method_field': 'met_bulk_dens',
    'method_taxonomy': 'BULK_DENSITY_METHODS',
    'observation_class': 'sosa:Observation',
    'observed_property': 'bulkDensity',
    'result_class': 'qudt:QuantityValue',
    'result_datatype': 'xsd:float',
    'unit': 'unit:GM-PER-CentiM3',
    'procedures': {
        'CM': 'local',
        'EM': 'local',
        'LM': 'local',
    },
    'generic_procedure': None,
    'procedure_prefix': '',
}



class LDLabObservationView(View):
    """JSON-LD observations for MED-SIS laboratory data."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, labdata_id, parameter):
        if parameter == 'texture':
            return self.get_texture(request, labdata_id)
        config = LAB_OBSERVATIONS.get(parameter)
        is_sand = parameter in SAND_FIELDS
        is_local_property = parameter in ('c-sand', 'f-sand', 'gravel', 'bulk-dens',)

        if config is None:
            raise Http404('Unsupported laboratory parameter')

        method_field = config['method_field']
        value_field = config['value_field']
        if method_field:
            lab = get_object_or_404(
                LabData.objects.using('backoffice')
                .select_related(method_field)
                .filter(point__project='SOILS4MED'),
                pk=labdata_id,
            )
        else: 
            lab = get_object_or_404(
                    LabData.objects.using('backoffice')
                    .filter(point__project='SOILS4MED'),
                    pk=labdata_id,
                )

        value = getattr(lab, value_field)

        if value is None:
            raise Http404('Laboratory observation not found')

        if parameter == 'hy-cond':
            value = value / 10

        method = getattr(lab, method_field) if method_field else None

        method_code = None

        if method is not None:
            if (
                method.taxonomy_id == config['method_taxonomy']
                and method.role == TaxonomyValue.ValueRole.CONCEPT
            ):
                method_code = method.value

        
        procedure_name = config['procedures'].get(
            method_code,
            config['generic_procedure'],
        )

        procedure_uri = None

        if procedure_name == 'local':
            procedure = None

            if method is not None:
                mapping = (
                    ProcedureMapping.objects.using('backoffice')
                    .select_related('procedure')
                    .filter(taxonomy_value=method)
                    .first()
                )

                if mapping is not None:
                    procedure = mapping.procedure

                if procedure is None:
                    procedure = (
                        Procedure.objects.using('backoffice')
                        .filter(taxonomy_value=method)
                        .first()
                    )

            if procedure is not None:
                procedure_uri = procedure.uri

        elif procedure_name is not None:
            if procedure_name.startswith('glosis-proc:'):
                procedure_uri = procedure_name
            else:
                procedure_uri = (
                    'glosis-proc:'
                    + config['procedure_prefix']
                    + procedure_name
                )

        lab_id = quote(str(lab.pk), safe='@')
        observed_property = config['observed_property']

        observation_class = config['observation_class']

        if is_sand and (
            is_local_property
            or procedure_uri is None
            or procedure_name == 'local'
        ):
            observation_class = None

        observation_types = ['sosa:Observation']

        if observation_class and observation_class not in observation_types:
            observation_types.append(observation_class)
        
        if is_local_property:
            prop = get_object_or_404(
                Property.objects.using('backoffice'),
                code=observed_property,
            )
            observed_property = prop.uri
            

        document = {
            '@context': _ld_context(
                **{
                    'sosa': 'http://www.w3.org/ns/sosa/',
                    'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                    'glosis-cl': 'http://w3id.org/glosis/model/codelists/',
                    'glosis-proc': 'http://w3id.org/glosis/model/procedure/',
                    'xsd': 'http://www.w3.org/2001/XMLSchema#',
                    'qudt': 'http://qudt.org/schema/qudt/',
                    'unit': 'http://qudt.org/vocab/unit/',
                }
            ),
            '@id': (
                f'medsis:ldobservation/{lab_id}/{parameter}/'
            ),
            '@type': observation_types,
            'sosa:hasFeatureOfInterest': {
                '@id': _lab_feature_of_interest(lab),
            },
            'sosa:observedProperty': {
                '@id': observed_property,
            },
            'sosa:hasResult': {
                '@type': list(dict.fromkeys([
                    config['result_class'],
                    'qudt:QuantityValue',
                ])),
                'qudt:numericValue': {
                    '@value': str(value),
                    '@type': config['result_datatype'],
                },
                'qudt:unit': {
                    '@id': config['unit'],
                },
            },
            
        }
        if procedure_uri is not None:
            document['sosa:usedProcedure'] = {
                '@id': procedure_uri,
            }
        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

    def get_texture(self, request, labdata_id):
        lab = get_object_or_404(
            LabData.objects.using('backoffice')
            .select_related('texture')
            .filter(point__project='SOILS4MED'),
            pk=labdata_id,
        )
        
        texture = lab.texture

        if (
            texture is None
            or texture.taxonomy_id != 'TEXTURE_CLASSES'
            or texture.role != TaxonomyValue.ValueRole.CONCEPT
        ):
            raise Http404('Laboratory texture observation not found')

        lab_id = quote(str(lab.pk), safe='@')

        document = {
            '@context': _ld_context(
                **{
                    'sosa': 'http://www.w3.org/ns/sosa/',
                    'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                    'glosis-cl': 'http://w3id.org/glosis/model/codelists/',
                    'xsd': 'http://www.w3.org/2001/XMLSchema#',
                }
            ),
            '@id': f'medsis:ldobservation/{lab_id}/texture/',
            '@type': [
                'sosa:Observation',
                'glosis-lh:TextureLabClass',
            ],
            'sosa:hasFeatureOfInterest': {
                '@id': _lab_feature_of_interest(lab),
            },
            'sosa:observedProperty': {
                '@id': (
                    'glosis-cl:properties/'
                    'descriptivePropertyCode-textureLabClassProperty'
                ),
            },
            'sosa:hasSimpleResult': {
                '@value': texture.value,
                '@type': 'xsd:string',
            },
            'sosa:hasResult': {
                '@id': (
                    'medsis:ldtaxonomy-value/'
                    'TEXTURE_CLASSES/'
                    f'{quote(texture.value, safe="")}/'
                ),
            },
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

HORIZON_OBSERVATIONS = {
    'texture-class': {
        'field_name': 'tex_cls',
        'taxonomy_id': 'TEXTURE_CLASSES',
        'exclude_nd': False,
        'property_code': None,
    },
    'texture-subclass': {
        'field_name': 'tex_subcls',
        'taxonomy_id': 'TEXTURE_SUBCLASSES',
        'exclude_nd': True,
        'property_code': 'textureFieldSubclass',
    },
}

class LDHorizonObservationView(View):
    """JSON-LD observations for MED-SIS horizon field data."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, horizon_id, parameter):
        if parameter not in ('texture-class', 'texture-subclass'):
            raise Http404('Unsupported horizon parameter')

        is_subclass = parameter == 'texture-subclass'

        field_name = 'tex_subcls' if is_subclass else 'tex_cls'
        taxonomy_id = (
            'TEXTURE_SUBCLASSES' if is_subclass
            else 'TEXTURE_CLASSES'
        )

        horizon = get_object_or_404(
            PointLayer.objects.using('backoffice')
            .select_related('point', field_name)
            .filter(point__project='SOILS4MED'),
            pk=horizon_id,
        )

        texture = getattr(horizon, field_name)

        if (
            texture is None
            or texture.taxonomy_id != taxonomy_id
            or texture.role != TaxonomyValue.ValueRole.CONCEPT
            or (is_subclass and texture.value == 'ND')
        ):
            raise Http404('Horizon observation not found')

        horizon_id_encoded = quote(str(horizon.pk), safe='@')

        if is_subclass:
            prop = get_object_or_404(
                Property.objects.using('backoffice'),
                code='textureFieldSubclass',
            )
            observed_property = prop.uri
            observation_types = ['sosa:Observation']
        else:
            observed_property = (
                'glosis-cl:properties/'
                'descriptivePropertyCode-textureFieldClassProperty'
            )
            observation_types = [
                'sosa:Observation',
                'glosis-lh:TextureFieldClass',
            ]

        document = {
            '@context': _ld_context(
                **{
                    'sosa': 'http://www.w3.org/ns/sosa/',
                    'glosis-lh': 'http://w3id.org/glosis/model/layerhorizon/',
                    'glosis-cl': 'http://w3id.org/glosis/model/codelists/',
                    'xsd': 'http://www.w3.org/2001/XMLSchema#',
                }
            ),
            '@id': (
                f'medsis:ldhorizonobservation/'
                f'{horizon_id_encoded}/{parameter}/'
            ),
            '@type': observation_types,
            'sosa:hasFeatureOfInterest': {
                '@id': f'medsis:ldhorizon/{horizon_id_encoded}/',
            },
            'sosa:observedProperty': {
                '@id': observed_property,
            },
            'sosa:hasSimpleResult': {
                '@value': texture.value,
                '@type': 'xsd:string',
            },
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.views import View
from urllib.parse import quote
import json


class LDObservationListView(View):
    """Paginated Hydra collection of MED-SIS observations."""

    http_method_names = ['get', 'head', 'options']

    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 200

    def get(self, request):
        try:
            page_size = int(
                request.GET.get('page_size', self.DEFAULT_PAGE_SIZE)
            )
        except (TypeError, ValueError):
            raise Http404('Invalid page_size')

        if page_size < 1:
            raise Http404('Invalid page_size')

        page_size = min(page_size, self.MAX_PAGE_SIZE)

        observations = set()

        # --------------------------------------------------
        # 1. Land Use observations
        # --------------------------------------------------

        verified_landuse_mapping = (
            VocabularyMapping.objects.using('backoffice')
            .filter(
                taxonomy_value_id=OuterRef('landuse__use_id'),
                relation=VocabularyMapping.Relation.EXACT,
                status=VocabularyMapping.Status.VERIFIED,
                external_term__vocabulary=GLOSIS_LAND_USE_VOCABULARY,
                external_term__version=GLOSIS_LAND_USE_VERSION,
            )
        )

        landuse_points = (
            PointGeneral.objects.using('backoffice')
            .filter(
                project='SOILS4MED',
                landuse__use__taxonomy_id='USES',
                landuse__use__role=TaxonomyValue.ValueRole.CONCEPT,
            )
            .annotate(
                has_verified_landuse_mapping=Exists(
                    verified_landuse_mapping
                )
            )
            .filter(
                has_verified_landuse_mapping=True
            )
            .values_list('pk', flat=True)
        )
        
        for profile_id in landuse_points.iterator():
            profile_id_encoded = quote(str(profile_id), safe='@')
            observations.add(
                f'medsis:ldobservation/'
                f'{profile_id_encoded}/land-use/'
            )

        # --------------------------------------------------
        # 2. Laboratory observations
        # --------------------------------------------------

        lab_fields = {
            config['value_field']
            for config in LAB_OBSERVATIONS.values()
        }

        lab_fields.update({
            'pk',
            'point_id',
            'horizon',
            'upper',
            'lower',
            'texture_id',
        })

        lab_filter = Q()

        for config in LAB_OBSERVATIONS.values():
            lab_filter |= Q(
                **{f"{config['value_field']}__isnull": False}
            )

        lab_filter |= Q(texture__isnull=False)

        labs = (
            LabData.objects.using('backoffice')
            .filter(
                lab_filter,
                point__project='SOILS4MED',
            )
            .select_related('texture')
            .only(*lab_fields)
            .order_by('pk')
        )

        # Laboratory records connected to PointLayer
        # represent Horizon observations.
        horizon_lab_ids = set(
            PointLayer.objects.using('backoffice')
            .filter(
                point__project='SOILS4MED',
                labdata__isnull=False,
            )
            .values_list('labdata_id', flat=True)
        )

        # Local properties required by some parameters.
        local_property_codes = {
            LAB_OBSERVATIONS[parameter]['observed_property']
            for parameter in ('c-sand', 'f-sand')
            if parameter in LAB_OBSERVATIONS
        }

        existing_properties = set(
            Property.objects.using('backoffice')
            .filter(code__in=local_property_codes)
            .values_list('code', flat=True)
        )

        for lab in labs.iterator():
            is_horizon_lab = lab.pk in horizon_lab_ids

            is_layer_lab = (
                not is_horizon_lab
                and lab.horizon is None
                and lab.upper is not None
                and lab.lower is not None
            )

            if not (is_horizon_lab or is_layer_lab):
                continue

            lab_id = quote(str(lab.pk), safe='@')

            for parameter, config in LAB_OBSERVATIONS.items():
                value = getattr(lab, config['value_field'])

                if value is None:
                    continue

                if parameter in ('c-sand', 'f-sand'):
                    if config['observed_property'] not in existing_properties:
                        continue

                observations.add(
                    f'medsis:ldobservation/'
                    f'{lab_id}/{parameter}/'
                )

            texture = lab.texture

            if (
                texture is not None
                and texture.taxonomy_id == 'TEXTURE_CLASSES'
                and texture.role == TaxonomyValue.ValueRole.CONCEPT
            ):
                observations.add(
                    f'medsis:ldobservation/{lab_id}/texture/'
                )

        # --------------------------------------------------
        # 3. Horizon field observations
        # --------------------------------------------------

        horizon_fields = {
            config['field_name']
            for config in HORIZON_OBSERVATIONS.values()
        }

        horizons = (
            PointLayer.objects.using('backoffice')
            .filter(point__project='SOILS4MED')
            .select_related(*horizon_fields)
            .order_by('pk')
        )

        required_property_codes = {
            config['property_code']
            for config in HORIZON_OBSERVATIONS.values()
            if config['property_code']
        }

        horizon_properties = set(
            Property.objects.using('backoffice')
            .filter(code__in=required_property_codes)
            .values_list('code', flat=True)
        )

        for horizon in horizons.iterator():
            horizon_id = quote(str(horizon.pk), safe='@')

            for parameter, config in HORIZON_OBSERVATIONS.items():
                texture = getattr(horizon, config['field_name'])

                if texture is None:
                    continue

                if (
                    texture.taxonomy_id != config['taxonomy_id']
                    or texture.role != TaxonomyValue.ValueRole.CONCEPT
                ):
                    continue

                if config['exclude_nd'] and texture.value == 'ND':
                    continue

                property_code = config['property_code']

                if (
                    property_code is not None
                    and property_code not in horizon_properties
                ):
                    continue

                observations.add(
                    f'medsis:ldhorizonobservation/'
                    f'{horizon_id}/{parameter}/'
                )

        # --------------------------------------------------
        # 4. Pagination
        # --------------------------------------------------

        ordered_observations = sorted(observations)

        paginator = Paginator(
            ordered_observations,
            page_size,
        )

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        def page_uri(number):
            return (
                f'medsis:ldobservations/'
                f'?page={number}&page_size={page_size}'
            )

        view = {
            '@id': page_uri(page.number),
            '@type': 'hydra:PartialCollectionView',
            'hydra:first': {
                '@id': page_uri(1),
            },
            'hydra:last': {
                '@id': page_uri(paginator.num_pages),
            },
        }

        if page.has_previous():
            view['hydra:previous'] = {
                '@id': page_uri(page.previous_page_number()),
            }

        if page.has_next():
            view['hydra:next'] = {
                '@id': page_uri(page.next_page_number()),
            }

        document = {
            '@context': _ld_context(
                **{
                    'hydra': 'http://www.w3.org/ns/hydra/core#',
                    'xsd': 'http://www.w3.org/2001/XMLSchema#',
                }
            ),
            '@id': 'medsis:ldobservations/',
            '@type': 'hydra:Collection',
            'hydra:totalItems': paginator.count,
            'hydra:member': [
                {'@id': uri}
                for uri in page.object_list
            ],
            'hydra:view': view,
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )
        
class LDPropertyView(View):
    """Return a MED-SIS observed property as JSON-LD."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, code):
        prop = get_object_or_404(
            Property.objects.using('backoffice'),
            code=code,
        )

        document = {
            '@context': _ld_context(
                **{
                    'skos': 'http://www.w3.org/2004/02/skos/core#',
                    'glosis-prop': (
                        'http://w3id.org/glosis/model/'
                        'codelists/properties/'
                    ),
                    'sosa': 'http://www.w3.org/ns/sosa/',
                }
            ),
            '@id': prop.uri,
            '@type': ['skos:Concept', 'sosa:ObservableProperty'],
            'skos:prefLabel': {
                '@value': prop.label,
                '@language': 'en',
            },
            'skos:definition': {
                '@value': prop.description,
                '@language': 'en',
            },
        }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )

class LDProcedureView(View):
    """Return a local MED-SIS procedure as JSON-LD."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, taxonomy_id, code):
        procedure_uri = (
            f"{settings.BACKOFFICE_API_BASE_URL}"
            f"procedures/{taxonomy_id}/{code}"
        )

        procedure = get_object_or_404(
            Procedure.objects.using('backoffice')
            .select_related('taxonomy_value'),
            uri=procedure_uri,
        )

        document = {
            '@context': _ld_context(
                **{
                    'skos': 'http://www.w3.org/2004/02/skos/core#',
                    'sosa': 'http://www.w3.org/ns/sosa/',
                }
            ),
            '@id': procedure.uri,
            '@type': ['skos:Concept', 'sosa:Procedure'],
            'skos:prefLabel': {
                '@value': procedure.label,
                '@language': 'en',
            },
        }

        if procedure.description:
            document['skos:definition'] = {
                '@value': procedure.description,
                '@language': 'en',
            }

        return HttpResponse(
            json.dumps(
                document,
                ensure_ascii=False,
                indent=2,
            ),
            content_type='application/ld+json; charset=utf-8',
        )



