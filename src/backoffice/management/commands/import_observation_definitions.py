from decimal import Decimal
from importlib import import_module

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.conf import settings

from backoffice.models import (
    ObservationDefinition,
    Property,
    Taxonomy,
)

# Sostituire con il modulo effettivo che definisce LAB_OBSERVATIONS.
OBSERVATIONS_MODULE = "backoffice.api.ldviews"

PREFIXES = {
    "sosa": "http://www.w3.org/ns/sosa/",
    "glosis-lh": "http://w3id.org/glosis/model/layerhorizon/",
    "glosis-cl": "http://w3id.org/glosis/model/codelists/",
    "glosis-proc": "http://w3id.org/glosis/model/procedure/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "qudt": "http://qudt.org/schema/qudt/",
    "unit": "http://qudt.org/vocab/unit/",
}

LOCAL_PROPERTIES = {
    "c-sand",
    "f-sand",
    "gravel",
    "bulk-dens",
}

def normalize_property_uri(value):
    if value.startswith("medsis:"):
        return value

    return expand_uri(value)

def expand_uri(value):
    if not value:
        return ""

    if value.startswith(("http://", "https://")):
        return value

    prefix, separator, suffix = value.partition(":")

    if separator and prefix in PREFIXES:
        return PREFIXES[prefix] + suffix

    raise ValueError(f"Unrecognized URI: {value}")


class Command(BaseCommand):
    help = "Import laboratory observation definitions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate without writing to the database",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        db = "backoffice"

        try:
            module = import_module(OBSERVATIONS_MODULE)
            configurations = dict(module.LAB_OBSERVATIONS)
        except (ImportError, AttributeError) as exc:
            raise CommandError(
                f"Cannot load LAB_OBSERVATIONS: {exc}"
            ) from exc

        # Texture is currently handled separately in the view.
        if "texture" in configurations:
            raise CommandError(
                "texture is already present in LAB_OBSERVATIONS"
            )

        configurations["texture"] = {
            "value_field": "texture",
            "method_field": None,
            "method_taxonomy": None,
            "observation_class": "glosis-lh:TextureLabClass",
            "observed_property": (
                "glosis-cl:properties/"
                "descriptivePropertyCode-textureLabClassProperty"
            ),
            "result_class": None,
            "result_datatype": "xsd:string",
            "unit": None,
            "result_taxonomy": "TEXTURE_CLASSES",
        }

        errors = []
        pending = []
        existing = 0

        for code, config in configurations.items():
            try:
                if ObservationDefinition.objects.using(db).filter(
                    pk=code
                ).exists():
                    existing += 1
                    self.stdout.write(f"EXISTS  {code}")
                    continue

                property_code = config["observed_property"]

                if code == "gravel":
                    observed_property = "medsis:property/gravelContent/"
                
                elif code in LOCAL_PROPERTIES:
                    prop = Property.objects.using(db).get(
                        code=property_code
                    )
                    observed_property = normalize_property_uri(prop.uri)

                else:
                    observed_property = expand_uri(property_code)

                method_taxonomy = None
                taxonomy_code = config.get("method_taxonomy")

                if taxonomy_code:
                    method_taxonomy = Taxonomy.objects.using(db).get(
                        pk=taxonomy_code
                    )

                result_taxonomy = None
                result_taxonomy_code = config.get("result_taxonomy")

                if result_taxonomy_code:
                    result_taxonomy = Taxonomy.objects.using(db).get(
                        pk=result_taxonomy_code
                    )

                is_texture = code == "texture"

                definition = ObservationDefinition(
                    code=code,
                    label=code,
                    description="",
                    feature_type="",
                    source_type="legacy",
                    source_model="labdata",
                    result_type=(
                        "categorical" if is_texture else "numeric"
                    ),
                    observation_class=expand_uri(
                        config.get("observation_class")
                    ),
                    observed_property=observed_property,
                    result_class=expand_uri(
                        config.get("result_class")
                    ),
                    result_datatype=expand_uri(
                        config.get("result_datatype")
                    ),
                    unit=expand_uri(config.get("unit")),
                    source_unit="",
                    conversion_factor=(
                        Decimal("0.1")
                        if code == "hy-cond"
                        else Decimal("1")
                    ),
                    method_taxonomy=method_taxonomy,
                    result_taxonomy=result_taxonomy,
                    value_field=config["value_field"],
                    method_field=config.get("method_field") or "",
                )

                definition.full_clean()
                pending.append(definition)
                self.stdout.write(f"NEW     {code}")

            except (
                Property.DoesNotExist,
                Taxonomy.DoesNotExist,
                ValidationError,
                ValueError,
            ) as exc:
                errors.append(f"{code}: {exc}")
                self.stderr.write(f"ERROR   {code}: {exc}")

        self.stdout.write(
            f"\nDefinitions: {len(configurations)}"
            f"\nNew: {len(pending)}"
            f"\nExisting: {existing}"
            f"\nErrors: {len(errors)}"
        )

        if errors:
            raise CommandError(
                "Validation failed. No records were written."
            )

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    "DRY RUN completed. No records were written."
                )
            )
            return

        with transaction.atomic(using=db):
            for definition in pending:
                definition.save(using=db)

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(pending)} definitions."
            )
        )