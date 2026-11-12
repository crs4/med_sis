"""Import the GloSIS landUseClass collection from expanded JSON-LD.

Example:
  python manage.py import_glosis_results /path/to/glosis_results.jsonld --vocabulary-version 1.9.9 --dry-run
  python manage.py import_glosis_results /path/to/glosis_results.jsonld --vocabulary-version 1.9.9

The supplied source may use the /codelists/results/ namespace; the published
concept IRIs use /codelists/. The conversion is restricted to landUseClass.
"""
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from backoffice.models import VocabularyTerm

SKOS = 'http://www.w3.org/2004/02/skos/core#'
DCT = 'http://purl.org/dc/terms/'
OWL = 'http://www.w3.org/2002/07/owl#'
OLD_BASE = 'http://w3id.org/glosis/model/codelists/results/'
PUBLIC_BASE = 'http://w3id.org/glosis/model/codelists/'
COLLECTION_SUFFIX = 'LandUseClassValueCollection'
CONCEPT_PREFIX = 'landUseClassValueCode-'
VOCABULARY = 'glosis-results-landUseClass'


def nodes_from(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get('@graph'), list):
        return data['@graph']
    raise CommandError('JSON-LD non espanso: atteso array o oggetto con @graph. Convertire in expanded JSON-LD.')


def entries(node, key):
    value = node.get(key, [])
    return value if isinstance(value, list) else [value]


def links(node, key):
    return {item['@id'] for item in entries(node, key) if isinstance(item, dict) and isinstance(item.get('@id'), str)}


def lit(node, key):
    candidates = [v for v in entries(node, key) if isinstance(v, dict) and isinstance(v.get('@value'), str)]
    preferred = next((v for v in candidates if v.get('@language') == 'en'), None)
    return (preferred or (candidates[0] if candidates else {})).get('@value', '').strip()


def suffix_of(uri):
    for base in (OLD_BASE, PUBLIC_BASE):
        if uri.startswith(base):
            return uri[len(base):]
    return None


class Command(BaseCommand):
    help = 'Importa i 50 concetti GloSIS landUseClass in vocabulary_term.'

    def add_arguments(self, parser):
        parser.add_argument('jsonld_path', type=Path)
        parser.add_argument('--vocabulary-version', required=True, help='Versione della sorgente, ad es. 1.9.9')
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--database', default='backoffice')

    def handle(self, *args, **opts):
        path = opts['jsonld_path']
        if not path.is_file():
            raise CommandError(f'File non trovato: {path}')
        try:
            nodes = nodes_from(json.loads(path.read_text(encoding='utf-8-sig')))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise CommandError(f'Impossibile leggere JSON-LD: {exc}') from exc

        by_id = {n['@id']: n for n in nodes if isinstance(n, dict) and isinstance(n.get('@id'), str)}
        collection = [n for uri, n in by_id.items() if suffix_of(uri) == COLLECTION_SUFFIX]
        if len(collection) != 1:
            raise CommandError('Collection LandUseClassValueCollection assente o ambigua.')
        members = links(collection[0], SKOS + 'member')
        if len(members) != 50:
            raise CommandError(f'Attesi 50 membri della collection, trovati {len(members)}.')

        # Reject inconsistent source versions, when an ontology versionInfo is provided.
        declared = {lit(n, OWL + 'versionInfo') for n in nodes if isinstance(n, dict) and OWL + 'Ontology' in n.get('@type', [])}
        declared.discard('')
        if declared and opts['vocabulary_version'] not in declared:
            raise CommandError(f'Versione richiesta {opts["vocabulary_version"]} non coincide con il JSON-LD: {sorted(declared)}')

        records = {}
        notations = set()
        for member in members:
            node = by_id.get(member)
            if not node:
                raise CommandError(f'Membro non definito nel JSON-LD: {member}')
            suffix = suffix_of(member)
            if not suffix or not suffix.startswith(CONCEPT_PREFIX):
                raise CommandError(f'IRI membro inatteso: {member}')
            if SKOS + 'Concept' not in node.get('@type', []) and SKOS + 'Concept' not in links(node, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'):
                raise CommandError(f'Membro non dichiarato skos:Concept: {member}')
            notation = lit(node, SKOS + 'notation')
            label = lit(node, SKOS + 'prefLabel')
            if not notation or not label or notation in notations:
                raise CommandError(f'Notation/label assente o notation duplicata: {member}')
            notations.add(notation)
            uri = PUBLIC_BASE + suffix
            if uri in records:
                raise CommandError(f'IRI duplicato: {uri}')
            records[uri] = {
                'vocabulary': VOCABULARY,
                'label': label,
                'description': lit(node, SKOS + 'definition'),
                'source_type': 'skos:Concept',
            }

        database, version, dry_run = opts['database'], opts['vocabulary_version'], opts['dry_run']
        created = updated = unchanged = 0
        try:
            with transaction.atomic(using=database):
                existing = {x.uri: x for x in VocabularyTerm.objects.using(database).select_for_update().filter(uri__in=records, version=version)}
                for uri, defaults in sorted(records.items()):
                    current = existing.get(uri)
                    if current is None:
                        created += 1
                        if not dry_run:
                            VocabularyTerm.objects.using(database).create(uri=uri, version=version, **defaults)
                    elif any(getattr(current, key) != value for key, value in defaults.items()):
                        updated += 1
                        if not dry_run:
                            for key, value in defaults.items():
                                setattr(current, key, value)
                            current.save(using=database, update_fields=list(defaults))
                    else:
                        unchanged += 1
                if dry_run:
                    transaction.set_rollback(True, using=database)
        except Exception as exc:
            raise CommandError(f'Errore database ({database}): {exc}') from exc

        self.stdout.write(self.style.SUCCESS(
            f'{"[DRY RUN] " if dry_run else ""}GloSIS landUseClass {version}: '
            f'{len(records)} concetti; da creare={created}, da aggiornare={updated}, invariati={unchanged}.'
        ))
        if dry_run:
            self.stdout.write('Nessuna modifica al database.')
