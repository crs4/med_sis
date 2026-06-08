from django.db import migrations
  
SQL_CREATE = f"""
-- New Soil Indicators:
-- 7 layers
  CREATE OR REPLACE VIEW soc_clay_ratio AS
  SELECT
    a.id, a.point_id, a.date, a.upper, a.lower, a.survey_m_id, a.point_type, a.project, NULL as method,
    ((a.org_car /10)/ a.clay) as value, 'unitless' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.clay is not null AND a.org_car is not null AND a.clay > 0;
  ALTER VIEW IF EXISTS soc_clay_ratio OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW pd AS
  SELECT
    a.id, a.point_id, a.date, a.upper, a.lower, a.survey_m_id, a.point_type, a.project, NULL as method,
    (a.bulk_dens + 0.009 * a.clay ) AS value, 'unitless' as unit, a.geom    
  FROM public.labdata_geo a
  WHERE a.bulk_dens is not null AND a.bulk_dens is not null;
  ALTER VIEW IF EXISTS pd OWNER TO backoffice_user;
 
  CREATE OR REPLACE VIEW gapon AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, NULL as method,
    (a.na * 10 * SQRT(a.sol_ca * 10))  / NULLIF(SQRT(a.ca * 10) * a.sol_na * 10, 0) AS value, 'unitless' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.na is not null AND a.sol_ca is not null AND a.ca is not null AND a.sol_na is not null;
  ALTER VIEW IF EXISTS gapon OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW cs AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, NULL as method,
    (a.ca + a.mg + a.k + a.na) * 100 / NULLIF(a.cec, 0) AS value, 'unitless' as unit, a.geom  
  FROM public.labdata_geo a
  WHERE a.na is not null AND a.mg is not null AND a.k is not null AND a.ca is not null;
  ALTER VIEW IF EXISTS cs OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW c AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, NULL as method,
    (0.95 + 0.016 * (a.clay +a.silt) -
      0.00012 * POWER((a.clay + a.silt), 2) ) + EXP(-(0.49 + 0.27 * a.org_mat)) AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.clay is not null AND a.silt is not null AND a.org_mat is not null ;
  ALTER VIEW IF EXISTS c OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW crust_cover AS
  SELECT
    a.id, a.id as point_id, a.type_id as point_type, a.date, 0 as upper, NULL as lower, a.survey_m_id, a.project, NULL as method,
    b.crust_area as value, 'percentage' AS unit, ST_SetSRID( ST_MakePoint(a.lon_wgs84, a.lat_wgs84), 4326 ) AS geom 
  FROM public.point_general a, public.surface b
  WHERE a.id = b.id AND b.crust_area IS NOT NULL;
  ALTER VIEW IF EXISTS crust_cover OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW litter_layer_cover AS
  SELECT
    a.id, a.id as point_id, a.type_id as point_type, a.date, 0 as upper, NULL as lower, a.survey_m_id, a.project, NULL as method,
    b.litter_area as value, 'percentage' AS unit, ST_SetSRID( ST_MakePoint(a.lon_wgs84, a.lat_wgs84), 4326 ) AS geom 
  FROM public.point_general a, public.surface b
  WHERE a.id = b.id AND b.litter_area IS NOT NULL;
  ALTER VIEW IF EXISTS litter_layer_cover OWNER TO backoffice_user;

"""

SQL_DROP = f""" 
  DROP VIEW IF EXISTS soc_clay_ratio CASCADE;
"""
class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0004_sqlview_indicators'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
