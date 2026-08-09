from django.db import migrations
  
SQL_CREATE = f"""
-- Soil Indicators:
-- 

--1) rupture_resistance_cemented_soil (percentage)
CREATE OR REPLACE VIEW rupture AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, 
    l.cement_cls_id as rupture, 
    NULL AS unit, 
    NULL as method, 
    l.geom
    FROM layer_consistence_geo l
    WHERE l.cement_cls_id IS NOT NULL;

ALTER VIEW IF EXISTS rupture OWNER TO backoffice;

"""
SQL_DROP = f""" 
DROP VIEW IF EXISTS rupture CASCADE;                                                                                        

"""

### WARNING: Changes to tables will not be applied if they affect fields used in SQL views.
### It is recommended to verify the results of any new migrations generated with `makemigrations`.

class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0006_hydroptftrainingset_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
    
