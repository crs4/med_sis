"""Import GloSIS Procedures 2.0.0 JSON-LD into VocabularyTerm.

Usage:
    python manage.py import_glosis_procedures /path/to/doc_glosis_procedures.jsonld --dry-run
    python manage.py import_glosis_procedures /path/to/doc_glosis_procedures.jsonld
"""
import json
from pathlib import Path
from urllib.parse import urlparse

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from backoffice.models import VocabularyTerm

OWL_NAMED_INDIVIDUAL = 'http://www.w3.org/2002/07/owl#NamedIndividual'
OWL_ONTOLOGY = 'http://www.w3.org/2002/07/owl#Ontology'
OWL_VERSION_IRI = 'http://www.w3.org/2002/07/owl#versionIRI'
OWL_VERSION_INFO = 'http://www.w3.org/2002/07/owl#versionInfo'
RDF_TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
SKOS_CONCEPT = 'http://www.w3.org/2004/02/skos/core#Concept'
SKOS_PREF_LABEL = 'http://www.w3.org/2004/02/skos/core#prefLabel'
SKOS_DEFINITION = 'http://www.w3.org/2004/02/skos/core#definition'
SKOS_NOTATION = 'http://www.w3.org/2004/02/skos/core#notation'
BASE_URI = 'http://w3id.org/glosis/model/procedure/'
ONTOLOGY_URI = BASE_URI.rstrip('/')
VERSION = '2.0.0'
VOCABULARY = 'glosis-proc'


def objects_from(document):
    if isinstance(document, list):
        return document
    if isinstance(document, dict) and isinstance(document.get('@graph'), list):
        return document['@graph']
    raise CommandError('Formato JSON-LD non supportato: atteso array o oggetto con @graph.')


def values(node, predicate):
    result = node.get(predicate, [])
    if isinstance(result, dict):
        return [result]
    return result if isinstance(result, list) else []


def literal(node, predicate):
    entries = [x for x in values(node, predicate) if isinstance(x, dict) and isinstance(x.get('@value'), str)]
    for entry in entries:
        if entry.get('@language') == 'en':
            return entry['@value'].strip()
    return entries[0]['@value'].strip() if entries else ''


def ids(node, predicate):
    return {x['@id'] for x in values(node, predicate) if isinstance(x, dict) and isinstance(x.get('@id'), str)}


class Command(BaseCommand):
    help = 'Importa solo i concetti di procedura GloSIS 2.0.0 in vocabulary_term (database backoffice).'

    def add_arguments(self, parser):
        parser.add_argument('jsonld_path', type=Path, help='File JSON-LD GloSIS Procedures 2.0.0')
        parser.add_argument('--dry-run', action='store_true', help='Verifica e conta le operazioni senza scrivere nel DB')
        parser.add_argument('--database', default='backoffice', help='Alias database Django (default: backoffice)')

    def handle(self, *args, **options):
        path = options['jsonld_path']
        if not path.is_file():
            raise CommandError(f'File non trovato: {path}')
        try:
            nodes = objects_from(json.loads(path.read_text(encoding='utf-8-sig')))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise CommandError(f'Impossibile leggere il JSON-LD: {exc}') from exc

        ontology = [n for n in nodes if isinstance(n, dict)
                    and n.get('@id') == ONTOLOGY_URI and OWL_ONTOLOGY in n.get('@type', [])]
        if len(ontology) != 1:
            raise CommandError('Ontologia GloSIS Procedures non identificata univocamente nel file.')
        version_iris = ids(ontology[0], OWL_VERSION_IRI)
        version_infos = {x.get('@value') for x in values(ontology[0], OWL_VERSION_INFO)}
        if f'{BASE_URI}{VERSION}' not in version_iris or VERSION not in version_infos:
            raise CommandError(f'Versione non corrispondente: attesa {VERSION}; trovati {version_iris}, {version_infos}')

        records = {}
        for node in nodes:
            if not isinstance(node, dict):
                continue
            if OWL_NAMED_INDIVIDUAL not in node.get('@type', []):
                continue
            if SKOS_CONCEPT not in ids(node, RDF_TYPE):
                continue  # Esclude schema SKOS e collezioni, non sono procedure
            uri = node.get('@id', '')
            parsed = urlparse(uri)
            if not uri.startswith(BASE_URI) or not parsed.scheme or not parsed.netloc:
                raise CommandError(f'URI procedura non valido: {uri!r}')
            if uri in records:
                raise CommandError(f'URI duplicato nel file: {uri}')
            label = literal(node, SKOS_PREF_LABEL) or literal(node, SKOS_NOTATION)
            if not label:
                raise CommandError(f'Etichetta assente per {uri}')
            records[uri] = {
                'vocabulary': VOCABULARY,
                'label': label,
                'description': literal(node, SKOS_DEFINITION),
                'source_type': 'skos:Concept',
            }
        if not records:
            raise CommandError('Nessuna procedura SKOS individuata: importazione annullata.')

        database = options['database']
        dry_run = options['dry_run']
        created = updated = unchanged = 0
        try:
            with transaction.atomic(using=database):
                # Lock existing rows while deciding whether to update.
                existing = {
                    item.uri: item
                    for item in VocabularyTerm.objects.using(database)
                    .select_for_update()
                    .filter(uri__in=records, version=VERSION)
                }
                for uri, defaults in sorted(records.items()):
                    current = existing.get(uri)
                    if current is None:
                        created += 1
                        if not dry_run:
                            VocabularyTerm.objects.using(database).create(
                                uri=uri, version=VERSION, **defaults
                            )
                    elif any(getattr(current, field) != value for field, value in defaults.items()):
                        updated += 1
                        if not dry_run:
                            for field, value in defaults.items():
                                setattr(current, field, value)
                            current.save(using=database, update_fields=list(defaults))
                    else:
                        unchanged += 1
                if dry_run:
                    transaction.set_rollback(True, using=database)
        except Exception as exc:
            raise CommandError(f'Errore database ({database}): {exc}') from exc

        prefix = '[DRY RUN] ' if dry_run else ''
        self.stdout.write(self.style.SUCCESS(
            f'{prefix}GloSIS Procedures {VERSION}: {len(records)} concetti; '
            f'da creare={created}, da aggiornare={updated}, invariati={unchanged}.'
        ))
        if dry_run:
            self.stdout.write('Nessuna modifica al database.')
