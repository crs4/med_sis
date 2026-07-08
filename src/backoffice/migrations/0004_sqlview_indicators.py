from django.db import migrations
  
SQL_CREATE = f"""
-- Soil Indicators:
-- 
--1) Active carbonate (percentage)
CREATE OR REPLACE VIEW active_carbonate AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.active_caco3 as value, 
    'percentage' AS unit, 
    l.met_active_caco3_id as method, 
    l.geom
    FROM labdata_geo l
    WHERE l.active_caco3 IS NOT NULL;
ALTER VIEW IF EXISTS active_carbonate OWNER TO backoffice_user;

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
  ) AND a.p_cont IS NOT NULL AND a.met_p_cont_id = 'P_CONTENT_METHODS:OL';
ALTER VIEW IF EXISTS available_phosphorus_content OWNER TO backoffice_user;

--3) Antimony Sb (mg/kg)
CREATE OR REPLACE VIEW antimony AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.sb as value, l.met_sb_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.sb IS NOT NULL;
ALTER VIEW IF EXISTS antimony OWNER TO backoffice_user;
  
--4) Arsenic As (mg/kg)
CREATE OR REPLACE VIEW arsenic AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.horizon, 
    a.as_value as value, 'mg/kg' AS unit, a.met_as_id as method, a.geom
   FROM labdata_geo a
   WHERE a.as_value IS NOT NULL;
ALTER VIEW IF EXISTS arsenic OWNER TO backoffice_user;

--5) Available base saturation (BS) exchangeable activity (percentage) 
CREATE OR REPLACE VIEW base_saturation_exchangeable_activity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    CASE
      WHEN  ( b.corine_id IS NOT NULL AND 
             ( b.corine_id ILIKE 'CORINE:21%' OR 
               b.corine_id ILIKE 'CORINE:22%' OR 
               b.corine_id ILIKE 'CORINE:24%' ) ) OR 
            b.use_id ILIKE 'USE:A%'
      THEN
        ( a.ca + a.mg + a.k + a.na ) * 100 / NULLIF( a.cec, 0 ) 
      ELSE NULL
    END AS value,
    'percentage' AS unit, a.geom   
  FROM public.labdata_geo a, public.land_use_geo b
  WHERE a.point_id = b.id AND a.na is not null AND a.mg is not null AND a.k is not null AND a.ca is not null AND
        a.cec is not null and a.ca + a.mg + a.k + a.na <= a.cec;
ALTER VIEW IF EXISTS base_saturation_exchangeable_activity OWNER TO backoffice_user;

--6) base saturation (BS) soil_structure (percentage)
CREATE OR REPLACE VIEW base_saturation_soil_structure AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    (a.ca + a.mg + a.k + a.na) * 100 / NULLIF(a.cec, 0) AS value,
    'percentage' AS unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.na is not null AND a.mg is not null AND a.k is not null AND a.ca is not null AND
    a.cec is not null and a.ca + a.mg + a.k + a.na <= a.cec;
ALTER VIEW IF EXISTS base_saturation_soil_structure OWNER TO backoffice_user;

--7) bulk density (BD)  (g/cm3)
CREATE OR REPLACE VIEW bulk_density AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, 
    a.met_bulk_dens_id as method,
    a.texture_id AS texture,
    a.bulk_dens AS value,
    a.clay AS clay,
    'g/cm3' AS unit,
    a.geom
  FROM public.labdata_geo a
  WHERE a.bulk_dens IS NOT NULL AND a.texture_id IS NOT NULL;
ALTER VIEW IF EXISTS bulk_density OWNER TO backoffice_user;

--8) C/N ratio (unitless)
CREATE OR REPLACE VIEW c_n_ratio AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    (a.org_car / a.n_tot) as value, 
    'unitless' as unit, 
    a.geom,
    CASE
      WHEN b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:31%' OR b.corine_id ILIKE 'CORINE:32%') THEN 'F' 
      WHEN b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:23%' OR b.corine_id ILIKE 'CORINE:33%' ) THEN 'G'
      WHEN b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:21%' OR b.corine_id ILIKE 'CORINE:22%' OR b.corine_id ILIKE 'CORINE:24%' ) THEN 'C'
      WHEN b.use_id ILIKE 'USE:A%' THEN 'C'
      WHEN b.use_id ILIKE 'USE:F%' THEN 'F'
      WHEN b.use_id ILIKE 'USE:H%' THEN 'G'
      WHEN b.nc_us_species1 IS NOT NULL AND b.nc_ms_species1 IS NOT NULL AND (b.use_id ILIKE 'USE:P%' OR b.use_id ILIKE 'USE:Y%' OR b.use_id ILIKE 'USE:U%') THEN 'F'
      WHEN b.nc_us_species1 IS NULL AND b.nc_ms_species1 IS NULL AND (b.use_id ILIKE 'USE:P%' OR b.use_id ILIKE 'USE:Y%' OR b.use_id ILIKE 'USE:U%') THEN 'G'
      ELSE 'O'
    END as lu_type
  FROM public.labdata_geo a, public.land_use_geo b
  WHERE a.upper = 0 AND a.point_id = b.id AND a.n_tot is not null AND a.org_car is not null AND a.n_tot > 0;
ALTER VIEW IF EXISTS c_n_ratio OWNER TO backoffice_user;

--9) Cadmium Cd (mg/kg)
CREATE OR REPLACE VIEW cadmium AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.horizon, 
    a.cd as value, a.met_cd_id as method, 'mg/kg' AS unit, a.geom
  FROM labdata_geo a
  WHERE a.cd IS NOT NULL;
ALTER VIEW IF EXISTS cadmium OWNER TO backoffice_user;

--10) carbonate content CaCo3 (percentage)
CREATE OR REPLACE VIEW carbonate_content AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.caco3_content as value, l.met_caco3_content_id as method, 'percentage' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.caco3_content IS NOT NULL;
ALTER VIEW IF EXISTS carbonate_content OWNER TO backoffice_user; 
  
--11) Cation Exchange Capacity (cmol/Kg)
CREATE OR REPLACE VIEW cation_exchange_capacity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.cec AS value,
    'cmol/Kg' AS unit,
    a.geom
FROM
  public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
WHERE
  ( ( b.corine_id IS NOT NULL AND 
      ( b.corine_id ILIKE 'CORINE:21%' OR 
        b.corine_id ILIKE 'CORINE:22%' OR 
        b.corine_id ILIKE 'CORINE:24%' ) ) OR 
    b.use_id ILIKE 'USE:A%' ) AND 
  a.cec IS NOT NULL;
ALTER VIEW IF EXISTS cation_exchange_capacity OWNER TO backoffice_user;

--12) Cation Exchange Capacity / Clay ratio (unitless)
CREATE OR REPLACE VIEW cec_clay_ratio AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    (a.cec / a.clay) AS value,
    'unitless' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.clay is not null and a.cec is not null and a.clay > 0;
  ALTER VIEW IF EXISTS cec_clay_ratio OWNER TO backoffice_user;

--13) Chromium Cr (mg/kg)
CREATE OR REPLACE VIEW chromium AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.cr as value, l.met_cr_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.cr IS NOT NULL;
ALTER VIEW IF EXISTS chromium OWNER TO backoffice_user;

--14) Cobalt Co (mg/kg)
CREATE OR REPLACE VIEW cobalt AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.co as value, l.met_co_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.co IS NOT NULL;
ALTER VIEW IF EXISTS cobalt OWNER TO backoffice_user; 

--15) Copper Cu (mg/kg)
CREATE OR REPLACE VIEW copper AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.cu as value, l.met_cu_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.cu IS NOT NULL;
ALTER VIEW IF EXISTS copper OWNER TO backoffice_user;

--16) Copper Relative Content (percentage)
CREATE OR REPLACE VIEW copper_relative_content AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    (a.cu / (a.cu + a.zn + a.pb))*100  AS value,
    'percentage' as unit, a.geom  
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS copper_relative_content OWNER TO backoffice_user;

--17) Crust Cover (percentage)
CREATE OR REPLACE VIEW crust_cover AS
  SELECT a.id, a.id AS point_id, a.type_id as point_type, a.date, NULL as upper, NULL as lower, a.survey_m_id, NULL as horizon, a.project, NULL as method,
     b.crust_area as value,
     'percentage' AS unit, 
     ST_SetSRID( ST_MakePoint( a.lon_wgs84, a.lat_wgs84 ), 4326 ) AS geom
  FROM public.point_general a
  JOIN public.surface b ON a.id = b.id
  JOIN public.climate_weather c ON a.id = c.id
WHERE c.clim_koppen_id IN ('CLIMATE_KOPPEN:BSH', 'CLIMATE_KOPPEN:BSC', 'CLIMATE_KOPPEN:BWH', 'CLIMATE_KOPPEN:BWC') AND b.crust_area IS NOT NULL;
ALTER VIEW IF EXISTS crust_cover OWNER TO backoffice_user; 

--18) Cryptogram Cover (percentage)
CREATE OR REPLACE VIEW cryptogram_cover AS
  SELECT a.id, a.id AS point_id, a.type_id as point_type, a.date, NULL as upper, NULL as lower, a.survey_m_id, NULL as horizon, a.project, NULL as method,
  CASE
    WHEN 
      b.nc_gs_area IS NULL AND 
      b.nc_us_area IS NULL AND 
      b.nc_ms_area IS NULL AND 
      b.cult_area IS NULL
    THEN NULL
    WHEN 
      b.nc_gs_veget1_id = 'VEGETATION_TYPES:NG' OR 
      b.nc_gs_veget2_id = 'VEGETATION_TYPES:NG' OR 
      b.nc_gs_veget3_id = 'VEGETATION_TYPES:NG'
    THEN 0
    WHEN  
      b.nc_gs_veget1_id IN ('VEGETATION_TYPES:CR','VEGETATION_TYPES:NF','VEGETATION_TYPES:NL','VEGETATION_TYPES:NM','VEGETATION_TYPES:NP') OR 
      b.nc_gs_veget2_id IN ('VEGETATION_TYPES:CR','VEGETATION_TYPES:NF','VEGETATION_TYPES:NL','VEGETATION_TYPES:NM','VEGETATION_TYPES:NP') OR 
      b.nc_gs_veget3_id IN ('VEGETATION_TYPES:CR','VEGETATION_TYPES:NF','VEGETATION_TYPES:NL','VEGETATION_TYPES:NM','VEGETATION_TYPES:NP')
    THEN COALESCE(b.nc_gs_area,0)
    ELSE NULL
  END AS value,
  'percentage' AS unit,
  ST_SetSRID( ST_MakePoint( a.lon_wgs84, a.lat_wgs84 ), 4326 ) AS geom
FROM public.point_general a JOIN public.land_use b ON a.id = b.id; 
ALTER VIEW IF EXISTS cryptogram_cover OWNER TO backoffice_user;

--19) Effective Cation Exchange Capacity (percentage)
CREATE OR REPLACE VIEW effective_cation_exchange_capacity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    CASE
      WHEN  ( ( b.corine_id IS NOT NULL AND 
                ( b.corine_id ILIKE 'CORINE:21%' OR 
                  b.corine_id ILIKE 'CORINE:22%' OR 
                  b.corine_id ILIKE 'CORINE:24%' ) ) 
              OR b.use_id ILIKE 'USE:A%' ) AND 
            (a.cec/a.clay) < 0.24 AND 
            a.ph_h2o < 6.5
      THEN 1.02 *(a.ca +a.mg +a.na +a.k)
      WHEN  ( ( b.corine_id IS NOT NULL AND 
                ( b.corine_id ILIKE 'CORINE:21%' OR 
                  b.corine_id ILIKE 'CORINE:22%' OR 
                  b.corine_id ILIKE 'CORINE:24%' ) ) 
              OR b.use_id ILIKE 'USE:A%' ) AND 
            (a.cec/a.clay) < 0.24 AND 
            a.ph_h2o >= 6.5
    THEN 0.0143 * a.clay * 10 + 0.00237 *(a.ph_h2o - 4.5) * a.clay * 10 + 0.0488 * (a.ph_h2o -1.2) * a.org_car
    ELSE NULL
    END AS value,
    'percentage' AS unit, a.geom   
  FROM public.labdata_geo a, public.land_use_geo b
  WHERE a.point_id = b.id AND a.ph_h2o is not null AND a.cec is not null AND a.clay > 0;
ALTER VIEW IF EXISTS effective_cation_exchange_capacity OWNER TO backoffice_user;

--20) Electric Conductivity EC (dS/m)
CREATE OR REPLACE VIEW electric_conductivity AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
    a.el_cond AS value, 'dS/m' AS unit, a.met_el_cond_id as method, a.geom
  FROM public.labdata_geo a
  WHERE a.el_cond IS NOT NULL; 
ALTER VIEW IF EXISTS electric_conductivity OWNER TO backoffice_user;

--21) Exchangeable Calcium - Ca  (cmol/Kg)
CREATE OR REPLACE VIEW exchangeable_calcium AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.ca as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.ca IS NOT NULL;
ALTER VIEW IF EXISTS exchangeable_calcium OWNER TO backoffice_user;

--22) Exchangeable Magnesium - Mg (cmol/Kg)
CREATE OR REPLACE VIEW exchangeable_magnesium AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.mg as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.mg IS NOT NULL;
ALTER VIEW IF EXISTS exchangeable_magnesium OWNER TO backoffice_user;

--23) Exchangeable Potassium - K (cmol/Kg)
CREATE OR REPLACE VIEW exchangeable_potassium AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.k as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.k IS NOT NULL;
ALTER VIEW IF EXISTS exchangeable_potassium OWNER TO backoffice_user; 

--24) Exchangeable Potassium (K) potential impact on produvtion (cmol/Kg)
CREATE OR REPLACE VIEW exchangeable_potassium_potential_impact AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.texture_id AS texture,
    a.k AS value,  
    'cmol/Kg' AS unit,
    a.geom
FROM public.labdata_geo a
WHERE a.k IS NOT NULL AND a.texture_id IS NOT NULL;
ALTER VIEW IF EXISTS exchangeable_potassium_potential_impact OWNER TO backoffice_user;

--25) Exchangeable Sodium - Na (cmol/Kg)
CREATE OR REPLACE VIEW exchangeable_sodium  AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.na as value, l.met_exc_id as method, 'cmol/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.na IS NOT NULL;
ALTER VIEW IF EXISTS exchangeable_sodium OWNER TO backoffice_user; 

--26) field capacity (percentage)
CREATE OR REPLACE VIEW field_capacity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.texture_id AS texture,
    a.field_cap AS value,
    'percentage' AS unit,
    a.geom
FROM
  public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  JOIN public.surface_geo c ON a.point_id = c.point_id
WHERE
    ( ( (b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:21%' OR b.corine_id ILIKE 'CORINE:22%' OR b.corine_id ILIKE 'CORINE:24%' ) ) OR b.use_id ILIKE 'USE:A%') AND (c.irrigation = 'IRRIGATION_TYPES:GR' OR c.irrigation = 'IRRIGATION_TYPES:SP' OR c.irrigation = 'IRRIGATION_TYPES:DR') )
AND a.field_cap IS NOT NULL AND a.texture_id IS NOT NULL;
ALTER VIEW IF EXISTS field_capacity OWNER TO backoffice_user;

--27) gravel (percentage)
CREATE OR REPLACE VIEW gravel AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.gravel as value, 
    'percentage' AS unit, 
    a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0;
  ALTER VIEW IF EXISTS gravel OWNER TO backoffice_user;

--28) gypsum (percentage)
CREATE OR REPLACE VIEW gypsum AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.gypsum AS value,
    'percentage' AS unit,
    a.geom
FROM
  public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE
    ( ( b.corine_id IS NOT NULL AND 
        ( b.corine_id ILIKE 'CORINE:21%' OR 
          b.corine_id ILIKE 'CORINE:22%' OR 
          b.corine_id ILIKE 'CORINE:24%' ) ) OR 
      b.use_id ILIKE 'USE:A%' ) AND 
    a.gypsum IS NOT NULL;
ALTER VIEW IF EXISTS gypsum OWNER TO backoffice_user;

--29) Hydraulic conductivity at saturation (ds/m)
CREATE OR REPLACE VIEW hydraulic_conductivity_at_saturation AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.hy_cond as value, l.met_hy_cond_id as method, 'ds/m' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.hy_cond IS NOT NULL;
ALTER VIEW IF EXISTS hydraulic_conductivity_at_saturation OWNER TO backoffice_user; 

--30) lead - Pb (mg/kg)
CREATE OR REPLACE VIEW lead AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.pb as value, l.met_pb_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.pb IS NOT NULL;
ALTER VIEW IF EXISTS lead OWNER TO backoffice_user;

--31) lead_relative_content (percentage)
CREATE OR REPLACE VIEW lead_relative_content AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    (a.pb / (a.cu + a.zn + a.pb))*100 AS value,
    'percentage' as unit, a.geom   
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS lead_relative_content OWNER TO backoffice_user;

--32) litter_layer_cover (percentage)
CREATE OR REPLACE VIEW litter_layer_cover AS
  SELECT a.id, a.id AS point_id, a.type_id as point_type, a.date, NULL as upper, NULL as lower, a.survey_m_id, NULL as horizon, a.project, NULL as method,
    b.litter_area as value,
    'percentage' AS unit,
    ST_SetSRID( ST_MakePoint( a.lon_wgs84, a.lat_wgs84 ), 4326 ) AS geom
  FROM public.point_general a, public.surface b
  WHERE a.id = b.id AND b.litter_area IS NOT NULL;
ALTER VIEW IF EXISTS litter_layer_cover OWNER TO backoffice_user; 

--33) Manganese - Mn (mg/Kg)
CREATE OR REPLACE VIEW manganese AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.mn as value, l.met_mn_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.mn IS NOT NULL;
ALTER VIEW IF EXISTS manganese OWNER TO backoffice_user; 

--34) Mercury - Hg (mg/Kg)
CREATE OR REPLACE VIEW mercury AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.hg as value, l.met_hg_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.hg IS NOT NULL;
ALTER VIEW IF EXISTS mercury OWNER TO backoffice_user;

--35) n_total (g/Kg)
CREATE OR REPLACE VIEW n_total AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.n_tot AS value,
    'g/Kg' as unit, 
    a.geom  
  FROM public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE ( ( b.corine_id IS NOT NULL AND 
              ( b.corine_id ILIKE 'CORINE:21%' OR 
                b.corine_id ILIKE 'CORINE:22%' OR 
                b.corine_id ILIKE 'CORINE:24%' ) ) OR 
            b.use_id ILIKE 'USE:A%' OR 
            ( b.corine_id IS NOT NULL AND 
              ( b.corine_id ILIKE 'CORINE:23%' OR 
                b.corine_id ILIKE 'CORINE:33%' ) ) OR 
            b.use_id ILIKE 'USE:H%' OR 
            ( b.nc_us_species1 IS NULL AND 
              b.nc_ms_species1 IS NULL AND 
              ( b.use_id ILIKE 'USE:P%' OR 
                b.use_id ILIKE 'USE:Y%' OR 
                b.use_id ILIKE 'USE:U%' ) ) ) AND 
        a.n_tot IS NOT NULL;
ALTER VIEW IF EXISTS n_total OWNER TO backoffice_user;

--36) Ammonium ion - nh4 (mg/Kg)
CREATE OR REPLACE VIEW nh4 AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.nh4 AS value,
    'mg/Kg' AS unit,
    a.geom
FROM
  public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE
    ( ( b.corine_id IS NOT NULL AND 
        ( b.corine_id ILIKE 'CORINE:21%' OR 
          b.corine_id ILIKE 'CORINE:22%' OR 
          b.corine_id ILIKE 'CORINE:24%' ) ) OR 
      b.use_id ILIKE 'USE:A%' ) AND 
    a.nh4 IS NOT NULL;
ALTER VIEW IF EXISTS nh4 OWNER TO backoffice_user;

--37) nichel - Ni (mg/Kg)
CREATE OR REPLACE VIEW nichel AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.ni as value, l.met_ni_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.ni IS NOT NULL;
ALTER VIEW IF EXISTS nichel OWNER TO backoffice_user; 
   
--38) Nitrate ion no3 (mg/Kg)
CREATE OR REPLACE VIEW no3 AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.no3 AS value,
    'mg/Kg' AS unit,
    a.geom
FROM
  public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE
    ( ( b.corine_id IS NOT NULL AND 
        ( b.corine_id ILIKE 'CORINE:21%' OR 
          b.corine_id ILIKE 'CORINE:22%' OR 
          b.corine_id ILIKE 'CORINE:24%' ) ) OR 
      b.use_id ILIKE 'USE:A%' ) AND 
    a.no3 IS NOT NULL;
ALTER VIEW IF EXISTS no3 OWNER TO backoffice_user;

--39) Organic Carbon (g/kg)
CREATE OR REPLACE VIEW organic_carbon AS
  SELECT
    a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.project, a.l_number, a.horizon, 
    a.org_car as value, 'g/kg' AS unit,  a.met_org_car_id as method, a.geom   
  FROM public.labdata_geo a
  WHERE a.org_car IS NOT NULL;
ALTER VIEW IF EXISTS organic_carbon OWNER TO backoffice_user;

--40) Organic Matter (percentage)
CREATE OR REPLACE VIEW organic_matter AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.org_mat as value, l.met_org_mat_id as method, 'percentage' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.org_mat IS NOT NULL;
ALTER VIEW IF EXISTS organic_matter OWNER TO backoffice_user;

--41) Oxygen availability for roots (unitless)
CREATE OR REPLACE VIEW oxygen_availability_for_roots AS 
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    CASE
      WHEN  ( b.corine_id IS NOT NULL AND 
              ( b.corine_id ILIKE 'CORINE:23%' OR 
                b.corine_id ILIKE 'CORINE:33%' ) ) OR
            ( b.corine_id IS NOT NULL AND 
              ( b.corine_id ILIKE 'CORINE:21%' OR 
                b.corine_id ILIKE 'CORINE:22%' OR 
                b.corine_id ILIKE 'CORINE:24%' ) ) OR
            b.use_id ILIKE 'USE:A%' OR
            b.use_id ILIKE 'USE:H%' OR
            ( b.nc_us_species1 IS NULL AND 
              b.nc_ms_species1 IS NULL AND 
              ( b.use_id ILIKE 'USE:P%' OR 
                b.use_id ILIKE 'USE:Y%' OR 
                b.use_id ILIKE 'USE:U%' ) )
      THEN
        CASE  
        WHEN a.satur > 0
          THEN ((a.satur - a.field_cap)/a.satur)^(4.0/3.0)
        WHEN a.satur IS NULL AND a.field_cap IS NOT NULL AND a.bulk_dens IS NOT NULL
          THEN ((((1 - (a.bulk_dens/2.65))*100) - a.field_cap)/( (1-(a.bulk_dens/2.65))*100))^(4.0/3.0)
        ELSE NULL
        END 
      ELSE NULL
    END AS value, 
    'unitless' AS unit,
    a.geom
  FROM public.labdata_geo a, public.land_use_geo b
  WHERE a.upper = 0 AND a.point_id = b.id;
ALTER VIEW IF EXISTS d_d0 OWNER TO backoffice_user;

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
      WHEN  a.met_p_cont_id = 'P_CONTENT_METHODS:OL' AND
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
ALTER VIEW p_p_threshold OWNER TO backoffice_user;

--43) packing density (g/cm3)
CREATE OR REPLACE VIEW packing_density AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    (a.bulk_dens + 0.009 * a.clay ) AS value,
    'g/cm3' AS unit, 
    a.geom   
  FROM public.labdata_geo a
  WHERE a.bulk_dens is not null AND a.clay is not null;
ALTER VIEW IF EXISTS packing_density OWNER TO backoffice_user;

--44) Perennial vegetation cover ( percentage )
CREATE OR REPLACE VIEW perennial_vegetation_cover AS
WITH temp_table AS (
  SELECT a.id, a.id AS point_id, a.type_id as point_type, a.date, a.survey_m_id,  a.project,
    b.cult_type_id, b.nc_gs_area, b.nc_us_area, b.nc_ms_area, b.cult_area,
    b.nc_us_veget1_id, b.nc_us_veget2_id, b.nc_us_veget3_id, b.nc_ms_veget1_id, b.nc_ms_veget2_id, b.nc_ms_veget3_id,
    ST_SetSRID( ST_MakePoint( a.lon_wgs84, a.lat_wgs84 ), 4326 ) AS geom,
    CASE
      WHEN b.nc_gs_veget1_id IN ('VEGETATION_TYPES:CR','VEGETATION_TYPES:NF','VEGETATION_TYPES:NL','VEGETATION_TYPES:NM','VEGETATION_TYPES:NP') OR 
           b.nc_gs_veget2_id IN ('VEGETATION_TYPES:CR','VEGETATION_TYPES:NF','VEGETATION_TYPES:NL','VEGETATION_TYPES:NM','VEGETATION_TYPES:NP') OR 
           b.nc_gs_veget3_id IN ('VEGETATION_TYPES:CR','VEGETATION_TYPES:NF','VEGETATION_TYPES:NL','VEGETATION_TYPES:NM','VEGETATION_TYPES:NP')
        
      THEN 0
      ELSE COALESCE(b.nc_gs_area,0)
    END AS addendum_gs,
    CASE
      WHEN b.nc_us_veget1_id = 'VEGETATION_TYPES:NO'
        OR b.nc_us_veget2_id = 'VEGETATION_TYPES:NO'
        OR b.nc_us_veget3_id = 'VEGETATION_TYPES:NO'
      THEN 0
      WHEN b.nc_us_veget1_id IN ('VEGETATION_TYPES:WH','VEGETATION_TYPES:WG','VEGETATION_TYPES:WS','VEGETATION_TYPES:WE','VEGETATION_TYPES:WT','VEGETATION_TYPES:WP','VEGETATION_TYPES:WR') OR 
           b.nc_us_veget2_id IN ('VEGETATION_TYPES:WH','VEGETATION_TYPES:WG','VEGETATION_TYPES:WS','VEGETATION_TYPES:WE','VEGETATION_TYPES:WT','VEGETATION_TYPES:WP','VEGETATION_TYPES:WR') OR 
           b.nc_us_veget3_id IN ('VEGETATION_TYPES:WH','VEGETATION_TYPES:WG','VEGETATION_TYPES:WS','VEGETATION_TYPES:WE','VEGETATION_TYPES:WT','VEGETATION_TYPES:WP','VEGETATION_TYPES:WR') 
      THEN COALESCE(b.nc_us_area,0)
      ELSE 0
    END AS addendum_us,
    CASE
      WHEN b.nc_ms_veget1_id = 'VEGETATION_TYPES:NO'
        OR b.nc_ms_veget2_id = 'VEGETATION_TYPES:NO'
        OR b.nc_ms_veget3_id = 'VEGETATION_TYPES:NO'
      THEN 0
      WHEN  b.nc_ms_veget1_id IN ('VEGETATION_TYPES:WH','VEGETATION_TYPES:WG','VEGETATION_TYPES:WS','VEGETATION_TYPES:WE','VEGETATION_TYPES:WT','VEGETATION_TYPES:WP','VEGETATION_TYPES:WR') OR
            b.nc_ms_veget2_id IN ('VEGETATION_TYPES:WH','VEGETATION_TYPES:WG','VEGETATION_TYPES:WS','VEGETATION_TYPES:WE','VEGETATION_TYPES:WT','VEGETATION_TYPES:WP','VEGETATION_TYPES:WR') OR 
            b.nc_ms_veget3_id IN ('VEGETATION_TYPES:WH','VEGETATION_TYPES:WG','VEGETATION_TYPES:WS','VEGETATION_TYPES:WE','VEGETATION_TYPES:WT','VEGETATION_TYPES:WP','VEGETATION_TYPES:WR')
      THEN COALESCE(b.nc_ms_area,0)
      ELSE 0
    END AS addendum_ms,
    CASE
      WHEN b.cult_type_id = 'CULTIVATION_TYPES:CPA'
      THEN 0
      WHEN b.cult_type_id IN ('CULTIVATION_TYPES:ACT','CULTIVATION_TYPES:AGG','CULTIVATION_TYPES:ACG', 'CULTIVATION_TYPES:GNP','CULTIVATION_TYPES:GIP','CULTIVATION_TYPES:GIN', 'CULTIVATION_TYPES:CPP','CULTIVATION_TYPES:FYO','CULTIVATION_TYPES:FOL','CULTIVATION_TYPES:FDF')
      THEN COALESCE(b.cult_area,0)
      ELSE 0
    END AS addendum_cult
    FROM public.point_general a
    JOIN public.land_use b ON a.id = b.id
)
SELECT id, point_id, point_type, date, NULL AS upper, NULL AS lower, survey_m_id, NULL as horizon, project, NULL as method, 
  CASE
    WHEN cult_type_id IN ('CULTIVATION_TYPES:ACA', 'CULTIVATION_TYPES:ACB') OR 
         ( nc_gs_area IS NULL AND nc_us_area IS NULL AND nc_ms_area IS NULL AND cult_area IS NULL )
    THEN NULL
    ELSE ( addendum_gs + addendum_us + addendum_ms + addendum_cult )
  END AS value,
  'percentage' AS unit,
  geom
FROM temp_table;
ALTER VIEW IF EXISTS perennial_vegetation_cover OWNER TO backoffice_user;

--45) pH-H2O bacterial diversity (unitless)
CREATE OR REPLACE VIEW ph_h2o_bacterial_diversity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, 
    a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_bacterial_diversity OWNER TO backoffice_user;

--46) pH-H2O fungal activity (unitless)
CREATE OR REPLACE VIEW ph_h2o_fungal AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, 
    a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_fungal OWNER TO backoffice_user;

--47)  pH-H2O metal toxicity (unitless)
CREATE OR REPLACE VIEW ph_h2o_metal_toxicity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_metal_toxicity OWNER TO backoffice_user;

--48) pH-H2O microbial carbon (unitless)
CREATE OR REPLACE VIEW ph_h2o_microbial_carbon AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, 
    a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_microbial_carbon OWNER TO backoffice_user;

--49) pH-H2O microbial diversity (unitless)
CREATE OR REPLACE VIEW ph_h2o_microbial_diversity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_microbial_diversity OWNER TO backoffice_user;

--50) pH-H2O organic decomposition (unitless)
CREATE OR REPLACE VIEW ph_h2o_organic_decomposition AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit,
    a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_organic_decomposition OWNER TO backoffice_user;

--51) pH-H2O phosphorus (unitless)
CREATE OR REPLACE VIEW ph_h2o_phosphorus AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_phosphorus OWNER TO backoffice_user;

--52) pH-H2O plant growth (unitless)
CREATE OR REPLACE VIEW ph_h2o_plant_growth AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, a.geom   
  FROM
  public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE
    ( ( b.corine_id IS NOT NULL AND 
        ( b.corine_id ILIKE 'CORINE:21%' OR 
          b.corine_id ILIKE 'CORINE:22%' OR 
          b.corine_id ILIKE 'CORINE:24%' ) ) OR 
      b.use_id ILIKE 'USE:A%' ) AND 
    a.ph_h2o IS NOT NULL;
  ALTER VIEW IF EXISTS ph_h2o_plant_growth OWNER TO backoffice_user;

--53) pH-H2O soil salinity (unitless)
CREATE OR REPLACE VIEW ph_h2o_soil_salinity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, 
    a.geom   
  FROM public.labdata_geo a;
  ALTER VIEW IF EXISTS ph_h2o_soil_salinity OWNER TO backoffice_user;

--54) pH-H2O som_for_grassland (unitless)
CREATE OR REPLACE VIEW ph_h2o_som_for_grassland AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    a.ph_h2o as value, 
    'unitless' AS unit, 
    a.geom
FROM
  public.labdata_geo a JOIN public.land_use_geo b ON a.point_id = b.id
  WHERE
    ( b.corine_id ILIKE 'CORINE:23%' OR 
      b.corine_id ILIKE 'CORINE:33%' OR 
      b.use_id ILIKE 'USE:H%' OR 
      ( b.nc_us_species1 IS NULL AND 
        b.nc_ms_species1 IS NULL AND 
        ( b.use_id ILIKE 'USE:P%' OR 
          b.use_id ILIKE 'USE:Y%' OR 
          b.use_id ILIKE 'USE:U%' ) ) ) AND 
    a.ph_h2o IS NOT NULL;
ALTER VIEW IF EXISTS ph_h2o_som_for_grassland OWNER TO backoffice_user;

--55) plant available water capacity (percentage)
CREATE OR REPLACE VIEW plant_available_water_capacity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,
    CASE
        WHEN a.awc IS NOT NULL THEN a.awc
        ELSE (a.field_cap - a.wilting_p) 
    END AS value,
    'percentage' as unit, 
    a.geom  
  FROM public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  JOIN public.surface_geo c ON a.point_id = c.point_id
  WHERE 
    ( ( ( b.corine_id IS NOT NULL AND 
          ( b.corine_id ILIKE 'CORINE:21%' OR 
            b.corine_id ILIKE 'CORINE:22%' OR 
            b.corine_id ILIKE 'CORINE:24%' ) ) OR 
        b.use_id ILIKE 'USE:A%' OR 
        ( b.corine_id IS NOT NULL AND 
          ( b.corine_id ILIKE 'CORINE:23%' OR 
            b.corine_id ILIKE 'CORINE:33%' ) ) OR 
        b.use_id ILIKE 'USE:H%' OR 
        ( b.nc_us_species1 IS NULL AND 
          b.nc_ms_species1 IS NULL AND 
          ( b.use_id ILIKE 'USE:P%' OR 
            b.use_id ILIKE 'USE:Y%' OR 
            b.use_id ILIKE 'USE:U%' ) ) ) 
      AND  c.irrigation NOT IN ( 'IRRIGATION_TYPES:GR', 'IRRIGATION_TYPES:SP', 'IRRIGATION_TYPES:DR') ) AND
    ( a.awc IS NOT NULL OR 
      ( a.field_cap is not null AND 
        a.wilting_p is not null ) );
ALTER VIEW IF EXISTS plant_available_water_capacity OWNER TO backoffice_user;

--56) relative field capacity (unitless)
CREATE OR REPLACE VIEW relative_field_capacity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    CASE
    WHEN c.irrigation NOT IN ( 'IRRIGATION_TYPES:GR', 'IRRIGATION_TYPES:SP', 'IRRIGATION_TYPES:DR') AND
       (  ( b.corine_id IS NOT NULL AND 
            ( b.corine_id ILIKE 'CORINE:23%' OR 
              b.corine_id ILIKE 'CORINE:33%' ) ) OR
          ( b.corine_id IS NOT NULL AND 
            ( b.corine_id ILIKE 'CORINE:21%' OR 
              b.corine_id ILIKE 'CORINE:22%' OR 
              b.corine_id ILIKE 'CORINE:24%' ) ) OR
          b.use_id ILIKE 'USE:A%' OR
          b.use_id ILIKE 'USE:H%' OR
          ( b.nc_us_species1 IS NULL AND 
            b.nc_ms_species1 IS NULL AND 
            ( b.use_id ILIKE 'USE:P%' OR 
              b.use_id ILIKE 'USE:Y%' OR 
              b.use_id ILIKE 'USE:U%' ) ) )
    THEN
      CASE  
        WHEN a.satur > 0
        THEN (a.field_cap / a.satur)
        WHEN a.satur IS NULL 
        THEN (a.field_cap/((1-(a.bulk_dens/2.65))*100) )
        ELSE NULL
      END 
    ELSE NULL
    END AS value,
    'unitless' as unit, 
    a.geom 
  FROM public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  JOIN public.surface_geo c ON a.point_id = c.point_id
  WHERE a.field_cap is not null;
ALTER VIEW IF EXISTS relative_field_capacity OWNER TO backoffice_user;

--57) slake test ('unitless')
CREATE OR REPLACE VIEW slake_test AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.slake_test as value, l.met_slake_test as method, 'unitless' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.slake_test IS NOT NULL;
ALTER VIEW IF EXISTS slake_test OWNER TO backoffice_user;  

--58) soc stock ('mg.ha^-1')
CREATE OR REPLACE VIEW soc_stock AS 
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    ((a.org_car / 10) * a.bulk_dens * (a.lower - a.upper) * (1 - a.gravel/100)) as value, 
    'mg.ha^-1' AS unit,
    a.geom,
    CASE
      WHEN b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:31%' OR b.corine_id ILIKE 'CORINE:32%') THEN 'F' 
      WHEN b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:23%' OR b.corine_id ILIKE 'CORINE:33%' ) THEN 'G'
      WHEN b.corine_id IS NOT NULL AND (b.corine_id ILIKE 'CORINE:21%' OR b.corine_id ILIKE 'CORINE:22%' OR b.corine_id ILIKE 'CORINE:24%' ) THEN 'C'
      WHEN b.use_id ILIKE 'USE:A%' THEN 'C'
      WHEN b.use_id ILIKE 'USE:F%' THEN 'F'
      WHEN b.use_id ILIKE 'USE:H%' THEN 'G'
      WHEN b.nc_us_species1 IS NOT NULL AND b.nc_ms_species1 IS NOT NULL AND (b.use_id ILIKE 'USE:P%' OR b.use_id ILIKE 'USE:Y%' OR b.use_id ILIKE 'USE:U%') THEN 'F'
      WHEN b.nc_us_species1 IS NULL AND b.nc_ms_species1 IS NULL AND (b.use_id ILIKE 'USE:P%' OR b.use_id ILIKE 'USE:Y%' OR b.use_id ILIKE 'USE:U%') THEN 'G'
      ELSE 'O'
    END as lu_type
  FROM public.labdata_geo a, public.land_use_geo b
  WHERE a.upper = 0 AND a.point_id = b.id AND a.gravel is not null AND a.org_car is not null AND a.bulk_dens is not null;
ALTER VIEW IF EXISTS soc_stock OWNER TO backoffice_user;

--59) sodicity salinity ratio (unitless)
CREATE OR REPLACE VIEW sodicity_salinity_ratio AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    CASE
      WHEN a.sar IS NOT NULL THEN (a.sar/a.el_cond) 
      WHEN a.sol_na IS NOT NULL AND a.sol_ca IS NOT NULL AND a.sol_mg IS NOT NULL 
      THEN (a.sol_na / SQRT(a.sol_ca + a.sol_mg)) / a.el_cond 
      ELSE NULL
    END AS value,
    'unitless' AS unit,
    a.geom
FROM public.labdata_geo a
WHERE
    (
      a.upper = 0 AND 
      a.el_cond IS NOT NULL AND 
      a.el_cond > 0  AND
      ( a.sar IS NOT NULL OR 
        ( a.sol_na IS NOT NULL AND 
          a.met_el_cond_id = 'EL_CONDUCTIVITY_PH_METHODS:SP' AND 
          a.met_sol_cations_id = 'SOLUBLE_CATIONS_METHODS:SSE' AND 
          a.sol_ca IS NOT NULL AND 
          a.sol_mg IS NOT NULL AND 
          a.sol_ca + a.sol_mg > 0 AND 
          a.el_cond > 0.2 AND 
          a.el_cond < 20 ) ) );
ALTER VIEW IF EXISTS sodicity_salinity_ratio OWNER TO backoffice_user;

--60) sodium adsorption ratio sodicity (cmol(c)^(1/2).L^(-1/2))
CREATE OR REPLACE VIEW sodium_adsorption_ratio_sodicity AS
SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
  CASE
    WHEN a.sar IS NOT NULL 
    THEN a.sar
    ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg))
  END AS value,
  'cmol(c)^(1/2).L^(-1/2)' AS unit,
  a.geom
FROM public.labdata_geo a
WHERE
    a.met_sol_cations_id = 'SOLUBLE_CATIONS_METHODS:SSE' AND
	  ( a.sar IS NOT NULL OR 
      ( a.sol_na IS NOT NULL AND 
        a.sol_ca IS NOT NULL AND 
        a.sol_mg IS NOT NULL AND 
        a.sol_ca + a.sol_mg > 0
	    ) ) ;
ALTER VIEW IF EXISTS sodium_adsorption_ratio_sodicity OWNER TO backoffice_user;

--61) sodium adsorption ratio toxicity (cmol(c)^(1/2).L^(-1/2))
CREATE OR REPLACE VIEW sodium_adsorption_ratio_toxicity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    CASE
        WHEN a.sar IS NOT NULL THEN a.sar
        ELSE (a.sol_na / SQRT(a.sol_ca + a.sol_mg))
    END AS value,
    'cmol(c)^(1/2).L^(-1/2)' AS unit,
    a.geom
  FROM public.labdata_geo a
  JOIN public.land_use_geo b ON a.point_id = b.id
  JOIN public.surface_geo c ON a.point_id = c.point_id
  WHERE
    ( ( ( ( b.corine_id IS NOT NULL AND 
           ( b.corine_id ILIKE 'CORINE:21%' OR 
             b.corine_id ILIKE 'CORINE:22%' OR 
             b.corine_id ILIKE 'CORINE:24%' ) ) OR 
          b.use_id ILIKE 'USE:A%' ) AND 
        ( c.irrigation = 'IRRIGATION_TYPES:GR' OR 
          c.irrigation = 'IRRIGATION_TYPES:SP' OR 
          c.irrigation = 'IRRIGATION_TYPES:DR' ) ) AND
      a.met_sol_cations_id = 'SOLUBLE_CATIONS_METHODS:SSE' ) AND
    (
      a.sar IS NOT NULL OR 
      ( a.sol_na IS NOT NULL AND 
        a.sol_ca IS NOT NULL AND 
        a.sol_mg IS NOT NULL AND 
        a.sol_ca + a.sol_mg > 0
      )
    );
ALTER VIEW IF EXISTS sodium_adsorption_ratio_toxicity OWNER TO backoffice_user;

--62) sodium exchangeable percentage sodicity (percentage)
CREATE OR REPLACE VIEW sodium_exchangeable_percentage_sodicity AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    CASE
      WHEN a.esp IS NOT NULL THEN a.esp
      ELSE ( a.na / a.cec ) * 100
    END AS value,
    'percentage' AS unit,
    a.geom
  FROM public.labdata_geo a
  WHERE a.esp IS NOT NULL OR ( a.na IS NOT NULL AND a.cec > 0 );
ALTER VIEW IF EXISTS sodium_exchangeable_percentage_sodicity OWNER TO backoffice_user;

--63) sodium exchangeable percentage waterlogging (percentage)
CREATE OR REPLACE VIEW sodium_exchangeable_percentage_waterlogging AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    (a.cec / a.clay) AS cec_clay_ratio,
    CASE
        WHEN a.esp IS NOT NULL THEN a.esp
        ELSE (a.na / a.cec)*100
    END AS value,
    'percentage' AS unit,
    a.geom
  FROM
    public.labdata_geo a 
    JOIN public.land_use_geo b ON a.point_id = b.id
    JOIN public.surface_geo c ON a.point_id = c.point_id
  WHERE
    ( ( b.corine_id IS NOT NULL AND 
          ( b.corine_id ILIKE 'CORINE:21%' OR 
            b.corine_id ILIKE 'CORINE:22%' OR 
            b.corine_id ILIKE 'CORINE:24%' ) ) OR 
        ( b.use_id ILIKE 'USE:A%' AND 
          ( c.irrigation = 'IRRIGATION_TYPES:GR' OR 
            c.irrigation = 'IRRIGATION_TYPES:SP' OR 
            c.irrigation = 'IRRIGATION_TYPES:DR' ) ) ) AND
      a.clay IS NOT NULL AND 
      a.clay > 0 AND
	    ( a.esp IS NOT NULL OR ( a.na IS NOT NULL AND a.cec > 0 ) );
ALTER VIEW IF EXISTS sodium_exchangeable_percentage_waterlogging OWNER TO backoffice_user;

--64) soil erodibility by water (Mg.h.MJ^(-1).mm^(-1))
CREATE OR REPLACE VIEW soil_erodibility_by_water AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    GREATEST(c.grad_ups, c.grad_downs) AS max_gradient,
    ( 
      2.1 * POWER(10, -4) * (12 - (a.org_car * 1.724 / 10)) 
      * POWER((a.silt * (a.silt + a.sand)), 1.14) 
      + 3.25 * ( (
        CASE
          WHEN b.size1_id = 'AGGREGATE_SIZES:VF' THEN 1
          WHEN b.size1_id = 'AGGREGATE_SIZES:FI' THEN 2
          WHEN b.size1_id IN ('AGGREGATE_SIZES:ME', 'AGGREGATE_SIZES:CO') THEN 3
          WHEN b.size1_id IN ('AGGREGATE_SIZES:VC', 'AGGREGATE_SIZES:EC') THEN 4
          ELSE NULL
        END ) - 2 ) 
      + 2.5 * ( (
        CASE
          WHEN a.hy_cond >= 0 AND  a.hy_cond < 0.01 THEN 1
          WHEN a.hy_cond >= 0.01 AND  a.hy_cond < 0.1 THEN 2
          WHEN a.hy_cond >= 0.1 AND  a.hy_cond < 1 THEN 3
          WHEN a.hy_cond >= 1 AND  a.hy_cond < 10 THEN 4
          WHEN a.hy_cond >= 10 AND  a.hy_cond < 100 THEN 5
          WHEN a.hy_cond >= 100 THEN 6
         ELSE NULL
         END ) - 3)
    ) / (100 * 7.59) AS value,
    'Mg.h.MJ^(-1).mm^(-1)' as unit, 
    a.geom
  
  FROM public.labdata_geo a
  JOIN public.layer_structure_geo b ON a.point_id = b.point_id
  JOIN public.landform_topography c ON a.point_id = c.id 
  WHERE b.upper = 0 AND b.size1_id is NOT NULL
    AND a.org_car IS NOT NULL AND a.silt IS NOT NULL
    AND a.sand IS NOT NULL AND a.hy_cond IS NOT NULL;
ALTER VIEW IF EXISTS soil_erodibility_by_water OWNER TO backoffice_user;

--65) soil erodibility by wind (percentage)
CREATE OR REPLACE VIEW soil_erodibility_by_wind AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    CASE
      WHEN  ( b.corine_id IS NOT NULL AND 
              ( b.corine_id ILIKE 'CORINE:21%' OR 
                b.corine_id ILIKE 'CORINE:22%' OR 
                b.corine_id ILIKE 'CORINE:24%' ) ) OR
            b.use_id ILIKE 'USE:A%' 
      THEN
        ( -40.20 + 1.44 * a.sand + 1.08 * a.silt - 5.4 * a.sand / a.clay + 6.13 * a.org_car / 10 + 84.17 * a.caco3_content ) 
      END AS value,
      'percentage' AS unit,
      a.geom
  FROM public.labdata_geo a, public.land_use_geo b
  WHERE a.upper =0 AND a.point_id = b.id AND 
      a.sand IS NOT NULL AND 
      a.org_car IS NOT NULL AND 
      a.clay > 0 AND 
      a.silt IS NOT NULL AND 
      a.caco3_content IS NOT NULL;
ALTER VIEW soil_erodibility_by_wind OWNER TO backoffice_user;

--66) surface_compaction_risk (Kg.m^(-2))
CREATE OR REPLACE VIEW surface_compaction_risk  AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    CASE
	    WHEN a.sand < 13 
      THEN 0.95 + 0.016 * (a.clay + a.silt) - 0.00012 * POWER((a.clay + a.silt), 2.0)	+ EXP(-(0.49 + 0.27 * a.org_mat))
    ELSE NULL
    END AS value,
    'Kg.m^(-2)' AS unit, 
    a.geom   
  FROM public.labdata_geo a
  WHERE a.upper = 0 AND a.clay is not null AND a.silt is not null AND a.org_mat is not null;
ALTER VIEW IF EXISTS surface_compaction_risk OWNER TO backoffice_user;

--67) Total Iron - Fe (mg/kg)
CREATE OR REPLACE VIEW total_iron AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.fe_tot as value, l.met_fe_tot_id as method, 'g/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.fe_tot IS NOT NULL;
ALTER VIEW IF EXISTS total_iron OWNER TO backoffice_user;
   
--68) Vanadium V (mg/kg)
CREATE OR REPLACE VIEW vanadium AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.v as value, l.met_v_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.v IS NOT NULL;
ALTER VIEW IF EXISTS vanadium OWNER TO backoffice_user;

--69) wilting_point (percentage)
CREATE OR REPLACE VIEW wilting_point AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.wilting_p as value, l.met_s_f_w_id as method, 'percentage' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.wilting_p IS NOT NULL;
ALTER VIEW IF EXISTS wilting_point OWNER TO backoffice_user;

--70) zinc (mg/kg)
CREATE OR REPLACE VIEW zinc AS
  SELECT 
    l.id, l.point_id, l.point_type, l.date, l.upper, l.lower, l.survey_m_id, l.project, l.horizon, 
    l.zn as value, l.met_zn_id as method, 'mg/kg' AS unit, l.geom
  FROM labdata_geo l
  WHERE l.zn IS NOT NULL;
ALTER VIEW IF EXISTS zinc OWNER TO backoffice_user;

--71) zinc_relative_content (percentage)
CREATE OR REPLACE VIEW zinc_relative_content AS
  SELECT a.id, a.point_id, a.point_type, a.date, a.upper, a.lower, a.survey_m_id, a.horizon, a.project, NULL as method,  
    (a.zn / (a.cu + a.zn + a.pb))*100 AS value,
    'percentage' as unit, 
    a.geom   
  FROM public.labdata_geo a
  WHERE a.cu is not null and a.zn is not null and a.pb is not null and (a.cu + a.zn + a.pb) > 0;
  ALTER VIEW IF EXISTS zinc_relative_content OWNER TO backoffice_user;

--72)
CREATE OR REPLACE VIEW water_infiltration_potential AS
WITH 
temp1_table AS (
	SELECT id, point_id, point_type, date, upper, lower, survey_m_id, project, NULL as method, geom,  
    texture_id as texture,
	  (((hy_cond)/10)*(POWER((1-((v_c_sand/100)/0.84)),1.26))) AS ks
	FROM public.labdata_geo
),
temp2_table AS (
  SELECT *,
	  CASE 
	    WHEN texture = 'C' THEN 0.5112
	    WHEN texture = 'SiC' THEN 0.5135
	    WHEN texture = 'SC' THEN 0.5169
	    WHEN texture = 'SiCL' THEN 0.5159
	    WHEN texture = 'CL' THEN 0.5212
	    WHEN texture = 'SCL' THEN 0.5268
	    WHEN texture = 'SiL' THEN 0.5322
  	  WHEN texture = 'L' THEN 0.5607
	    WHEN texture = 'SL' THEN 0.5679
      WHEN texture = 'LS' THEN 0.5783
	    WHEN texture = 'S' THEN 0.5839
	  ELSE NULL
	END AS alfa,
	CASE 
	  WHEN texture = 'C' THEN -0.0904
	  WHEN texture = 'SiC' THEN 0.0063
	  WHEN texture = 'SC' THEN 0.0152
	  WHEN texture = 'SiCL' THEN 0.1422
	  WHEN texture = 'CL' THEN 0.2004
	  WHEN texture = 'SCL'  THEN 0.3483
	  WHEN texture = 'SiL' THEN 0.4709
  	WHEN texture = 'L' THEN 0.5080
	  WHEN texture = 'SL' THEN 0.7331
    WHEN texture = 'LS' THEN 0.8550
	  WHEN texture = 'S' THEN 1.1434
	  ELSE NULL
	END AS log_k,
  CASE 
	  WHEN texture = 'C' THEN POWER ( ( (0.5112*(POWER(10,-0.0904)))/ks),2.046)
	  WHEN texture = 'SiC' THEN POWER ( ( (0.5135*(POWER(10,0.0063)))/ks),2.055)
	  WHEN texture = 'SC' THEN POWER ( ( (0.5169*(POWER(10,0.0152)))/ks),2.069)
	  WHEN texture = 'SiCL' THEN POWER ( ( (0.5159*(POWER(10,0.1422)))/ks),2.066)
	  WHEN texture = 'CL' THEN POWER ( ( (0.5212*(POWER(10,0.2004)))/ks),2.088)
	  WHEN texture = 'SCL' THEN POWER ( ( (0.5268*(POWER(10,0.3483)))/ks),2.113)
	  WHEN texture = 'SiL'  THEN POWER ( ( (0.5322*(POWER(10,0.4709)))/ks),2.138)
  	WHEN texture = 'L' THEN POWER ( ( (0.5607*(POWER(10,0.5080)))/ks),2.276)
	  WHEN texture = 'SL' THEN POWER ( ( (0.5679*(POWER(10,0.7331)))/ks),2.314)
    WHEN texture = 'LS' THEN POWER ( ( (0.5783*(POWER(10,0.8550)))/ks),2.369)
	  WHEN texture = 'S' THEN POWER ( ( (0.5839*(POWER(10,1.1434)))/ks),2.403)
	  ELSE NULL
	END AS tb
  FROM temp1_table
)

SELECT id, id as point_id, point_type, date, upper, lower, survey_m_id, project, texture, NULL as method,  
	CASE
	  WHEN tb>=1 THEN (((POWER(10,log_k)) * (POWER(1,alfa))) / NULLIF(lower - upper , 0))
	  WHEN tb<1 THEN ((((POWER(10,log_k)) * (POWER(tb,alfa))) + (ks * (1-tb)) ) / NULLIF(lower - upper, 0))
	  ELSE NULL    
	END AS value,
  'cm' AS unit,
  geom

FROM temp2_table;
ALTER VIEW IF EXISTS water_infiltration_potential OWNER TO backoffice_user;


"""
SQL_DROP = f""" 
DROP VIEW IF EXISTS active_calcium_carbonate CASCADE;
DROP VIEW IF EXISTS antimony CASCADE;
DROP VIEW IF EXISTS arsenic CASCADE;
DROP VIEW IF EXISTS available_p_content CASCADE;
DROP VIEW IF EXISTS base_saturation_exchangeable_activity CASCADE;
DROP VIEW IF EXISTS base_saturation_soil_structure CASCADE;
DROP VIEW IF EXISTS bulk_density CASCADE;
DROP VIEW IF EXISTS cadmium CASCADE; 
DROP VIEW IF EXISTS calcium_carbonate CASCADE; 
DROP VIEW IF EXISTS cation_exchange_capacity CASCADE;
DROP VIEW IF EXISTS cec_clay_ratio CASCADE;
DROP VIEW IF EXISTS chromium CASCADE;
DROP VIEW IF EXISTS cobalt CASCADE;
DROP VIEW IF EXISTS copper CASCADE;
DROP VIEW IF EXISTS copper_relative_content CASCADE;
DROP VIEW IF EXISTS crust_cover CASCADE;
DROP VIEW IF EXISTS cryptogram_cover CASCADE;
DROP VIEW IF EXISTS c_n_ratio CASCADE;
DROP VIEW IF EXISTS effective_cation_exchange_capacity CASCADE;
DROP VIEW IF EXISTS electric_conductivity CASCADE;
DROP VIEW IF EXISTS exchangeable_calcium CASCADE;
DROP VIEW IF EXISTS exchangeable_magnesium CASCADE;
DROP VIEW IF EXISTS exchangeable_potassium CASCADE;
DROP VIEW IF EXISTS exchangeable_potassium_potential_impact CASCADE;
DROP VIEW IF EXISTS exchangeable_sodium CASCADE;
DROP VIEW IF EXISTS field_capacity CASCADE;
DROP VIEW IF EXISTS gravel CASCADE;
DROP VIEW IF EXISTS gypsum CASCADE;
DROP VIEW IF EXISTS hydraulic_conductivity_at_saturation CASCADE;
DROP VIEW IF EXISTS lead CASCADE;
DROP VIEW IF EXISTS lead_relative_content CASCADE;
DROP VIEW IF EXISTS litter_layer_cover CASCADE;
DROP VIEW IF EXISTS manganese CASCADE;
DROP VIEW IF EXISTS mercury CASCADE;
DROP VIEW IF EXISTS n_total CASCADE;
DROP VIEW IF EXISTS nh4 CASCADE;
DROP VIEW IF EXISTS nichel CASCADE;
DROP VIEW IF EXISTS no3 CASCADE;
DROP VIEW IF EXISTS organic_carbon CASCADE;
DROP VIEW IF EXISTS organic_matter CASCADE;
DROP VIEW IF EXISTS oxygen_availability_for_roots CASCADE;
DROP VIEW IF EXISTS p_p_threshold CASCADE;
DROP VIEW IF EXISTS packing_density CASCADE;
DROP VIEW IF EXISTS perennial_vegetation_cover CASCADE;
DROP VIEW IF EXISTS ph_h2o_bacterial_diversity CASCADE;
DROP VIEW IF EXISTS ph_h2o_fungal CASCADE;
DROP VIEW IF EXISTS ph_h2o_metal_toxicity CASCADE;
DROP VIEW IF EXISTS ph_h2o_microbial_carbon CASCADE;
DROP VIEW IF EXISTS ph_h2o_microbial_diversity CASCADE;
DROP VIEW IF EXISTS ph_h2o_organic_decomposition CASCADE;
DROP VIEW IF EXISTS ph_h2o_phosphorus CASCADE;
DROP VIEW IF EXISTS ph_h2o_plant_growth CASCADE;
DROP VIEW IF EXISTS ph_h2o_soil_salinity CASCADE;
DROP VIEW IF EXISTS ph_h2o_som_for_grassland CASCADE;
DROP VIEW IF EXISTS plant_available_water_capacity CASCADE;
DROP VIEW IF EXISTS relative_field_capacity CASCADE; 
DROP VIEW IF EXISTS slake_test CASCADE;
DROP VIEW IF EXISTS soc_stock CASCADE;
DROP VIEW IF EXISTS sodicity_salinity_ratio CASCADE;
DROP VIEW IF EXISTS sodium_adsorption_ratio_sodicity CASCADE;
DROP VIEW IF EXISTS sodium_adsorption_ratio_toxicity CASCADE;
DROP VIEW IF EXISTS sodium_exchangeable_percentage_sodicity CASCADE;
DROP VIEW IF EXISTS sodium_exchangeable_percentage_waterlogging CASCADE;                                                                   ;
DROP VIEW IF EXISTS soil_erodibility_by_water CASCADE;
DROP VIEW IF EXISTS soil_erodibility_by_wind CASCADE;
DROP VIEW IF EXISTS surface_compaction_risk CASCADE;
DROP VIEW IF EXISTS texture CASCADE;
DROP VIEW IF EXISTS total_iron CASCADE;
DROP VIEW IF EXISTS vanadium CASCADE;
DROP VIEW IF EXISTS wilting_point CASCADE;
DROP VIEW IF EXISTS zinc CASCADE;
DROP VIEW IF EXISTS zinc_relative_content CASCADE;                                                                                         

"""

### WARNING: Changes to tables will not be applied if they affect fields used in SQL views.
### It is recommended to verify the results of any new migrations generated with `makemigrations`.

class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0003_sqlview_sections'),
    ]

    operations = [
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
    
