# backoffice/migrations/0006_create_profile_general_geo_view.py
from django.db import migrations, models
import django.db.models.deletion

SQL_CREATE = f"""
    CREATE OR REPLACE VIEW profile_general_geo AS
    SELECT
      t.code,t.date,t.surveyors,t.location,t.lat_wgs84,t.lon_wgs84,t.gps,t.elev_m_asl,
      t.elev_dem,t.survey_m_id,notes,horizons,old_cls,new_cls,cls_sys_id,project_id,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t;

    CREATE OR REPLACE VIEW surface_unevenness_geo AS
    SELECT
      t.code,
      s.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, surface_unevenness s
    WHERE t.surfaceunevenness_id = s.id;

    CREATE OR REPLACE VIEW surface1_geo AS
    SELECT
      t.code,
      s1.avg_thick as ll_avg_thick,
      s1.area as ll_area,
      s1.max_thick as ll_max_thick,
      s2.width1_id as sc_width1, 
      s2.dist1_id as sc_dist1,
      s2.spat_arr1_id as  sc_spat_arr1,
      s2.persist1_id as sc_persist1,
      s2.width2_id as sc_width2,
      s2.dist2_id as sc_dist2,
      s2.spat_arr2_id as sc_spat_arr2,
      s2.persist2_id as sc_persist2,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, litter_layer s1, surface_cracks s2
    WHERE t.litterlayer_id = s1.id AND t.surfacecracks_id = s2.id;

    CREATE OR REPLACE VIEW surface2_geo AS
    SELECT
      t.code,
      s.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, surface s
    WHERE t.surface_id = s.id;

    CREATE OR REPLACE VIEW landuse1_geo AS
    SELECT
      t.code,
      l1.corine_id,
      l1.land_use_id,
      l2.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, land_use l1, cultivated l2
    WHERE t.landuse_id = l1.id AND l1.cultivated_id = l2.id;

    CREATE OR REPLACE VIEW landuse2_geo AS
    SELECT
      t.code,
      l1.corine_id,
      l1.land_use_id,
      l2.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, land_use l1, not_cultivated l2
    WHERE t.landuse_id = l1.id AND l2.landuse_id = l1.id;
    
    CREATE OR REPLACE VIEW climate_weather_geo AS
    SELECT
      t.code,
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, climate_weather c
    WHERE t.climateandweather_id = c.id;

    CREATE OR REPLACE VIEW coarse_fragments_geo AS
    SELECT
      t.code,
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, coarse_fragments c
    WHERE t.coarsefragments_id = c.id;

    CREATE OR REPLACE VIEW landform_topography_geo AS
    SELECT
      t.code,
      c.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, landform_topography c
    WHERE t.landformtopography_id = c.id;

    CREATE OR REPLACE VIEW profilelayer_geo AS
    SELECT
      t.code,
      l.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, layer l
    WHERE t.code = l.profile_id;

    CREATE OR REPLACE VIEW labdata_geo AS
    SELECT
      t.code,
      pl.design,
      pl.number,
      pl.upper,
      pl.lower,
      pl.lower_bound,
      l.*,
      ST_SetSRID(
        ST_MakePoint(t.lon_wgs84, t.lat_wgs84),
        4326
      ) AS geom
    FROM profile_general t, layer pl, lab_data l
    WHERE t.code = pl.profile_id AND pl.labdata_id = l.id;

"""
## todo
# coarsefragments,artefacts,cracks,stressfeatures,coatingsbridges,ribbonlikeaccumulations,
# carbonates,gypsum ,secondarysilica, consistence, surfacecrusts,permafrost,
# remnants,organiccarbon,roots,animalactivity,humanalterations,degreedecomposition,
# nonmatrixpore,labdata,matrixcolours,texturecolour,lithogenicvariegates,redoximorphicfeatures
####
## todo2 SAMPLES
SQL_DROP = f"""
  DROP VIEW IF EXISTS  profile_general_geo CASCADE;"
  DROP VIEW IF EXISTS  surface_unevenness_geo CASCADE;"
  DROP VIEW IF EXISTS  surface1_geo CASCADE;"
  DROP VIEW IF EXISTS  surface2_geo CASCADE;"
  DROP VIEW IF EXISTS  landuse1_geo CASCADE;"
  DROP VIEW IF EXISTS  landuse2_geo CASCADE;"
  DROP VIEW IF EXISTS  climate_weather_geo CASCADE;"
  DROP VIEW IF EXISTS  coarse_fragments_geo CASCADE;"
  DROP VIEW IF EXISTS  landform_topography_geo CASCADE;"
  DROP VIEW IF EXISTS  labdata_geo CASCADE;"
  DROP VIEW IF EXISTS  profilelayer_geo CASCADE;"

"""  
class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name="profilegeneral",
            name="surfaceunevenness",
            field=models.OneToOneField(
                db_comment="Surface Unevenness",
                default=None,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="backoffice.surfaceunevenness",
            ),
        ),
        migrations.RunSQL(
            sql=SQL_CREATE,
            reverse_sql=SQL_DROP,
        ),
    ]
