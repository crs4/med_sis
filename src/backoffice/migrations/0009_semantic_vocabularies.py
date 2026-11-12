from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [('backoffice', '0008_alter_layercoatingsbridges_table_comment_and_more')]

    operations = [
        migrations.AddField(
            model_name='taxonomyvalue', name='role',
            field=models.CharField(max_length=20, default='concept', choices=[('concept','Concept'),('no_data','No data'),('unknown','Unknown'),('other','Other')]),
        ),
        migrations.CreateModel(
            name='VocabularyTerm',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uri', models.URLField(max_length=1000)),
                ('vocabulary', models.CharField(max_length=100)),
                ('version', models.CharField(max_length=40)),
                ('label', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('source_type', models.CharField(max_length=100, blank=True)),
            ],
            options={'db_table':'vocabulary_term', 'constraints':[models.UniqueConstraint(fields=('uri','version'),name='uq_vocab_term_uri_version')]},
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('uri', models.URLField(max_length=1000, unique=True)),
                ('label', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('taxonomy_value', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='procedure', to='backoffice.taxonomyvalue')),
            ],
            options={'db_table':'medsis_procedure'},
        ),
        migrations.CreateModel(
            name='VocabularyMapping',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('relation', models.CharField(max_length=20, choices=[('exactMatch','Exact match'),('closeMatch','Close match'),('broadMatch','Broad match'),('narrowMatch','Narrow match'),('relatedMatch','Related match')])),
                ('status', models.CharField(max_length=20, default='proposed', choices=[('proposed','Proposed'),('verified','Verified'),('rejected','Rejected')])),
                ('notes', models.TextField(blank=True)),
                ('external_term', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medsis_mappings', to='backoffice.vocabularyterm')),
                ('taxonomy_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vocabulary_mappings', to='backoffice.taxonomyvalue')),
            ],
            options={'db_table':'taxonomy_value_mapping', 'constraints':[models.UniqueConstraint(fields=('taxonomy_value','external_term','relation'),name='uq_taxval_external_relation')]},
        ),
        migrations.CreateModel(
            name='ProcedureStep',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('position', models.PositiveIntegerField()),
                ('procedure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='backoffice.procedure')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='used_in', to='backoffice.procedure')),
            ],
            options={'db_table':'medsis_procedure_step', 'ordering':['position'], 'constraints':[models.UniqueConstraint(fields=('procedure','position'),name='uq_medsis_proc_step_position')]},
        ),
    ]
