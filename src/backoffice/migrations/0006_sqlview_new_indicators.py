from django.db import migrations
  
SQL_CREATE = f"""
-- New Soil Indicators:
-- 5 layers
  CREATE OR REPLACE VIEW soc_clay_ratio AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    ((a.org_car /10)/ a.clay) as value, a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.clay is not null AND a.org_car is not null AND a.clay > 0;
  ALTER VIEW IF EXISTS soc_clay_ratio OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW pd AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.bulk_dens + 0.009 * a.clay ) AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.bulk_dens is not null AND a.bulk_dens is not null;
  ALTER VIEW IF EXISTS pd OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW gapon AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.na * 10 * SQRT(a.sol_ca * 10))  / NULLIF(SQRT(a.ca * 10) * a.sol_na * 10, 0) AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.na is not null AND a.sol_ca is not null AND a.ca is not null AND a.sol_na is not null;
  ALTER VIEW IF EXISTS gapon OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW cs AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.ca + a.mg + a.k + a.na) * 100 / NULLIF(a.cec, 0) AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.na is not null AND a.mg is not null AND a.k is not null AND a.ca is not null;
  ALTER VIEW IF EXISTS cs OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW c AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (0.95 + 0.016 * (a.clay +a.silt) -
      0.00012 * POWER((a.clay + a.silt), 2) ) + EXP(-(0.49 + 0.27 * a.org_mat)) AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.clay is not null AND a.silt is not null AND a.org_mat is not null ;
  ALTER VIEW IF EXISTS c OWNER TO backoffice_user;

"""

SQL_DROP = f""" 
  DROP VIEW IF EXISTS soc_clay_ratio CASCADE;
"""
class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0005_alter_layercoatingsbridges_table_comment_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
