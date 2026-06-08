from django.db import migrations
  
SQL_CREATE = f"""

--- Laboratory measures ---
--- 48 Layers
  
  CREATE OR REPLACE VIEW labdata_active_caco3 AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.active_caco3 as value, 'percentage' AS unit, l.met_active_caco3_id as method, l.geom
    FROM labdata_geo l
    WHERE l.active_caco3 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_active_caco3 OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_as AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
    a.as_value as value, 'mg/kg' AS unit, a.met_as_id as method, a.geom
   FROM labdata_geo a
   WHERE a.as_value IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_as OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_bulk_dens AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.texture_id, l.bulk_dens as value, l.met_bulk_dens as method, l.clay, 'g/cm3' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.bulk_dens IS NOT NULL AND l.texture_id IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_bulk_dens OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_caco3 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.caco3_content as value, l.met_content_caco3_id as method, 'percentage' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.caco3_content IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_caco3 OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ca_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.ca as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.ca IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ca_e OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_cec AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.cec as value, l.met_cec_id as method, 'cmol/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.cec IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cec OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cd AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.cd as value, l.met_cd_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.cd IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cd OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_co AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.co as value, l.met_co_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.co IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_co OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cr AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.cr as value, l.met_cr_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.cr IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cr OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cu AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.cu as value, l.met_cu_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.cu IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cu OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_el_cond_restrictions AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
    CASE
      WHEN a.sar IS NOT NULL THEN a.sar
      ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg))
    END AS sar,
    a.el_cond AS value, 'dS/m' AS unit, a.met_el_cond_id as method,
    a.geom
  FROM public.labdata_geo a
  WHERE ( a.el_cond IS NOT NULL AND ( a.sar IS NOT NULL
        	OR ( a.sol_na IS NOT NULL 
          AND a.sol_ca IS NOT NULL 
          AND a.sol_mg IS NOT NULL
          AND (a.sol_ca + a.sol_mg) > 0
        )
	    ));
  ALTER VIEW IF EXISTS el_cond_restrictions OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW el_cond AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
    a.el_cond AS value, 'dS/m' AS unit, a.met_el_cond_id as method, a.geom
  FROM public.labdata_geo a
  WHERE a.el_cond IS NOT NULL; 
  ALTER VIEW IF EXISTS el_cond OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_field_cap AS
  SELECT
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
    l.field_cap as value, l.texture_id, 'percentage' AS unit, l.met_s_f_w_id as method, l.geom
  FROM labdata_geo l
  WHERE l.field_cap IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_field_cap OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_fe_tot AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.fe_tot as value, l.met_fe_tot_id as method, 'g/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.fe_tot IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_fe_tot OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_gravel AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
    a.gravel as value, NULL as method, 'percentage' AS unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.gravel IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_gravel OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_gypsum AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.gypsum as value, l.met_gypsum_id as method, 'percentage' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.gypsum IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_gypsum OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_hg AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.hg as value, l.met_hg_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.hg IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_hg OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_k_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.k as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.k IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_k_e OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_mg_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.mg as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.mg IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_mg_e OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_mn AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.mn as value, l.met_mn_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.mn IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_mn OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_na_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.na as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.na IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_na_e OWNER TO backoffice_user; 
  
  CREATE OR REPLACE VIEW labdata_n_tot AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.n_tot as value, l.met_n_tot_id as method, 'g/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.n_tot IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_n_tot OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_nh4 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.nh4 as value, l.met_nh4_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.nh4 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_nh4 OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_ni AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.ni as value, l.met_ni_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.ni IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ni OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_no3 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.no3 as value, l.met_no3_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.no3 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_no3 OWNER TO backoffice_user;  

  CREATE OR REPLACE VIEW labdata_hy_cond AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.hy_cond as value, l.met_hy_cond_id as method, 'ds/m' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.hy_cond IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_hy_cond OWNER TO backoffice_user; 
  
  CREATE OR REPLACE VIEW labdata_org_car AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.org_car as value, 'g/kg' AS unit,  a.met_org_car_id as method, a.geom   
    FROM public.labdata_geo a
    WHERE a.org_car IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_org_car OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_org_mat AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.org_mat as value, l.met_org_mat_id as method, 'percentage' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.org_mat IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_org_mat OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_pb AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.pb as value, l.met_pb_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.pb IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_pb OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_ccl AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.ph_ccl as value, l.met_ph_ccl_id as method, l.geom
    FROM labdata_geo l
    WHERE l.ph_ccl IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ph_ccl OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ph_h2o_bacterial_diversity AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_bacterial_diversity OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_ph_h2o_organic_decomposition AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_organic_decomposition OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_phosphorus AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_phosphorus OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_plant_growth AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_plant_growth OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW ph_h2o_soil_salinity AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_soil_salinity OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_som_for_grassland AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_som_for_grassland OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_calcite_buffering AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_calcite_buffering OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_fungal AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_fungal OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_metal_toxicity AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_metal_toxicity OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_microbial_carbon AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_microbial_carbon OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_ph_h2o_microbial_diversity AS
    SELECT
      a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
      a.ph_h2o as value, a.met_ph_h20_id as method, 'unitless' AS unit, a.geom   
    FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS labdata_ph_h2o_microbial_diversity OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_p_cont AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.p_cont as value, l.met_p_cont_id as method, 'mg/Kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.p_cont IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_p_cont OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_sb AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.sb as value, l.met_sb_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.sb IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_sb OWNER TO backoffice_user; 
  
  CREATE OR REPLACE VIEW labdata_slake_test AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.slake_test as value, l.met_slake_test as method, 'unitless' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.slake_test IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_slake_test OWNER TO backoffice_user;  

  CREATE OR REPLACE VIEW labdata_texture AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.texture_id as value, null as method, 'unitless' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.texture_id IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_texture OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_wilting_point AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.wilting_p as value, l.met_s_f_w_id as method, 'percentage' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.wilting_p IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_wilting_point OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_v AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.v as value, l.met_v_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.v IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_v OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_zn AS
    SELECT 
      l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.l_number, l.horizon, 
      l.zn as value, l.met_zn_id as method, 'mg/kg' AS unit, l.geom
    FROM labdata_geo l
    WHERE l.zn IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_zn OWNER TO backoffice_user;


"""
SQL_DROP = f"""
  DROP VIEW IF EXISTS labdata_active_caco3;
  DROP VIEW IF EXISTS labdata_as;
  DROP VIEW IF EXISTS labdata_hy_cond;
  DROP VIEW IF EXISTS labdata_org_mat; 
  DROP VIEW IF EXISTS labdata_caco3; 
  DROP VIEW IF EXISTS labdata_gypsum;
  DROP VIEW IF EXISTS labdata_cec;
  DROP VIEW IF EXISTS labdata_k_e;
  DROP VIEW IF EXISTS labdata_mg_e;
  DROP VIEW IF EXISTS labdata_na_e;
  DROP VIEW IF EXISTS labdata_ca_e;
  DROP VIEW IF EXISTS labdata_n_tot;
  DROP VIEW IF EXISTS labdata_nh4;
  DROP VIEW IF EXISTS labdata_no3;
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
  DROP VIEW IF EXISTS labdata_ph_ccl;
  DROP VIEW IF EXISTS labdata_p_cont;
  DROP VIEW IF EXISTS labdata_fe; 
  DROP VIEW IF EXISTS labdata_mn; 
  DROP VIEW IF EXISTS labdata_zn; 
  DROP VIEW IF EXISTS labdata_cu; 
  DROP VIEW IF EXISTS labdata_cd;
  DROP VIEW IF EXISTS labdata_pb; 
  DROP VIEW IF EXISTS labdata_hg; 
  DROP VIEW IF EXISTS labdata_ni; 
  DROP VIEW IF EXISTS labdata_cr; 
  DROP VIEW IF EXISTS labdata_sb;
  DROP VIEW IF EXISTS labdata_v; 
  DROP VIEW IF EXISTS labdata_co; 
  DROP VIEW IF EXISTS labdata_v; 
  DROP VIEW IF EXISTS labdata_bulk_dens; 
  DROP VIEW IF EXISTS labdata_slake_test;
  DROP VIEW IF EXISTS labdata_el_cond;  
  DROP VIEW IF EXISTS labdata_wilting_point; 
  DROP VIEW IF EXISTS labdata_field_cap;  
  DROP VIEW IF EXISTS labdata_awc; 
  DROP VIEW IF EXISTS labdata_gravel;
  DROP VIEW IF EXISTS labdata_texture;
""" 


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0002_sqlview_sections'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
