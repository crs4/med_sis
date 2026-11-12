
from urllib.parse import quote

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ...models import TaxonomyValue, Procedure

METHOD_TAXONOMIES = [
    "ACTIVE_CACO3_CONTENT_METHODS",
    "BULK_DENSITY_METHODS",
    "CACO3_CONTENT_METHODS",
    "CEC_CA_MG_NA_K_METHODS",
    "EL_CONDUCTIVITY_PH_METHODS",
    "EXCHANGEABLE_CATIONS_METHODS",
    "FE_TOT_METHODS",
    "GYPSUM_CONTENT_METHODS",
    "HYDRAULIC_CONDUCTIVITY_METHODS",
    "MN_ZN_CU_METHODS",
    "NH4_METHODS",
    "NO3_METHODS",
    "N_CONTENT_METHODS",
    "ORGANIC_CARBON_METHODS",
    "ORGANIC_MATTER_CONTENT_METHODS",
    "PB_HG_CD_NI_CR_AS_CO_V_METHODS",
    "P_AVAILABLE_METHODS",
    "ROC_TOC400_METHODS",
    "SAND_CONTENT_METHODS",
    "SILT_CLAY_CONTENT_METHODS",
    "SOLUBLE_CATIONS_METHODS",
    "WILTING_POINT_METHODS",
]

def get_base_uri():
    configured = getattr(settings, "BACKOFFICE_API_BASE_URL", None)

    if configured:
        return configured.rstrip("/") + "/"

    site_url = getattr(settings, "SITE_URL", None)
    if not site_url:
        raise CommandError(
            "Configure SITE_URL or BACKOFFICE_API_BASE_URL"
        )

    return site_url.rstrip("/") + "/api/backoffice/"


def build_procedure_uri(base_uri, taxonomy_id, code):
    return (
        f"{base_uri}procedures/"
        f"{quote(taxonomy_id, safe='')}/"
        f"{quote(code, safe='')}"
    )


class Command(BaseCommand):
    help = "Import MED-SIS local procedures from TaxonomyValue"

    def add_arguments(self, parser):
        parser.add_argument(
            "--taxonomy",
            action="append",
            help="Method taxonomy ID; repeat for multiple taxonomies",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write changes to the backoffice database",
        )

    def handle(self, *args, **options):
        base_uri = get_base_uri()
        taxonomy_ids = sorted(set(options["taxonomy"] or METHOD_TAXONOMIES))
        apply = options["apply"]
        values = (
            TaxonomyValue.objects.using("backoffice")
            .filter(
                taxonomy_id__in=taxonomy_ids,
                role=TaxonomyValue.ValueRole.CONCEPT,
            )
            .order_by("taxonomy_id", "value")
        )

        counts = {
            "create": 0,
            "existing": 0,
            "conflict": 0,
        }

        with transaction.atomic(using="backoffice"):
            for value in values.iterator():
                uri = build_procedure_uri(
                    base_uri,
                    value.taxonomy_id,
                    value.value,
                )

                existing = (
                    Procedure.objects.using("backoffice")
                    .filter(taxonomy_value_id=value.pk)
                    .first()
                )

                if existing:
                    if existing.uri != uri:
                        self.stdout.write(
                            f"EXISTING URI DIFFERS: {value.pk} "
                            f"{existing.uri}"
                        )
                    counts["existing"] += 1
                    continue

                if (
                    Procedure.objects.using("backoffice")
                    .filter(uri=uri)
                    .exists()
                ):
                    self.stderr.write(
                        f"URI CONFLICT: {value.pk} -> {uri}"
                    )
                    counts["conflict"] += 1
                    continue

                label = value.descr or value.value

                self.stdout.write(
                    f"CREATE: {value.pk} -> {uri}"
                )
                counts["create"] += 1

                if apply:
                    Procedure.objects.using("backoffice").create(
                        taxonomy_value=value,
                        uri=uri,
                        label=label,
                        description=value.descr or "",
                    )

        self.stdout.write(
            f"\nMode: {'APPLY' if apply else 'DRY RUN'}"
        )
        self.stdout.write(str(counts))

        if counts["conflict"]:
            raise CommandError(
                "URI conflicts detected; review before proceeding"
            )

