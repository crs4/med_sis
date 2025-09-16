from django.db import migrations

SQL_CREATE = f"""
  CREATE OR REPLACE VIEW points_geo AS
  SELECT 
    id as point_id,date,surveyors,location,lat_wgs84,lon_wgs84,gps,elev_m_asl,
    elev_dem,survey_m,project_id,
    ST_SetSRID(
      ST_MakePoint(lon_wgs84, lat_wgs84),
      4326
    ) AS geom
  FROM point_general;

  CREATE OR REPLACE VIEW point_general_geo AS
  SELECT 
    t.id,t.date,t.surveyors,t.location,t.lat_wgs84,t.lon_wgs84,t.gps,t.elev_m_asl,
    t.elev_dem,t.survey_m, t.horizons_sequence, t.old_cls, t.new_cls, t.cls_sys, t.project_id,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t;
  ALTER VIEW IF EXISTS point_general_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW surface_unevenness_geo AS
  SELECT
    t.id as point_id ,
    s.*,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, surface_unevenness s
  WHERE t.surfaceunevenness_id = s.id;
  ALTER VIEW IF EXISTS surface_unevenness_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW surface1_geo AS
  SELECT
    t.id as point_id,
    s1.avg_thick as ll_avg_thick,
    s1.area as ll_area,
    s1.max_thick as ll_max_thick,
    s2.width1 as sc_width1, 
    s2.dist1 as sc_dist1,
    s2.spat_arr1 as  sc_spat_arr1,
    s2.persist1 as sc_persist1,
    s2.width2 as sc_width2,
    s2.dist2 as sc_dist2,
    s2.spat_arr2 as sc_spat_arr2,
    s2.persist2 as sc_persist2,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, litter_layer s1, surface_cracks s2
  WHERE t.litterlayer_id = s1.id AND t.surfacecracks_id = s2.id;
  ALTER VIEW IF EXISTS surface1_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW surface2_geo AS
  SELECT
    t.id as point_id,
    s.*,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, surface s
  WHERE t.surface_id = s.id;
  ALTER VIEW IF EXISTS surface2_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW landuse1_geo AS
  SELECT
    t.id as point_id,
    l1.corine,
    l1.land_use,
    l2.*,
    ST_SetSRID(
      ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
      4326
    ) AS geom
  FROM point_general t, land_use l1, cultivated l2
  WHERE t.landuse_id = l1.id AND l1.cultivated_id = l2.id;
  ALTER VIEW IF EXISTS landuse1_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW landuse2_geo AS
    SELECT
      t.id as point_id,
      l1.corine,
      l1.land_use,
      l2.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, land_use l1, not_cultivated l2
    WHERE t.landuse_id = l1.id AND l2.landuse_id = l1.id;
  ALTER VIEW IF EXISTS landuse2_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW climate_weather_geo AS
    SELECT
      t.id as point_id,
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, climate_weather c
    WHERE t.climateandweather_id = c.id;
  ALTER VIEW IF EXISTS climate_weather_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW coarse_fragments_geo AS
    SELECT
      t.id as point_id,
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, coarse_fragments c
    WHERE t.coarsefragments_id = c.id;
  ALTER VIEW IF EXISTS coarse_fragments_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW landform_topography_geo AS
    SELECT
      t.id as point_id,
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, landform_topography c
    WHERE t.landformtopography_id = c.id;
  ALTER VIEW IF EXISTS landform_topography_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW point_layer_geo AS
    SELECT
      t.date,
      t.project_id,
      l.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer l
    WHERE t.id = l.point_id;
  ALTER VIEW IF EXISTS point_layer_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_geo AS
    SELECT
      t.id as point_id,
      t.date,
      pl.upper,
      pl.lower,
      l.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, point_layer pl, lab_data l
    WHERE t.id = pl.point_id AND pl.labdata_id = l.id ;
  ALTER VIEW IF EXISTS labdata_geo OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW labdata_sampling_geo AS
    SELECT
      l.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM point_general t, lab_data_sampling l
    WHERE t.id = l.point_id ;
  ALTER VIEW IF EXISTS labdata_sampling_geo OWNER TO backoffice_user;
      
-- Nutrient imbalance SOC Decline
  CREATE OR REPLACE VIEW nutrient_imbalance_soc_decline AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN a.n_tot = 0 THEN NULL
          ELSE (a.org_car / a.n_tot)     
      END AS c_n
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS nutrient_imbalance_soc_decline OWNER TO backoffice_user;

  -- Sodium exchangeable percentage
  CREATE OR REPLACE VIEW sodium_exchangeable_percentage AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN a.cec = 0 THEN NULL
          ELSE (a.na / a.cec)     
      END AS esp
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS sodium_exchangeable_percentage OWNER TO backoffice_user;

  CREATE OR REPLACE VIEW sodium_adsorption_ratio AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN a.ca IS NULL OR a.mg IS NULL OR (a.ca + a.mg) = 0 THEN NULL
          ELSE (a.na / SQRT(a.ca + a.mg))
      END AS sar
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS sodium_adsorption_ratio OWNER TO backoffice_user;

  -- Sodicity/salinity ratio
  CREATE OR REPLACE VIEW sodicity_salinity_ratio AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN a.el_cond IS NULL OR a.el_cond = 0 THEN NULL
          WHEN a.ca IS NULL OR a.mg IS NULL OR (a.ca + a.mg) = 0 THEN NULL
          ELSE ( (a.na / SQRT(a.ca + a.mg)) / a.el_cond)     
      END AS sar_elcond
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS sodicity_salinity_ratio OWNER TO backoffice_user;

  -- Cupper relative content indicator 
  CREATE OR REPLACE VIEW cupper_relative_content AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN (a.cu + a.zn + a.pb) = 0 THEN NULL
          ELSE (a.cu / (a.cu + a.zn + a.pb))*100
      END AS cu_rc
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS cupper_relative_content OWNER TO backoffice_user;

  -- Lead relative content indicator
  CREATE OR REPLACE VIEW lead_relative_content AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN (a.cu + a.zn + a.pb) = 0 THEN NULL
          ELSE (a.pb / (a.cu + a.zn + a.pb))*100
      END AS pb_rc
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS lead_relative_content OWNER TO backoffice_user;

  -- Zinc relative content indicator
  CREATE OR REPLACE VIEW zinc_relative_content AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN (a.cu + a.zn + a.pb) = 0 THEN NULL
          ELSE (a.zn / (a.cu + a.zn + a.pb))*100
      END AS zn_rc
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS zinc_relative_content OWNER TO backoffice_user;

  -- CEC/Clay ratio
  CREATE OR REPLACE VIEW cec_clay_ratio AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN a.clay = 0 THEN NULL
          ELSE (a.cec / a.clay)
      END AS cec_clayratio
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS cec_clay_ratio OWNER TO backoffice_user;

  -- Air capacity
  CREATE OR REPLACE VIEW air_capacity AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      a.satur - a.field_cap AS ac
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS air_capacity OWNER TO backoffice_user;

  -- Plant available water capacity
  CREATE OR REPLACE VIEW plant_avail_water_c AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      a.field_cap - a.wilting_p AS pawc
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS plant_avail_water_c OWNER TO backoffice_user;

  -- Relative field capacity
  CREATE OR REPLACE VIEW rel_field_capacity AS
  SELECT
      a.id as labdata_id,
      b.*,
      l.upper,
      l.lower,
      CASE 
          WHEN a.satur = 0 THEN NULL
          ELSE (a.field_cap / a.satur)
      END AS rfc
  FROM public.lab_data a, points_geo b, point_layer l
  WHERE b.point_id = l.point_id and a.id = l.labdata_id;
  ALTER VIEW IF EXISTS rel_field_capacity OWNER TO backoffice_user;
"""
## todo
# coarsefragments,artefacts,cracks,stressfeatures,coatingsbridges,ribbonlikeaccumulations,
# carbonates,gypsum ,secondarysilica, consistence, surfacecrusts,permafrost,
# remnants,organiccarbon,roots,animalactivity,humanalterations,degreedecomposition,
# nonmatrixpore,labdata,matrixcolours,texturecolour,lithogenicvariegates,redoximorphicfeatures
####
## todo2 SAMPLES
SQL_DROP = f"""
  DROP VIEW IF EXISTS points_geo CASCADE;
  DROP VIEW IF EXISTS point_general_geo CASCADE;
  DROP VIEW IF EXISTS surface_unevenness_geo CASCADE;
  DROP VIEW IF EXISTS surface1_geo CASCADE;
  DROP VIEW IF EXISTS surface2_geo CASCADE;
  DROP VIEW IF EXISTS landuse1_geo CASCADE;
  DROP VIEW IF EXISTS landuse2_geo CASCADE;
  DROP VIEW IF EXISTS climate_weather_geo CASCADE;
  DROP VIEW IF EXISTS coarse_fragments_geo CASCADE;
  DROP VIEW IF EXISTS landform_topography_geo CASCADE;
  DROP VIEW IF EXISTS labdata_geo CASCADE;
  DROP VIEW IF EXISTS labdata_sampling_geo CASCADE;
  DROP VIEW IF EXISTS point_layer_geo CASCADE;
  DROP VIEW IF EXISTS rel_field_capacity CASCADE;
  DROP VIEW IF EXISTS plant_avail_water_c CASCADE;
  DROP VIEW IF EXISTS air_capacity CASCADE;
  DROP VIEW IF EXISTS cec_clay_ratio CASCADE;
  DROP VIEW IF EXISTS cupper_relative_content CASCADE;
  DROP VIEW IF EXISTS lead_relative_content CASCADE;
  DROP VIEW IF EXISTS zinc_relative_contentt CASCADE;
  DROP VIEW IF EXISTS sodicity_salinity_ratio CASCADE;
  DROP VIEW IF EXISTS sodium_adsorption_ratio CASCADE;
  DROP VIEW IF EXISTS sodium_exchangeable_percentage CASCADE;
  DROP VIEW IF EXISTS nutrient_imbalance_soc_decline CASCADE;
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
