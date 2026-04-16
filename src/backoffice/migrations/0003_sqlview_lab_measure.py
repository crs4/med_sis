from django.db import migrations
  
SQL_CREATE = f"""

--- Laboratory measures ---
--- 48 Layers

  CREATE OR REPLACE VIEW labdata_hy_cond AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.hy_cond as value, l.met_hy_cond_id as method, l.geom
    FROM labdata_geo l
    WHERE l.hy_cond IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_hy_cond OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_acidity AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.acidity as value, l.met_acidity as method, l.geom
    FROM labdata_geo l
    WHERE l.acidity IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_acidity OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ph_h2o AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.ph_h2o as value, l.met_ph_h20_id as method, l.geom
    FROM labdata_geo l
    WHERE l.ph_h2o IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ph_h2o OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ph_kcl AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.ph_kcl as value, l.met_ph_kcl_id as method, l.geom
    FROM labdata_geo l
    WHERE l.ph_kcl IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ph_kcl OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ph_ccl AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.ph_ccl as value, l.met_ph_ccl_id as method, l.geom
    FROM labdata_geo l
    WHERE l.ph_ccl IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ph_ccl OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_org_mat AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.org_mat as value, l.met_org_mat_id as method, l.geom
    FROM labdata_geo l
    WHERE l.org_mat IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_org_mat OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_org_car AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.org_car as value, l.met_org_car_id as method, l.geom
    FROM labdata_geo l
    WHERE l.org_car IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_org_car OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_caco3 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.caco3_content as value, l.met_content_caco3_id as method, l.geom
    FROM labdata_geo l
    WHERE l.caco3_content IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_caco3 OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_active_caco3 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.active_caco3 as value, l.met_active_caco3_id as method, l.geom
    FROM labdata_geo l
    WHERE l.active_caco3 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_active_caco3 OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_gypsum AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.gypsum as value, l.met_gypsum_id as method, l.geom
    FROM labdata_geo l
    WHERE l.gypsum IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_gypsum OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cec AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.cec as value, l.met_cec_id as method, l.geom
    FROM labdata_geo l
    WHERE l.cec IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cec OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_k_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.k as value, l.met_exc_id as method, l.geom
    FROM labdata_geo l
    WHERE l.k IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_k_e OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_na_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.na as value, l.met_exc_id as method, l.geom
    FROM labdata_geo l
    WHERE l.na IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_na_e OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_mg_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.mg as value, l.met_exc_id as method, l.geom
    FROM labdata_geo l
    WHERE l.mg IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_mg_e OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ca_e AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.ca as value, l.met_exc_id as method, l.geom
    FROM labdata_geo l
    WHERE l.ca IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ca_e OWNER TO backoffice_user; 
  
  CREATE OR REPLACE VIEW labdata_n_tot AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.n_tot as value, l.met_n_tot_id as method, l.geom
    FROM labdata_geo l
    WHERE l.n_tot IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_n_tot OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_p_cont AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.p_cont as value, l.met_p_cont_id as method, l.geom
    FROM labdata_geo l
    WHERE l.p_cont IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_p_cont OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_nh4 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.nh4 as value, l.met_nh4_id as method, l.geom
    FROM labdata_geo l
    WHERE l.nh4 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_nh4 OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_no3 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.no3 as value, l.met_no3_id as method, l.geom
    FROM labdata_geo l
    WHERE l.no3 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_no3 OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_roc AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.roc as value, l.geom
    FROM labdata_geo l
    WHERE l.roc IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_roc OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_toc400 AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.toc400 as value, l.met_roc_toc400_id as method, l.geom
    FROM labdata_geo l
    WHERE l.toc400 IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_toc400 OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_fe AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.feox, l.fed, l.fep, l.fe_tot as value, l.met_fe_tot_id as method, l.geom
    FROM labdata_geo l
    WHERE l.fe_tot IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_fe OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_mn AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.mn as value, l.met_mn_id as method, l.geom
    FROM labdata_geo l
    WHERE l.mn IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_mn OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_zn AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.zn as value, l.met_zn_id as method, l.geom
    FROM labdata_geo l
    WHERE l.zn IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_zn OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cu AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.cu as value, l.met_cu_id as method, l.geom
    FROM labdata_geo l
    WHERE l.cu IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cu OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_pb AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.pb as value, l.met_pb_id as method, l.geom
    FROM labdata_geo l
    WHERE l.pb IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_pb OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_hg AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.hg as value, l.met_hg_id as method, l.geom
    FROM labdata_geo l
    WHERE l.hg IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_hg OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cd AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.cd as value, l.met_cd_id as method, l.geom
    FROM labdata_geo l
    WHERE l.cd IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cd OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_ni AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.ni as value, l.met_ni_id as method, l.geom
    FROM labdata_geo l
    WHERE l.ni IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_ni OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_sb AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.sb as value, l.met_sb_id as method, l.geom
    FROM labdata_geo l
    WHERE l.sb IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_sb OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_cr AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.cr as value, l.met_cr_id as method, l.geom
    FROM labdata_geo l
    WHERE l.cr IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_cr OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_co AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.co as value, l.met_co_id as method, l.geom
    FROM labdata_geo l
    WHERE l.co IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_co OWNER TO backoffice_user; 

  CREATE OR REPLACE VIEW labdata_v AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.v as value, l.met_v_id as method, l.geom
    FROM labdata_geo l
    WHERE l.v IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_v OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_bulk_dens AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.bulk_dens as value, l.met_bulk_dens as method,
      l.geom
    FROM labdata_geo l
    WHERE l.bulk_dens IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_bulk_dens OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_slake_test AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.slake_test as value, l.met_slake_test as method, l.geom
    FROM labdata_geo l
    WHERE l.slake_test IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_slake_test OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_el_cond AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.el_cond as value, l.met_el_cond_id as method, l.geom
    FROM labdata_geo l
    WHERE l.el_cond IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_el_cond OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_hy_cond AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.hy_cond as value, l.met_hy_cond_id as method, l.geom
    FROM labdata_geo l
    WHERE l.hy_cond IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_hy_cond OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_saturation AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.satur as value, l.met_s_f_w_id as method, l.geom
    FROM labdata_geo l
    WHERE l.satur IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_saturation OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_field_cap AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.field_cap as value, l.met_s_f_w_id as method, l.geom
    FROM labdata_geo l
    WHERE l.field_cap IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_field_cap OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_wilting_point AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.wilting_p as value, l.met_s_f_w_id as method,
      l.geom
    FROM labdata_geo l
    WHERE l.wilting_p IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_wilting_point OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_awc AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.awc as value, l.met_s_f_w_id as method, l.geom
    FROM labdata_geo l
    WHERE l.awc IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_awc OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_as AS
    SELECT 
      a.id, a.point_id, a.point_type, a.project, a.date, 
      a.survey_m_id, a.l_number, a.horizon, a.upper, a.lower,
      a.as_value as value, a.met_as_id as method, a.geom
   FROM labdata_geo a
   WHERE a.as_value IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_as OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_gravel AS
  SELECT
    a.id, a.point_id, a.point_type, a.project, a.date, 
    a.survey_m_id, a.l_number, a.horizon, a.upper, a.lower,
    a.gravel as value, a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.gravel IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_gravel OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_sand AS
    SELECT 
      a.id, a.point_id, a.point_type, a.project, a.date, 
      a.survey_m_id, a.l_number, a.horizon, a.upper, a.lower,
      a.v_c_sand, a.c_sand, a.m_sand, a.f_sand, a.v_f_sand, 
      a.sand as value, a.met_sand_id as method, a.geom
   FROM labdata_geo a
   WHERE a.sand IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_sand OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_silt AS
    SELECT 
      a.id, a.point_id, a.point_type, a.project, a.date, a.survey_m_id, 
      a.l_number, a.horizon, a.upper, a.lower, a.c_silt, a.f_silt, 
      a.silt as value, a.met_silt_id as method, a.geom
   FROM labdata_geo a
   WHERE a.silt IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_silt OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW labdata_clay AS
    SELECT 
      a.id, a.point_id, a.point_type, a.project, a.date, 
      a.survey_m_id, a.l_number, a.horizon, a.upper, a.lower,
      a.clay as value, a.met_clay_id as method, a.geom
    FROM labdata_geo a
    WHERE a.clay IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_clay OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_bulk_dens AS
    SELECT 
      l.id, l.point_id, l.point_type, l.project, l.date, 
      l.survey_m_id, l.l_number, l.horizon, l.upper, l.lower,
      l.bulk_dens as value, l.met_bulk_dens as method, l.geom
    FROM labdata_geo l
    WHERE l.bulk_dens IS NOT NULL;
  ALTER VIEW IF EXISTS labdata_bulk_dens OWNER TO backoffice_user;

"""

SQL_DROP = f"""
  DROP VIEW IF EXISTS labdata_hy_cond;
  DROP VIEW IF EXISTS labdata_acidity;
  DROP VIEW IF EXISTS labdata_ph_h2o;
  DROP VIEW IF EXISTS labdata_ph_kcl;
  DROP VIEW IF EXISTS labdata_ph_ccl;
  DROP VIEW IF EXISTS labdata_org_mat; 
  DROP VIEW IF EXISTS labdata_caco3; 
  DROP VIEW IF EXISTS labdata_active_caco3;
  DROP VIEW IF EXISTS labdata_gypsum;
  DROP VIEW IF EXISTS labdata_cec;
  DROP VIEW IF EXISTS labdata_k_e;
  DROP VIEW IF EXISTS labdata_mg_e;
  DROP VIEW IF EXISTS labdata_na_e;
  DROP VIEW IF EXISTS labdata_ca_e;
  DROP VIEW IF EXISTS labdata_n_tot;
  DROP VIEW IF EXISTS labdata_p_cont;
  DROP VIEW IF EXISTS labdata_nh4;
  DROP VIEW IF EXISTS labdata_no3;
  DROP VIEW IF EXISTS labdata_roc;
  DROP VIEW IF EXISTS labdata_toc400;   
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
  DROP VIEW IF EXISTS labdata_hy_cond; 
  DROP VIEW IF EXISTS labdata_saturation; 
  DROP VIEW IF EXISTS labdata_wilting_point; 
  DROP VIEW IF EXISTS labdata_field_cap; 
  DROP VIEW IF EXISTS labdata_clay; 
  DROP VIEW IF EXISTS labdata_silt; 
  DROP VIEW IF EXISTS labdata_awc; 
  DROP VIEW IF EXISTS labdata_gravel;
  DROP VIEW IF EXISTS labdata_sand; 
  DROP VIEW IF EXISTS labdata_as;
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
