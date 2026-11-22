from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from backoffice.models import (
    ObservationDefinition,
    ObservationProcedureMapping,
    TaxonomyValue,
)
from backoffice.api.ldviews import LAB_OBSERVATIONS


def procedure_mapping_data(config, procedure_name):
    if procedure_name == 'local':
        return {
            'procedure_source': 'local',
            'procedure_uri': '',
        }

    if procedure_name.startswith('glosis-proc:'):
        uri = procedure_name
    else:
        uri = (
            'glosis-proc:'
            + config['procedure_prefix']
            + procedure_name
        )

    return {
        'procedure_source': 'uri',
        'procedure_uri': uri,
    }


class Command(BaseCommand):
    help = 'Import laboratory observation procedure mappings.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
        )

    def handle(self, *args, **options):
        db = 'backoffice'
        dry_run = options['dry_run']

        new_count = 0
        existing_count = 0
        errors = []

        definitions = {
            d.code: d
            for d in ObservationDefinition.objects.using(db)
            .filter(source_type='legacy', source_model='labdata')
        }

        planned = []

        for code, config in LAB_OBSERVATIONS.items():
            definition = definitions.get(code)

            if definition is None:
                errors.append(f'{code}: definition not found')
                continue

            taxonomy_id = definition.method_taxonomy_id

            for method_code, procedure_name in config['procedures'].items():
                method = (
                    TaxonomyValue.objects.using(db)
                    .filter(
                        taxonomy_id=taxonomy_id,
                        value=method_code,
                        role=TaxonomyValue.ValueRole.CONCEPT,
                    )
                    .first()
                )

                if method is None:
                    errors.append(
                        f'{code}/{method_code}: method not found'
                    )
                    continue

                data = procedure_mapping_data(
                    config, procedure_name
                )

                planned.append((definition, method, data))

            generic = config.get('generic_procedure')

            if generic is not None:
                data = procedure_mapping_data(config, generic)
                planned.append((definition, None, data))

        if errors:
            for error in errors:
                self.stderr.write(error)

            raise CommandError(
                f'Import aborted: {len(errors)} errors'
            )

        for definition, method, data in planned:
            exists = (
                ObservationProcedureMapping.objects.using(db)
                .filter(
                    observation=definition,
                    method=method,
                )
                .exists()
            )

            if exists:
                existing_count += 1
                status = 'EXISTS'
            else:
                new_count += 1
                status = 'NEW'

            self.stdout.write(
                f'{status:6} {definition.code} / '
                f'{method.value if method else "default"} '
                f'-> {data["procedure_source"]}: '
                f'{data["procedure_uri"]}'
            )

        self.stdout.write(
            f'\nMappings: {len(planned)}'
            f'\nNew: {new_count}'
            f'\nExisting: {existing_count}'
            f'\nErrors: 0'
        )

        if dry_run:
            self.stdout.write(
                'DRY RUN completed. No records were written.'
            )
            return

        with transaction.atomic(using=db):
            for definition, method, data in planned:
                mapping, created = (
                    ObservationProcedureMapping.objects.using(db)
                    .get_or_create(
                        observation=definition,
                        method=method,
                        defaults=data,
                    )
                )

                if created:
                    mapping.full_clean()

        self.stdout.write(
            self.style.SUCCESS('Import completed.')
        )