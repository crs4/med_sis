from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ...models import Procedure, ProcedureStep


COMPONENTS = {
    "dtpa-ammonium-bicarbonate": (
        "extraction",
        "DTPA ammonium bicarbonate extraction",
    ),
    "dtpa": ("extraction", "DTPA extraction"),
    "edta": ("extraction", "EDTA extraction"),
    "hno3": ("extraction", "Nitric acid extraction"),
    "faas": ("determination", "FAAS determination"),
    "icp-aes": ("determination", "ICP-AES determination"),
    "icp-ms": ("determination", "ICP-MS determination"),
}

METHODS = {
    "DBF": ("dtpa-ammonium-bicarbonate", "faas"),
    "DBIA": ("dtpa-ammonium-bicarbonate", "icp-aes"),
    "DBIM": ("dtpa-ammonium-bicarbonate", "icp-ms"),
    "DF": ("dtpa", "faas"),
    "DIA": ("dtpa", "icp-aes"),
    "DIM": ("dtpa", "icp-ms"),
    "EF": ("edta", "faas"),
    "EIA": ("edta", "icp-aes"),
    "EIM": ("edta", "icp-ms"),
    "NAF": ("hno3", "faas"),
    "NAIA": ("hno3", "icp-aes"),
    "NAIM": ("hno3", "icp-ms"),
}

TAXONOMY_METHODS = {
    "MN_ZN_CU_METHODS": list(METHODS),
    "PB_HG_CD_NI_CR_AS_CO_V_METHODS": [
        "DBF", "DBIA", "DBIM", "NAF", "NAIA", "NAIM",
    ],
}


class Command(BaseCommand):
    help = "Import reusable MED-SIS procedure steps"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply", action="store_true"
        )

    def handle(self, *args, **options):
        apply = options["apply"]
        base = getattr(
            settings, "BACKOFFICE_API_BASE_URL", None
        )
        if not base:
            site = getattr(settings, "SITE_URL", None)
            if not site:
                raise CommandError("Missing SITE_URL")
            base = site.rstrip("/") + "/api/backoffice/"
        base = base.rstrip("/") + "/"

        component_uris = {
            code: (
                f"{base}procedures/steps/{kind}/{code}"
            )
            for code, (kind, _) in COMPONENTS.items()
        }

        with transaction.atomic(using="backoffice"):
            existing_components = {}
            new_components = {}

            for code, uri in component_uris.items():
                obj = (
                    Procedure.objects.using("backoffice")
                    .filter(uri=uri).first()
                )
                if obj:
                    if obj.taxonomy_value_id is not None:
                        raise CommandError(
                            f"Component URI conflict: {uri}"
                        )
                    existing_components[code] = obj
                else:
                    new_components[code] = uri

            assignments = []
            new_links = 0
            existing_links = 0

            for taxonomy, codes in TAXONOMY_METHODS.items():
                for code in codes:
                    tv_id = f"{taxonomy}:{code}"
                    proc = (
                        Procedure.objects.using("backoffice")
                        .filter(taxonomy_value_id=tv_id)
                        .first()
                    )
                    if proc is None:
                        raise CommandError(
                            f"Missing procedure: {tv_id}"
                        )

                    for position, component in enumerate(
                        METHODS[code], start=1
                    ):
                        current = (
                            ProcedureStep.objects.using(
                                "backoffice"
                            )
                            .filter(
                                procedure=proc,
                                position=position,
                            )
                            .select_related("step")
                            .first()
                        )
                        target_uri = component_uris[component]

                        if current:
                            if current.step.uri != target_uri:
                                raise CommandError(
                                    f"Step conflict: {tv_id} "
                                    f"position {position}"
                                )
                            existing_links += 1
                        else:
                            assignments.append(
                                (proc, position, component)
                            )
                            new_links += 1

            self.stdout.write(
                f"Mode: {'APPLY' if apply else 'DRY RUN'}"
            )
            self.stdout.write(
                f"Components to create: {len(new_components)}"
            )
            self.stdout.write(
                f"Components existing: {len(existing_components)}"
            )
            self.stdout.write(
                f"Links to create: {new_links}"
            )
            self.stdout.write(
                f"Links existing: {existing_links}"
            )

            if not apply:
                return

            components = dict(existing_components)

            for code, uri in new_components.items():
                _, label = COMPONENTS[code]
                components[code] = (
                    Procedure.objects.using("backoffice")
                    .create(
                        taxonomy_value=None,
                        uri=uri,
                        label=label,
                        description="",
                    )
                )

            for proc, position, component in assignments:
                ProcedureStep.objects.using("backoffice").create(
                    procedure=proc,
                    step=components[component],
                    position=position,
                )

            self.stdout.write(
                self.style.SUCCESS("Import completed")
            )

