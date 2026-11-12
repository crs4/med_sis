from django.db import migrations
  
SQL_CREATE = f"""
-- Soil Indicators:
-- 

--2) Available Phosphorus  content (mg/Kg)
CREATE OR REPLACE VIEW available_phosphorus_content AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, 
    a.met_p_cont_id AS method,
    a.p_cont AS value, 
    'mg/Kg' as unit, 
    a.geom  
  FROM public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE 
  ( ( b.corine_id IS NOT NULL AND 
      ( b.corine_id ILIKE 'CORINE:21%' OR 
        b.corine_id ILIKE 'CORINE:22%' OR 
        b.corine_id ILIKE 'CORINE:24%' ) ) OR 
    ( b.use_id ILIKE 'USE:A%' ) OR 
    ( b.corine_id IS NOT NULL AND 
      ( b.corine_id ILIKE 'CORINE:23%' OR 
        b.corine_id ILIKE 'CORINE:33%' ) ) OR 
    ( b.use_id ILIKE 'USE:H%') OR 
    ( b.nc_us_species1 IS NULL AND b.nc_ms_species1 IS NULL AND 
      ( b.use_id ILIKE 'USE:P%' OR 
        b.use_id ILIKE 'USE:Y%' OR 
        b.use_id ILIKE 'USE:U%' ) ) 
  ) AND a.p_cont IS NOT NULL AND a.met_p_cont_id = 'P_AVAILABLE_METHODS:OL';
ALTER VIEW IF EXISTS available_phosphorus_content OWNER TO backoffice;

--42) p_p_threshold (unitless)
CREATE OR REPLACE VIEW p_p_threshold AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    CASE
      WHEN c.irrigation = 'IRRIGATION_TYPE:NA' AND 
           a.p_cont IS NOT NULL AND 
           ( ( b.corine_id IS NOT NULL AND 
               ( b.corine_id ILIKE 'CORINE:23%' OR 
                 b.corine_id ILIKE 'CORINE:33%' ) ) OR 
              b.use_id ILIKE 'USE:H%' OR 
              ( b.nc_us_species1 IS NULL AND 
                b.nc_ms_species1 IS NULL AND 
                ( b.use_id ILIKE 'USE:P%' OR 
                  b.use_id ILIKE 'USE:Y%' OR 
                  b.use_id ILIKE 'USE:U%' ) ) )
      THEN  a.p_cont / 19.4
      WHEN  a.met_p_cont_id = 'P_AVAILABLE_METHODS:OL' AND
            a.p_cont IS NOT NULL AND
            a.clay IS NOT NULL AND
            a.ph_h2o IS NOT NULL AND
            ( ( b.corine_id IS NOT NULL AND 
                ( b.corine_id ILIKE 'CORINE:21%' OR
                  b.corine_id ILIKE 'CORINE:22%' OR
                  b.corine_id ILIKE 'CORINE:24%' ) ) OR
              b.use_id ILIKE 'USE:A%' )
      THEN a.p_cont / NULLIF( 49 - 0.016 * a.clay * 10 - 3.81 * a.ph_h2o, 0)
      ELSE NULL
    END AS value,
    'unitless' AS unit,
    a.geom
  FROM public.labdata_geo a 
       JOIN public.land_use_geo b ON a.point_id = b.id
       LEFT JOIN public.surface_geo c ON a.point_id = c.id
  WHERE a."upper" = 0;
ALTER VIEW p_p_threshold OWNER TO backoffice;

"""


### WARNING: Changes to tables will not be applied if they affect fields used in SQL views.
### It is recommended to verify the results of any new migrations generated with `makemigrations`.

class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0009_semantic_vocabularies'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
    
