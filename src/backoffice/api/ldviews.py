
"""Read-only JSON-LD endpoints for MED-SIS soil observations."""

import json
import re
from urllib.parse import quote
from decimal import Decimal, ROUND_DOWN

from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from backoffice.models import PointGeneral, VocabularyMapping, TaxonomyValue, PointLayer, LabData

GLOSIS_LAND_USE_VOCABULARY = 'glosis-results-landUseClass'
GLOSIS_LAND_USE_VERSION = '1.9.9'


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

PH_H2O_PROCEDURES = {
    'OF': 'pHH2O_ratio1-5',
    'OO': 'pHH2O_ratio1-1',
    'OP': 'pHH2O_ratio1-2.5',
    'OT': 'pHH2O_ratio1-2',
    'SP': 'pHH2O_sat',
}

PH_H2O_GENERIC_PROCEDURE = 'pHH2O'


class LDPHObservationView(View):
    """JSON-LD observation for LabData.ph_h2o."""

    http_method_names = ['get', 'head', 'options']

    def get(self, request, labdata_id):
        lab = get_object_or_404(
            LabData.objects.using('backoffice')
            .select_related('met_ph_h20')
            .filter(point__project='SOILS4MED'),
            pk=labdata_id,
            horizon__isnull=True,
            upper__isnull=False,
            lower__isnull=False,
        )

        if lab.ph_h2o is None:
            raise Http404('pH H2O observation not found')

        # Il metodo appartiene alla tassonomia condivisa
        # EL_CONDUCTIVITY_PH_METHODS.
        method_code = None

        if lab.met_ph_h20_id:
            method = lab.met_ph_h20

            if (
                method.taxonomy_id == 'EL_CONDUCTIVITY_PH_METHODS'
                and method.role == TaxonomyValue.ValueRole.CONCEPT
            ):
                method_code = method.value

        procedure_name = PH_H2O_PROCEDURES.get(
            method_code,
            PH_H2O_GENERIC_PROCEDURE,
        )

        procedure_uri = (
            'glosis-proc:pHProcedure-' + procedure_name
        )

        # Le URI MED-SIS sono riferite al nodo corrente.
        lab_id = quote(str(lab.pk), safe='@')

        document = {
            '@context': _ld_context(
                **{
                    'sosa': 'http://www.w3.org/ns/sosa/',
                    'glosis-lh':
                        'http://w3id.org/glosis/model/layerhorizon/',
                    'glosis-cl':
                        'http://w3id.org/glosis/model/codelists/',
                    'glosis-proc':
                        'http://w3id.org/glosis/model/procedure/',
                    'xsd':
                        'http://www.w3.org/2001/XMLSchema#',
                }
            ),
            '@id': f'medsis:ldobservation/{lab_id}/ph-h2o/',
            '@type': [
                'sosa:Observation',
                'glosis-lh:PH',
            ],
            'sosa:hasFeatureOfInterest': {
                '@id': f'medsis:ldlayer/{lab_id}/',
            },
            'sosa:observedProperty': {
                '@id':
                    'glosis-cl:physioChemicalPropertyCode-pH',
            },
            'sosa:usedProcedure': {
                '@id': procedure_uri,
            },
            'sosa:hasSimpleResult': {
                '@value': str(Decimal(str(lab.ph_h2o))),
                '@type': 'xsd:decimal',
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
