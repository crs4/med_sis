
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from backoffice.models import Procedure, ProcedureStep, TaxonomyValue


DB = "backoffice"

# Componenti analitici riutilizzabili.
# Le descrizioni non introducono concentrazioni o tecniche
# strumentali non documentate.
COMPONENTS = {
    "nh4oac-ph7": (
        "extraction",
        "Ammonium acetate extraction at pH 7",
    ),
    "mehlich-iii": (
        "extraction",
        "Mehlich III extraction",
    ),
    "bacl2": (
        "extraction",
        "Barium chloride extraction/saturation",
    ),
    "bacl2-equilibration": (
        "equilibration",
        "Barium chloride equilibration",
    ),
    "mgso4-exchange": (
        "exchange",
        "Compulsive exchange with magnesium sulfate",
    ),
    "cec-difference": (
        "calculation",
        "CEC determination by difference",
    ),
}

# Sequenza delle fasi per le sei procedure.
# BM (CEC) segue la sequenza ISO 11260 proposta.
METHOD_STEPS = {
    "CEC_CA_MG_NA_K_METHODS:AA": [
        "nh4oac-ph7",
    ],
    "CEC_CA_MG_NA_K_METHODS:BM": [
        "bacl2",
        "bacl2-equilibration",
        "mgso4-exchange",
        "cec-difference",
    ],
    "CEC_CA_MG_NA_K_METHODS:ME": [
        "mehlich-iii",
    ],
    "EXCHANGEABLE_CATIONS_METHODS:AA": [
        "nh4oac-ph7",
    ],
    "EXCHANGEABLE_CATIONS_METHODS:BM": [
        "bacl2",
    ],
    "EXCHANGEABLE_CATIONS_METHODS:ME": [
        "mehlich-iii",
    ],
}


def get_api_base():
    base = getattr(settings, "BACKOFFICE_API_BASE_URL", None)

    if not base:
        site_url = getattr(settings, "SITE_URL", None)
        if not site_url:
            raise CommandError(
                "BACKOFFICE_API_BASE_URL or SITE_URL is required"
            )
        base = site_url.rstrip("/") + "/api/backoffice/"

    return base.rstrip("/") + "/"


class Command(BaseCommand):
    help = "Import reusable CEC and exchangeable-cation procedure steps"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write changes to the backoffice database",
        )

    def handle(self, *args, **options):
        apply_changes = options["apply"]
        base = get_api_base()

        self.stdout.write(
            f"Mode: {'APPLY' if apply_changes else 'DRY RUN'}"
        )

        component_specs = {}

        for code, (kind, label) in COMPONENTS.items():
            uri = f"{base}procedures/steps/{kind}/{code}"
            component_specs[code] = {
                "uri": uri,
                "label": label,
            }

        # Validate all parent procedures before writing.
        parents = {}

        for taxonomy_value_id in METHOD_STEPS:
            try:
                parent = (
                    Procedure.objects.using(DB)
                    .select_related("taxonomy_value")
                    .get(taxonomy_value_id=taxonomy_value_id)
                )
            except Procedure.DoesNotExist:
                raise CommandError(
                    f"Missing parent procedure: {taxonomy_value_id}"
                )

            parents[taxonomy_value_id] = parent

        created_components = 0
        existing_components = 0
        created_links = 0
        existing_links = 0

        with transaction.atomic(using=DB):
            components = {}

            for code, spec in component_specs.items():
                uri = spec["uri"]

                component = (
                    Procedure.objects.using(DB)
                    .filter(uri=uri)
                    .first()
                )

                if component is not None:
                    if (
                        component.taxonomy_value_id is not None
                        or component.label != spec["label"]
                    ):
                        raise CommandError(
                            f"Component URI conflict: {uri}"
                        )

                    existing_components += 1

                else:
                    created_components += 1

                    if apply_changes:
                        component = Procedure.objects.using(DB).create(
                            taxonomy_value=None,
                            uri=uri,
                            label=spec["label"],
                            description="",
                        )

                components[code] = component

            for taxonomy_value_id, codes in METHOD_STEPS.items():
                parent = parents[taxonomy_value_id]

                for position, code in enumerate(codes, start=1):
                    component = components[code]
                    spec = component_specs[code]

                    existing_link = (
                        ProcedureStep.objects.using(DB)
                        .select_related("step")
                        .filter(
                            procedure=parent,
                            position=position,
                        )
                        .first()
                    )

                    if existing_link is not None:
                        if existing_link.step.uri != spec["uri"]:
                            raise CommandError(
                                "Step conflict: "
                                f"{taxonomy_value_id}, "
                                f"position {position}"
                            )

                        existing_links += 1

                    else:
                        created_links += 1

                        if apply_changes:
                            ProcedureStep.objects.using(DB).create(
                                procedure=parent,
                                step=component,
                                position=position,
                            )

            self.stdout.write(
                f"Components to create: {created_components}"
            )
            self.stdout.write(
                f"Components existing: {existing_components}"
            )
            self.stdout.write(
                f"Links to create: {created_links}"
            )
            self.stdout.write(
                f"Links existing: {existing_links}"
            )

            if not apply_changes:
                transaction.set_rollback(True, using=DB)
                self.stdout.write("Dry run completed")
            else:
                self.stdout.write("Import completed")

