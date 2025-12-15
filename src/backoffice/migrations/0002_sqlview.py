from django.db import migrations
  
SQL_CREATE = f"""
--- General and Surface ---
  CREATE OR REPLACE VIEW addendum_point_general  AS 
  SELECT point_id, count(point_id) as n_layer, concat(design) as horizon_designation
  FROM point_layer
  GROUP BY point_id, design;
  
  ALTER VIEW IF EXISTS addendum_point_general OWNER TO backoffice_user;


  CREATE OR REPLACE VIEW points_geo AS
  SELECT 
    id as pointid, date, location, lat_wgs84, lon_wgs84, 
    gps, elev_m_asl, elev_dem, survey_m_id, project,
    ST_SetSRID(
      ST_MakePoint(lon_wgs84, lat_wgs84),
      4326
    ) AS geom
  FROM point_general;
  ALTER VIEW IF EXISTS points_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW point_general_geo AS
  SELECT 
    t.*, a.n_layer, a.horizon_designation,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, addendum_point_general a
  WHERE t.id = a.point_id;
  ALTER VIEW IF EXISTS point_general_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW surface_unevenness_geo AS
  SELECT
    s.*,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, surface_unevenness s
  WHERE t.surfaceunevenness_id = s.id;
  ALTER VIEW IF EXISTS surface_unevenness_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW surface_geo AS
  SELECT
    s.*,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, surface s
  WHERE t.surface_id = s.id;
  ALTER VIEW IF EXISTS surface_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW land_use_geo AS
  SELECT
    l.*,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, land_use l
  WHERE t.landuse_id = l.id;
  ALTER VIEW IF EXISTS land_use_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW climate_weather_geo AS
    SELECT
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, climate_weather c
    WHERE t.climateandweather_id = c.id;
  ALTER VIEW IF EXISTS climate_weather_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW landform_topography_geo AS
    SELECT
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, landform_topography c
    WHERE t.landformtopography_id = c.id;
  ALTER VIEW IF EXISTS landform_topography_geo OWNER TO backoffice_user;

--- Laboratory data ---
  CREATE OR REPLACE VIEW labdata_layer AS
    SELECT 
      l.id, l.point_id, t.type_id as point_type, t.project, t.date, t.survey_m_id, l.l_number, l.horizon, pl.upper, pl.lower,
      l.gravel, l.cls_sys_id, l.texture_id, l.sand, l.v_c_sand, l.c_sand, l.m_sand, l.f_sand,
      l.v_f_sand, l.met_sand_id, l.silt, l.c_silt, l.f_silt, l.met_silt_id, l.clay, l.met_clay_id,
      l.bulk_dens, l.met_bulk_dens, l.slake_test, l.met_slake_test, l.el_cond, l.met_el_cond_id,
      l.hy_cond, l.met_hy_cond_id, l.satur, l.field_cap, l.wilting_p, l.awc, l.met_s_f_w_id, l.acidity,
      l.met_acidity, l.ph_h2o, l.met_ph_h20_id, l.ph_kcl, l.met_ph_kcl_id, l.ph_ccl, l.met_ph_ccl_id,
      l.org_car, l.met_org_car_id, l.org_mat, l.met_org_mat_id, l.caco3_content, l.met_content_caco3_id,
      l.active_caco3, l.met_active_caco3_id, l.gypsum, l.met_gypsum_id, l.cec, l.met_cec_id, l.ca,
      l.met_ca_id, l.mg, l.met_mg_id, l.na, l.met_na_id, l.k, l.met_k_id, l.n_tot, l.met_n_tot_id, l.p_cont, 
      l.met_p_cont_id, l.nh4, l.met_nh4_id, l.no3, l.met_no3_id, l.roc, l.toc400, l.met_roc_toc400_id,
      l.feox, l.fed, l.fep, l.fe_tot, l.met_fe_tot_id, l.mn, l.met_mn_id, l.zn, l.met_zn_id, l.cu, l.met_cu_id,
      l.act_caco3, l.pb, l.met_pb_id, l.hg, l.met_hg_id, l.cd, l.met_cd_id, l.ni, l.met_ni_id, l.sb, l.met_sb_id,
      l.cr, l.met_cr_id, l.as_value, l.met_as_id, l.co, l.met_co_id, l.v, l.met_v_id, l.notes,
      st_setsrid(st_makepoint(t.lon_wgs84::double precision, t.lat_wgs84::double precision), 4326) AS geom
   FROM point_general t, point_layer pl, lab_data l
  WHERE l.l_number is not null AND t.id = pl.point_id AND pl.labdata_id = l.id;
  ALTER VIEW IF EXISTS labdata_layer OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_no_layer AS
    SELECT 
      l.id, l.point_id, t.type_id as point_type, t.project, t.date, t.survey_m_id, NULL::numeric(40,6) as l_number, NULL as horizon, l.upper, l.lower,
      l.gravel, l.cls_sys_id, l.texture_id, l.sand, l.v_c_sand, l.c_sand, l.m_sand, l.f_sand,
      l.v_f_sand, l.met_sand_id, l.silt, l.c_silt, l.f_silt, l.met_silt_id, l.clay, l.met_clay_id,
      l.bulk_dens, l.met_bulk_dens, l.slake_test, l.met_slake_test, l.el_cond, l.met_el_cond_id,
      l.hy_cond, l.met_hy_cond_id, l.satur, l.field_cap, l.wilting_p, l.awc, l.met_s_f_w_id, l.acidity,
      l.met_acidity, l.ph_h2o, l.met_ph_h20_id, l.ph_kcl, l.met_ph_kcl_id, l.ph_ccl, l.met_ph_ccl_id,
      l.org_car, l.met_org_car_id, l.org_mat, l.met_org_mat_id, l.caco3_content, l.met_content_caco3_id,
      l.active_caco3, l.met_active_caco3_id, l.gypsum, l.met_gypsum_id, l.cec, l.met_cec_id, l.ca,
      l.met_ca_id, l.mg, l.met_mg_id, l.na, l.met_na_id, l.k, l.met_k_id, l.n_tot, l.met_n_tot_id, l.p_cont, 
      l.met_p_cont_id, l.nh4, l.met_nh4_id, l.no3, l.met_no3_id, l.roc, l.toc400, l.met_roc_toc400_id,
      l.feox, l.fed, l.fep, l.fe_tot, l.met_fe_tot_id, l.mn, l.met_mn_id, l.zn, l.met_zn_id, l.cu, l.met_cu_id,
      l.act_caco3, l.pb, l.met_pb_id, l.hg, l.met_hg_id, l.cd, l.met_cd_id, l.ni, l.met_ni_id, l.sb, l.met_sb_id,
      l.cr, l.met_cr_id, l.as_value, l.met_as_id, l.co, l.met_co_id, l.v, l.met_v_id, l.notes,
      st_setsrid(st_makepoint(t.lon_wgs84::double precision, t.lat_wgs84::double precision), 4326) AS geom
   FROM point_general t, lab_data l
  WHERE l.l_number is null AND l.upper is not null AND t.id = l.point_id;
  ALTER VIEW IF EXISTS labdata_no_layer OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_geo AS
   SELECT * from labdata_layer
   UNION 
   SELECT * from labdata_no_layer;
  ALTER VIEW IF EXISTS labdata_geo OWNER TO backoffice_user;   

--- Layer descriptions ---
  CREATE OR REPLACE VIEW point_layer_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project, 
      l.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l
    WHERE t.id = l.point_id;
  ALTER VIEW IF EXISTS point_layer_geo OWNER TO backoffice_user;
 
  CREATE OR REPLACE VIEW layer_remants_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_remnants lr
    WHERE t.id = l.point_id and l.layerremnants_id = lr.id;
  ALTER VIEW IF EXISTS layer_remants_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_coarse_fragments_geo AS
  SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_coarse_fragments lr
    WHERE t.id = l.point_id and l.layercoarsefragments_id = lr.id;
  ALTER VIEW IF EXISTS layer_coarse_fragments_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_artefacts_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_artefacts lr
    WHERE t.id = l.point_id and l.layerartefacts_id = lr.id;
  ALTER VIEW IF EXISTS layer_artefacts_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_cracks_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_cracks lr
    WHERE t.id = l.point_id and l.layercracks_id = lr.id;
  ALTER VIEW IF EXISTS layer_cracks_geo OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW layer_matrix_colours_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_matrix_colours lr
    WHERE t.id = l.point_id and l.layermatrixcolours_id = lr.id;
  ALTER VIEW IF EXISTS layer_matrix_colours_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_lithogenic_variegates_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_lithogenic_variegates lr
    WHERE t.id = l.point_id and l.layerlithogenicvariegates_id = lr.id;
  ALTER VIEW IF EXISTS layer_lithogenic_variegates_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_redoximorphic_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_redoximorphic lr
    WHERE t.id = l.point_id and l.layerredoximorphic_id = lr.id;
  ALTER VIEW IF EXISTS layer_redoximorphic_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_coatings_bridges_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_coatings_bridges lr
    WHERE t.id = l.point_id and l.layercoatingsbridges_id = lr.id;
  ALTER VIEW IF EXISTS layer_coatings_bridges_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_carbonates_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_carbonates lr
    WHERE t.id = l.point_id and l.layercarbonates_id = lr.id;
  ALTER VIEW IF EXISTS layer_carbonates_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_gypsum_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_gypsum lr
    WHERE t.id = l.point_id and l.layergypsum_id = lr.id;
  ALTER VIEW IF EXISTS layer_gypsum_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_secondary_silica_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_secondary_silica lr
    WHERE t.id = l.point_id and l.layersecondarysilica_id = lr.id;
  ALTER VIEW IF EXISTS layer_secondary_silica_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_consistence_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_consistence lr
    WHERE t.id = l.point_id and l.layerconsistence_id = lr.id;
  ALTER VIEW IF EXISTS layer_consistence_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_permafrost_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_permafrost lr
    WHERE t.id = l.point_id and l.layerpermafrost_id = lr.id;
  ALTER VIEW IF EXISTS layer_permafrost_geo OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW layer_organic_carbon_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_organic_carbon lr
    WHERE t.id = l.point_id and l.layerorganiccarbon_id = lr.id;
  ALTER VIEW IF EXISTS layer_organic_carbon_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_roots_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_roots lr
    WHERE t.id = l.point_id and l.layerroots_id = lr.id;
  ALTER VIEW IF EXISTS layer_roots_geo OWNER TO backoffice_user;
  
  CREATE OR REPLACE VIEW layer_animal_activity_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_animal_activity lr
    WHERE t.id = l.point_id and l.layeranimalactivity_id = lr.id;
  ALTER VIEW IF EXISTS layer_animal_activity_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_human_alterations_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_human_alterations lr
    WHERE t.id = l.point_id and l.layerhumanalterations_id = lr.id;
  ALTER VIEW IF EXISTS layer_human_alterations_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_degree_decomposition_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_degree_decomposition lr
    WHERE t.id = l.point_id and l.layerdegreedecomposition_id = lr.id;
  ALTER VIEW IF EXISTS layer_degree_decomposition_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_nonmatrix_pore_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, l.id as layer_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_nonmatrix_pore lr
    WHERE t.id = l.point_id and l.layernonmatrixpore_id = lr.id;
  ALTER VIEW IF EXISTS layer_nonmatrix_pore_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW layer_structure_geo AS
    SELECT t.date, t.location, t.lat_wgs84, t.lon_wgs84, 
      t.elev_m_asl, t.elev_dem, t.survey_m_id, t.project,
      l.upper as layer_upper, l.lower as layer_lower, l.point_id, 
      lr.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l, layer_structure lr
    WHERE t.id = l.point_id and l.id = lr.layer_id;
  ALTER VIEW IF EXISTS layer_structure_geo OWNER TO backoffice_user;

  -- Soil Indicators:

  --1) Nutrient imbalance SOC Decline
  CREATE OR REPLACE VIEW nutrient_imbalance_soc_decline AS
  SELECT
    a.id as labdata_id, a.point_id, a.point_type,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.org_car / a.n_tot) as value, 
    'dimensionless' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.n_tot is not null and a.org_car is not null and a.n_tot > 0;
  ALTER VIEW IF EXISTS nutrient_imbalance_soc_decline OWNER TO backoffice_user;

  --2) Sodium exchangeable percentage 
  CREATE OR REPLACE VIEW sodium_exchangeable_percentage AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.na / a.cec)*100 AS value,
    '%' as unit, a.geom
  FROM public.labdata_geo a
  WHERE a.cec is not null and a.na is not null and a.cec > 0 ;
  ALTER VIEW IF EXISTS sodium_exchangeable_percentage OWNER TO backoffice_user;

  --3) Sodium adsorption ratio
  CREATE OR REPLACE VIEW sodium_adsorption_ratio AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.na / SQRT(a.ca + a.mg)) AS value,
    'dimensionless' as unit, a.geom  
  FROM public.labdata_geo a
  WHERE a.na IS NOT NULL and a.ca IS NOT NULL AND a.mg IS NOT NULL AND (a.ca + a.mg) > 0 ;
  ALTER VIEW IF EXISTS sodium_adsorption_ratio OWNER TO backoffice_user;

  --4) Sodicity/salinity ratio
  CREATE OR REPLACE VIEW sodicity_salinity_ratio AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.na / SQRT(a.ca + a.mg)) / a.el_cond AS value,
    'dimensionless' as unit, a.geom  
  FROM public.labdata_geo a
  WHERE a.na IS NOT NULL and a.ca IS NOT NULL AND a.mg IS NOT NULL AND 
  (a.ca + a.mg) > 0 AND a.el_cond IS NOT NULL AND a.el_cond > 0; 
  ALTER VIEW IF EXISTS sodicity_salinity_ratio OWNER TO backoffice_user;

  --5) Cupper relative content indicator 
  CREATE OR REPLACE VIEW cupper_relative_content AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.cu / (a.cu + a.zn + a.pb))*100  AS value,
    '%' as unit, a.geom  
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS cupper_relative_content OWNER TO backoffice_user;

  --6) Lead relative content indicator
  CREATE OR REPLACE VIEW lead_relative_content AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.pb / (a.cu + a.zn + a.pb))*100 AS value,
    '%' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS lead_relative_content OWNER TO backoffice_user;

  --7) Zinc relative content indicator
  CREATE OR REPLACE VIEW zinc_relative_content AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.zn / (a.cu + a.zn + a.pb))*100 AS value,
    '%' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS zinc_relative_content OWNER TO backoffice_user;

  --8) CEC/Clay ratio 
  CREATE OR REPLACE VIEW cec_clay_ratio AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    (a.cec / a.clay) AS value,
    '%' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.clay is not null and a.cec is not null and a.clay > 0;
  ALTER VIEW IF EXISTS cec_clay_ratio OWNER TO backoffice_user;

  --9) Air capacity
  CREATE OR REPLACE VIEW air_capacity AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    a.satur - a.field_cap AS value,
    '%' as unit, a.geom 
  FROM public.labdata_geo a
  WHERE a.satur is not null and a.field_cap is not null;
  ALTER VIEW IF EXISTS air_capacity OWNER TO backoffice_user;

  --10) Plant available water capacity
  CREATE OR REPLACE VIEW plant_available_water_capacity AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    a.field_cap - a.wilting_p AS value,
    '%' as unit, a.geom  
  FROM public.labdata_geo a
  WHERE a.field_cap is not null and a.wilting_p is not null;
  ALTER VIEW IF EXISTS plant_available_water_capacity OWNER TO backoffice_user;

  --11) Relative field capacity
  CREATE OR REPLACE VIEW relative_field_capacity AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    a.field_cap / a.satur AS value,
    'dimensionless' as unit, a.geom 
  FROM public.labdata_geo a
  WHERE a.satur is not null and a.field_cap is not null and a.satur > 0;
  ALTER VIEW IF EXISTS relative_field_capacity OWNER TO backoffice_user;

  --12) Soil erodibility by water
  CREATE OR REPLACE VIEW soil_erodibility_by_water AS
  SELECT
    a.id as labdata_id,
    a.date, a.upper, a.lower, a.survey_m_id, a.project,
    GREATEST(c.grad_ups, c.grad_downs) AS max_gradient,
    ( 
      2.1 * POWER(10, -4) * (12 - (a.org_car * 1.724 / 10)) 
      * POWER((a.silt * (a.silt + a.sand)), 1.14) 
      + 3.25 * (
        CASE
            WHEN b.size1_id = 'AGGREGATE_SIZES:VF' THEN 1
            WHEN b.size1_id = 'AGGREGATE_SIZES:FI' THEN 2
            WHEN b.size1_id IN ('AGGREGATE_SIZES:ME', 'AGGREGATE_SIZES:CO') THEN 3
            WHEN b.size1_id IN ('AGGREGATE_SIZES:CO', 'AGGREGATE_SIZES:EC') THEN 4
            ELSE NULL
        END - 2 ) 
      + 2.5 * (a.hy_cond - 3)
    ) / (100 * 7.59) AS value,
    'Mg.ha.h.ha^-1.MJ^-1.mm^-1' as unit, 'soil erosion' as fao_soilstat, a.geom
  FROM public.labdata_geo a, public.layer_structure_geo b, public.landform_topography c
  WHERE a.point_id = b.point_id AND a.point_id = c.id 
    AND b.layer_upper = 0 AND b.size1_id is NOT NULL
    AND a.org_car IS NOT NULL AND a.silt IS NOT NULL
    AND a.sand IS NOT NULL AND a.hy_cond IS NOT NULL;
  ALTER VIEW IF EXISTS soil_erodibility_by_water OWNER TO backoffice_user;

  

--CREATE OR REPLACE VIEW data_monitor AS
--SELECT  
-- count points per tipo
-- count points without project
    
-- count values indicator x

-- count layers

"""

SQL_DROP = f"""
  DROP VIEW IF EXISTS points_geo CASCADE;
  DROP VIEW IF EXISTS point_general_geo CASCADE;
  DROP VIEW IF EXISTS surface_unevenness_geo CASCADE;
  DROP VIEW IF EXISTS surface_geo CASCADE;
  DROP VIEW IF EXISTS land_use_geo CASCADE;
  DROP VIEW IF EXISTS climate_weather_geo CASCADE;
  DROP VIEW IF EXISTS landform_topography_geo CASCADE;
  
  DROP VIEW IF EXISTS labdata_no_layer CASCADE;
  DROP VIEW IF EXISTS labdata_layer CASCADE;
  DROP VIEW IF EXISTS labdata_geo CASCADE;
  
  DROP VIEW IF EXISTS point_layer_geo CASCADE;
  DROP VIEW IF EXISTS layer_remants_geo CASCADE; 
  DROP VIEW IF EXISTS layer_coarse_fragments_geo CASCADE; 
  DROP VIEW IF EXISTS layer_artefacts_geo CASCADE;
  DROP VIEW IF EXISTS layer_cracks_geo CASCADE; 
  DROP VIEW IF EXISTS layer_matrix_colours_geo CASCADE;
  DROP VIEW IF EXISTS layer_lithogenic_variegates_geo CASCADE;
  DROP VIEW IF EXISTS layer_redoximorphic_geo CASCADE; 
  DROP VIEW IF EXISTS layer_coatings_bridges_geo CASCADE; 
  DROP VIEW IF EXISTS layer_carbonates_geo CASCADE;
  DROP VIEW IF EXISTS layer_gypsum_geo CASCADE; 
  DROP VIEW IF EXISTS layer_secondary_silica_geo CASCADE; 
  DROP VIEW IF EXISTS layer_consistence_geo CASCADE; 
  DROP VIEW IF EXISTS layer_permafrost_geo CASCADE; 
  DROP VIEW IF EXISTS layer_organic_carbon_geo CASCADE; 
  DROP VIEW IF EXISTS layer_roots_geo CASCADE; 
  DROP VIEW IF EXISTS layer_animal_activity_geo CASCADE; 
  DROP VIEW IF EXISTS layer_human_alterations_geo CASCADE;
  DROP VIEW IF EXISTS layer_degree_decomposition_geo CASCADE; 
  DROP VIEW IF EXISTS layer_nonmatrix_pore_geo CASCADE; 
  DROP VIEW IF EXISTS layer_structure_geo  CASCADE;
  
  DROP VIEW IF EXISTS relative_field_capacity CASCADE;
  DROP VIEW IF EXISTS plant_available_water_capacity CASCADE;
  DROP VIEW IF EXISTS air_capacity CASCADE;
  DROP VIEW IF EXISTS cec_clay_ratio CASCADE;
  DROP VIEW IF EXISTS cupper_relative_content CASCADE;
  DROP VIEW IF EXISTS lead_relative_content CASCADE;
  DROP VIEW IF EXISTS zinc_relative_content CASCADE;
  DROP VIEW IF EXISTS sodicity_salinity_ratio CASCADE;
  DROP VIEW IF EXISTS sodium_adsorption_ratio CASCADE;
  DROP VIEW IF EXISTS sodium_exchangeable_percentage CASCADE;
  DROP VIEW IF EXISTS nutrient_imbalance_soc_decline CASCADE;
  DROP VIEW IF EXISTS soil_erodibility_by_water CASCADE;
  DROP VIEW IF EXISTS data_monitor CASCADE;
""" 

class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
