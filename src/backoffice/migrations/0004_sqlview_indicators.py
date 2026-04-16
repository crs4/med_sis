from django.db import migrations
  
SQL_CREATE = f"""
-- Soil Indicators:
-- 25 layers

  --1 Electric conductivity Restrictions (dS/m) 
  CREATE OR REPLACE VIEW el_cond_restrictions AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    CASE
        WHEN a.sar IS NOT NULL THEN a.sar
        ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg))
    END AS sar, a.el_cond AS value, a.geom
  FROM public.labdata_geo a
  WHERE
    ( a.el_cond IS NOT NULL AND ( a.sar IS NOT NULL
      OR ( a.sol_na IS NOT NULL AND a.sol_ca IS NOT NULL
           AND a.sol_mg IS NOT NULL AND a.sol_ca + a.sol_mg > 0 ))
    );
  ALTER VIEW IF EXISTS el_cond_restrictions OWNER TO backoffice_user;

  --2) Sodium exchangeable percentage  
  CREATE OR REPLACE VIEW sodium_exchangeable_percentage_sodicity AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    CASE
        WHEN a.esp IS NOT NULL THEN a.esp
        ELSE (a.na / a.cec)*100
    END AS value,  a.geom
  FROM public.labdata_geo a
  WHERE ( a.esp IS NOT NULL OR ( a.cec IS NOT NULL AND a.na IS NOT NULL AND a.cec > 0 ));
  ALTER VIEW IF EXISTS sodium_exchangeable_percentage_sodicity OWNER TO backoffice_user;

  --3) Sodium adsorption ratio
  CREATE OR REPLACE VIEW sodium_adsorption_ratio_sodicity AS
  SELECT a.id AS labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    CASE
      WHEN a.sar IS NOT NULL THEN a.sar
      ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg))
    END AS value, a.geom
  FROM public.labdata_geo a
  WHERE ( a.sar IS NOT NULL OR ( a.sol_na IS NOT NULL AND a.sol_ca IS NOT NULL AND a.sol_mg IS NOT NULL 
          AND a.sol_ca + a.sol_mg > 0 ));
  ALTER VIEW IF EXISTS sodium_adsorption_ratio_sodicity OWNER TO backoffice_user;

  --4) Sodicity/salinity ratio
  CREATE OR REPLACE VIEW sodicity_salinity_ratio AS
  SELECT a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    CASE
        WHEN a.sar IS NOT NULL THEN (a.sar/a.el_cond) 
        ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg)) / a.el_cond
    END AS value,  a.geom
  FROM public.labdata_geo a
  WHERE
    ( a.upper = 0 AND a.el_cond IS NOT NULL AND a.el_cond > 0  AND 
      ( a.sar IS NOT NULL OR ( a.sol_na IS NOT NULL AND a.met_el_cond_id = 'SP' AND a.sol_ca IS NOT NULL
        AND a.sol_mg IS NOT NULL AND a.sol_ca + a.sol_mg > 0 AND a.el_cond > 0.2 AND  a.el_cond < 20 )));
  ALTER VIEW IF EXISTS sodicity_salinity_ratio OWNER TO backoffice_user;

  --5) Copper relative content indicator 
  CREATE OR REPLACE VIEW copper_relative_content AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.cu / (a.cu + a.zn + a.pb))*100  AS value,  a.geom  
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS copper_relative_content OWNER TO backoffice_user;

  --6) Lead relative content indicator
  CREATE OR REPLACE VIEW lead_relative_content AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.pb / (a.cu + a.zn + a.pb))*100 AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS lead_relative_content OWNER TO backoffice_user;

  --7) Zinc relative content indicator
  CREATE OR REPLACE VIEW zinc_relative_content AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.zn / (a.cu + a.zn + a.pb))*100 AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS zinc_relative_content OWNER TO backoffice_user;

  --8) CEC/Clay ratio 
  CREATE OR REPLACE VIEW cec_clay_ratio AS
  SELECT a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.cec / a.clay) AS value, a.geom   
  FROM public.labdata_geo a
  WHERE a.clay is not null and a.cec is not null and a.clay > 0;
  ALTER VIEW IF EXISTS cec_clay_ratio OWNER TO backoffice_user;

  --9) Air capacity
  CREATE OR REPLACE VIEW air_capacity AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.satur - a.field_cap) AS value, a.geom 
  FROM public.labdata_geo a
  WHERE a.satur is not null and a.field_cap is not null;
  ALTER VIEW IF EXISTS air_capacity OWNER TO backoffice_user;

  --10) Plant available water capacity
  CREATE OR REPLACE VIEW plant_available_water_capacity AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    CASE
        WHEN a.awc IS NOT NULL THEN a.awc
        ELSE (a.field_cap - a.wilting_p) 
    END AS value, a.geom  
  FROM public.labdata_geo a
  WHERE a.awc IS NOT NULL OR (a.field_cap is not null and a.wilting_p is not null);
  ALTER VIEW IF EXISTS plant_available_water_capacity OWNER TO backoffice_user;

  --11) Relative field capacity
  CREATE OR REPLACE VIEW relative_field_capacity AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.field_cap / a.satur) AS value, a.geom 
  FROM public.labdata_geo a
  WHERE a.satur is not null and a.field_cap is not null and a.satur > 0;
  ALTER VIEW IF EXISTS relative_field_capacity OWNER TO backoffice_user;

  --12) Soil erodibility by water
  CREATE OR REPLACE VIEW soil_erodibility_by_water AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    GREATEST(c.grad_ups, c.grad_downs) AS max_gradient,
    ( 
      2.1 * POWER(10, -4) * (12 - (a.org_car * 1.724 / 10)) * POWER((a.silt * (a.silt + a.sand)), 1.14) 
      + 3.25 * ((
        CASE
          WHEN b.size1_id = 'AGGREGATE_SIZES:VF' THEN 1
          WHEN b.size1_id = 'AGGREGATE_SIZES:FI' THEN 2
          WHEN b.size1_id IN ('AGGREGATE_SIZES:ME', 'AGGREGATE_SIZES:CO') THEN 3
          WHEN b.size1_id IN ('AGGREGATE_SIZES:CO', 'AGGREGATE_SIZES:EC') THEN 4
          ELSE NULL
        END 
        ) - 2 ) + 2.5 * ( (
	      CASE
          WHEN a.hy_cond >= 0 AND  a.hy_cond < 1.27 THEN 1
          WHEN a.hy_cond >= 1.27 AND  a.hy_cond < 5.08 THEN 2
          WHEN a.hy_cond >= 5.08 AND  a.hy_cond < 20.32 THEN 3
          WHEN a.hy_cond >= 20.32 AND  a.hy_cond < 63.5 THEN 4
          WHEN a.hy_cond >= 63.5 AND  a.hy_cond < 127 THEN 5
          WHEN a.hy_cond >= 127 AND  a.hy_cond < 254 THEN 6
          WHEN a.hy_cond >= 254 THEN 7
          ELSE NULL
        END
        ) - 3)) / (100 * 7.59) AS value, a.geom
  FROM public.labdata_geo a, public.layer_structure_geo b, public.landform_topography c
  WHERE a.point_id = b.point_id AND a.point_id = c.id 
    AND b.layer_upper = 0 AND b.size1_id is NOT NULL
    AND a.org_car IS NOT NULL AND a.silt IS NOT NULL
    AND a.sand IS NOT NULL AND a.hy_cond IS NOT NULL;
  ALTER VIEW IF EXISTS soil_erodibility_by_water OWNER TO backoffice_user;

  -- 13 Sodium Exchangeable Percentage (ESP)- Waterlogging
  CREATE OR REPLACE VIEW sodium_exchangeable_percentage_waterlogging AS
  SELECT
    a.id as labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.cec / a.clay) AS cec_clay_ratio,
    CASE
        WHEN a.esp IS NOT NULL THEN a.esp
        ELSE (a.na / a.cec)*100
    END AS value, a.geom
  FROM public.labdata_geo a
  WHERE ( a.esp IS NOT NULL OR ( a.na IS NOT NULL AND a.cec IS NOT NULL AND a.cec > 0  ) )
	  AND a.clay IS NOT NULL AND a.clay > 0;
  ALTER VIEW IF EXISTS sodium_exchangeable_percentage_waterlogging OWNER TO backoffice_user;  

  -- 14 Sodium adsorption ratio (SAR) - toxicity
  CREATE OR REPLACE VIEW sodium_adsorption_ratio_toxicity AS
  SELECT
    a.id AS labdata_id, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    CASE
        WHEN a.sar IS NOT NULL THEN a.sar
        ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg))
    END AS value, a.geom
  FROM public.labdata_geo a
  WHERE ( a.sar IS NOT NULL OR ( a.sol_na IS NOT NULL AND a.sol_ca IS NOT NULL
      AND a.sol_mg IS NOT NULL AND a.sol_ca + a.sol_mg > 0 ));
  ALTER VIEW IF EXISTS sodium_adsorption_ratio_toxicity OWNER TO backoffice_user;   

  -- 15 ph H20 bacterial diversity
  CREATE OR REPLACE VIEW ph_h2o_bacterial_diversity AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    a.ph_h2o as value, a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_bacterial_diversity OWNER TO backoffice_user;  

  -- 16 ph H20 Calcite buffering 
  CREATE OR REPLACE VIEW ph_h2o_calcite_buffering AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project,
    a.ph_h2o as value, a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_calcite_buffering OWNER TO backoffice_user;

  
"""
SQL_DROP = f""" 
  DROP VIEW IF EXISTS ph_h2o_microbial_carbon CASCADE;
  DROP VIEW IF EXISTS ph_h2o_plant_growth CASCADE;
  DROP VIEW IF EXISTS ph_h2o_organic_decomposition CASCADE;
  DROP VIEW IF EXISTS ph_h2o_metal_toxicity CASCADE;
  DROP VIEW IF EXISTS ph_h2o_som_for_grassland CASCADE;
  DROP VIEW IF EXISTS ph_h2o_fungal CASCADE;
  DROP VIEW IF EXISTS ph_h2o_phosphorus CASCADE;
  DROP VIEW IF EXISTS ph_h2o_microbial_diversity CASCADE;
  DROP VIEW IF EXISTS ph_h2o_soil_salinity CASCADE;
  DROP VIEW IF EXISTS ph_h2o_calcite_buffering CASCADE;
  DROP VIEW IF EXISTS ph_h2o_bacterial_diversity CASCADE;
  DROP VIEW IF EXISTS sodium_exchangeable_percentage_waterlogging CASCADE;
  DROP VIEW IF EXISTS sodium_adsorption_ratio_toxicity CASCADE;
  DROP VIEW IF EXISTS soil_erodibility_by_water CASCADE;
  DROP VIEW IF EXISTS copper_relative_content CASCADE;
  DROP VIEW IF EXISTS plant_available_water_capacity CASCADE;
  DROP VIEW IF EXISTS relative_field_capacity CASCADE;
  DROP VIEW IF EXISTS air_capacity CASCADE;
  DROP VIEW IF EXISTS cec_clay_ratio CASCADE;
  DROP VIEW IF EXISTS zinc_relative_content CASCADE;
  DROP VIEW IF EXISTS lead_relative_content CASCADE;
  DROP VIEW IF EXISTS sodium_exchangeable_percentage CASCADE;
  DROP VIEW IF EXISTS sodium_adsorption_ratio CASCADE;
  DROP VIEW IF EXISTS sodicity_salinity_ratio CASCADE; 
  DROP VIEW IF EXISTS soil_erodibility_by_water CASCADE;
"""
class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0003_sqlview_lab_measure'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
