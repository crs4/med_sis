
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from backoffice.models import Procedure, ProcedureStep


DB = "backoffice"

TAXONOMY = "P_AVAILABLE_METHODS"

# Componenti da creare o riutilizzare.
COMPONENTS = {
    "bray": {
        "kind": "extraction",
        "label": "Bray extraction",
        "description": (
            "Bray extraction for available phosphorus. "
            "Bray variant not specified."
        ),
    },
    "mehlich-iii": {
        "kind": "extraction",
        "label": "Mehlich III extraction",
        "description": "",
    },
    "olsen": {
        "kind": "extraction",
        "label": "Olsen extraction",
        "description": (
            "Olsen extraction for available phosphorus."
        ),
    },
}

METHOD_STEPS = {
    "BR": ["bray"],
    "MN": ["mehlich-iii"],
    "OL": ["olsen"],
}


def get_api_base():
    base = getattr(
        settings,
        "BACKOFFICE_API_BASE_URL",
        None,
    )

    if not base:
        site_url = getattr(settings, "SITE_URL", None)

        if not site_url:
            raise CommandError(
                "BACKOFFICE_API_BASE_URL or SITE_URL is required"
            )

        base = site_url.rstrip("/") + "/api/backoffice/"

    return base.rstrip("/") + "/"


class Command(BaseCommand):
    help = "Import reusable procedure steps for Available P"

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

        specs = {}

        for code, component in COMPONENTS.items():
            kind = component["kind"]

            specs[code] = {
                **component,
                "uri": (
                    f"{base}procedures/steps/"
                    f"{kind}/{code}"
                ),
            }

        component_create = 0
        component_existing = 0
        link_create = 0
        link_existing = 0

        with transaction.atomic(using=DB):
            parents = {}

            for method in METHOD_STEPS:
                taxonomy_value_id = f"{TAXONOMY}:{method}"

                try:
                    parents[method] = (
                        Procedure.objects.using(DB).get(
                            taxonomy_value_id=taxonomy_value_id
                        )
                    )
                except Procedure.DoesNotExist:
                    raise CommandError(
                        f"Missing procedure: {taxonomy_value_id}"
                    )

            components = {}

            for code, spec in specs.items():
                component = (
                    Procedure.objects.using(DB)
                    .filter(uri=spec["uri"])
                    .first()
                )

                if component is not None:
                    if component.taxonomy_value_id is not None:
                        raise CommandError(
                            f"URI conflict: {spec['uri']}"
                        )

                    if component.label != spec["label"]:
                        raise CommandError(
                            f"Label conflict: {spec['uri']}"
                        )

                    component_existing += 1

                else:
                    component_create += 1

                    if apply_changes:
                        component = (
                            Procedure.objects.using(DB).create(
                                taxonomy_value=None,
                                uri=spec["uri"],
                                label=spec["label"],
                                description=spec["description"],
                            )
                        )

                components[code] = component

            for method, codes in METHOD_STEPS.items():
                parent = parents[method]

                for position, code in enumerate(codes, start=1):
                    spec = specs[code]

                    existing = (
                        ProcedureStep.objects.using(DB)
                        .select_related("step")
                        .filter(
                            procedure=parent,
                            position=position,
                        )
                        .first()
                    )

                    if existing is not None:
                        if existing.step.uri != spec["uri"]:
                            raise CommandError(
                                "Step conflict: "
                                f"{TAXONOMY}:{method}, "
                                f"position {position}"
                            )

                        link_existing += 1

                    else:
                        link_create += 1

                        if apply_changes:
                            ProcedureStep.objects.using(DB).create(
                                procedure=parent,
                                step=components[code],
                                position=position,
                            )

            self.stdout.write(
                f"Components to create: {component_create}"
            )
            self.stdout.write(
                f"Components existing: {component_existing}"
            )
            self.stdout.write(
                f"Links to create: {link_create}"
            )
            self.stdout.write(
                f"Links existing: {link_existing}"
            )

            if not apply_changes:
                transaction.set_rollback(True, using=DB)
                self.stdout.write("Dry run completed")
            else:
                self.stdout.write("Import completed")

