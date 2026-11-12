"""Importa solo candidati di mapping MED-SIS -> GloSIS Procedures 2.0.

Non crea Procedure, non modifica TaxonomyValue e NON approva mapping.
"""
import csv
from collections import Counter
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from backoffice.models import TaxonomyValue, VocabularyMapping, VocabularyTerm

DB = 'backoffice'
EXPECTED_VERSION = '2.0.0'
EXPECTED_VOCAB = 'glosis-proc'
EXCLUDED_CODES = {'ND', 'UN', 'OTH'}


class Command(BaseCommand):
    help = 'Importa i candidati di mapping dei metodi MED-SIS verso GloSIS 2.0 (sempre proposed).'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=Path)
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--strict', action='store_true', help='Interrompe senza scrivere se mancano termini/valori o ci sono righe incoerenti.')

    def handle(self, *args, **options):
        path = options['csv_file']
        if not path.is_file():
            raise CommandError(f'File non trovato: {path}')
        with path.open(encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream, delimiter=';')
            required = {'medsis_id', 'taxonomy', 'code', 'candidate_glosis_uri', 'mapping_relation', 'review_status'}
            if not required.issubset(reader.fieldnames or []):
                raise CommandError(f'Colonne mancanti: {sorted(required - set(reader.fieldnames or []))}')
            rows = list(reader)

        counters = Counter()
        actions = []
        issues = []
        seen = set()
        for line_no, row in enumerate(rows, 2):
            mid = (row.get('medsis_id') or '').strip()
            taxonomy = (row.get('taxonomy') or '').strip()
            code = (row.get('code') or '').strip()
            uri = (row.get('candidate_glosis_uri') or '').strip()
            status = (row.get('review_status') or '').strip()
            relation_raw = (row.get('mapping_relation') or '').strip()
            if not mid or mid != f'{taxonomy}:{code}':
                issues.append(f'Riga {line_no}: identificatore incoerente: {mid}')
                continue
            if code.upper() in EXCLUDED_CODES or status == 'no_procedure_admin_value':
                counters['administrative_skipped'] += 1
                continue
            if not uri:
                counters['no_candidate_skipped'] += 1
                continue
            if not taxonomy.endswith('_METHODS'):
                issues.append(f'Riga {line_no}: tassonomia non METHODS: {taxonomy}')
                continue
            # Un candidato parziale NON costituisce una relazione SKOS accertata.
            # Si registra closeMatch esclusivamente come relazione PROPOSTA, non pubblicabile come RDF.
            if relation_raw == 'exactMatch':
                relation = VocabularyMapping.Relation.EXACT
            elif relation_raw == 'candidate_closeMatch_not_asserted':
                relation = VocabularyMapping.Relation.CLOSE
            else:
                issues.append(f'Riga {line_no}: relazione non gestita: {relation_raw!r}')
                continue
            key = (mid, uri, relation)
            if key in seen:
                issues.append(f'Riga {line_no}: candidato duplicato: {mid} {uri}')
                continue
            seen.add(key)
            tv = TaxonomyValue.objects.using(DB).filter(pk=mid).first()
            if tv is None:
                issues.append(f'Riga {line_no}: TaxonomyValue assente: {mid}')
                continue
            term = VocabularyTerm.objects.using(DB).filter(uri=uri, version=EXPECTED_VERSION, vocabulary=EXPECTED_VOCAB).first()
            if term is None:
                issues.append(f'Riga {line_no}: URI non presente in GloSIS 2.0: {uri}')
                continue
            note = ' | '.join(x for x in [
                'Importazione Step 2b; proposta non approvata',
                f'CSV review_status={status}',
                (row.get('notes') or '').strip(),
                (row.get('recommendation') or '').strip(),
            ] if x)
            existing = VocabularyMapping.objects.using(DB).filter(taxonomy_value=tv, external_term=term, relation=relation).first()
            if existing is None:
                counters['to_create'] += 1
                actions.append(('create', tv, term, relation, note))
            elif existing.status == VocabularyMapping.Status.VERIFIED:
                counters['already_verified_preserved'] += 1
            elif existing.status == VocabularyMapping.Status.REJECTED:
                counters['rejected_preserved'] += 1
            else:
                # Non sovrascrive note/revisioni già esistenti.
                counters['existing_proposed_preserved'] += 1

        counters['csv_rows'] = len(rows)
        counters['issues'] = len(issues)
        self.stdout.write(f"CSV={counters['csv_rows']}; da creare={counters['to_create']}; "
                          f"già proposti={counters['existing_proposed_preserved']}; "
                          f"verificati preservati={counters['already_verified_preserved']}; "
                          f"rifiutati preservati={counters['rejected_preserved']}; "
                          f"amministrativi esclusi={counters['administrative_skipped']}; "
                          f"senza candidato={counters['no_candidate_skipped']}; problemi={counters['issues']}")
        for item in issues[:30]:
            self.stderr.write(self.style.WARNING(item))
        if len(issues) > 30:
            self.stderr.write(f'... e altri {len(issues) - 30} problemi')
        if options['strict'] and issues:
            raise CommandError('Modalità strict: problemi riscontrati, nessuna modifica effettuata.')
        if options['dry_run']:
            self.stdout.write(self.style.SUCCESS('[DRY RUN] Nessuna modifica al database.'))
            return
        with transaction.atomic(using=DB):
            for _, tv, term, relation, note in actions:
                VocabularyMapping.objects.using(DB).get_or_create(
                    taxonomy_value=tv, external_term=term, relation=relation,
                    defaults={'status': VocabularyMapping.Status.PROPOSED, 'notes': note},
                )
        self.stdout.write(self.style.SUCCESS(f"Importazione completata: {len(actions)} candidati elaborati (status=proposed)."))
