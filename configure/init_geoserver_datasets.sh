#!/usr/bin/env bash
# Register existing GeoServer layers as GeoNode datasets.
# Run inside the Django container, from the directory containing manage.py.
set -uo pipefail

MANAGE_PY="${MANAGE_PY:-manage.py}"
PYTHON="${PYTHON:-python}"
# Edit these constants for your installation.
GEOSERVER_STORE="backoffice"
GEOSERVER_WORKSPACE="geonode" # Change to the actual GeoServer workspace
DATASET_OWNER="admin"
MANAGERS_GROUP="data-managers"
SKIP_REGISTERED=1
STOP_ON_ERROR=0
available_phosphorus_content_fine_texture
available_phosphorus_content_medium_texture
available_phosphorus_content_light_texture
LAYERS=(
  gravel carbonate_content nh4 active_carbonate antimony mercury cryptogram_cover
  c_n_ratio electric_conductivity organic_matter manganese chromium crust_cover
  exchangeable_magnesium cation_exchange_capacity cec_clay_ratio cobalt
  exchangeable_calcium exchangeable_potassium lead oxygen_availability_for_roots
  cadmium copper_relative_content gypsum litter_layer_cover no3
  lead_relative_content exchangeable_sodium hydraulic_conductivity_at_saturation
  n_total nichel organic_carbon ph_h2o_microbial_diversity soc_clay_ratio
  total_iron vanadium ph_h2o_organic_decomposition ph_h2o_metal_toxicity
  ph_h2o_microbial_carbon ph_h2o_plant_growth soil_erodibility_by_wind
  sodium_exchangeable_percentage_sodicity sodium_adsorption_ratio_toxicity
  ph_h2o_bacterial_diversity ph_h2o_fungal wilting_point
  water_infiltration_potential sodium_exchangeable_percentage_waterlogging
  soc_stock soil_erodibility_by_water slake_test zinc
  sodium_adsorption_ratio_sodicity sodicity_salinity_ratio surface_compaction_risk
  point_general_geo surface_unevenness_geo surface_geo layer_gypsum_geo
  layer_secondary_silica_geo layer_roots_geo layer_degree_decomposition_geo
  layer_structure_geo copper arsenic field_capacity
  base_saturation_soil_structure bulk_density base_saturation_exchangeable_acidity
  exchangeable_potassium_potential_impact packing_density layer_animal_activity_geo
  layer_carbonates_geo point_layer_geo effective_cation_exchange_capacity
  hydro_ptf_input_data_geo layer_lithogenic_variegates_geo layer_artefacts_geo
  layer_human_alterations_geo layer_organic_carbon_geo layer_remants_geo
  layer_matrix_colours_geo layer_nonmatrix_pore_geo available_phosphorus_content
  land_use_geo ph_h2o_soil_salinity perennial_vegetation_cover
  ph_h2o_phosphorus layer_cracks_geo rupture climate_weather_geo texture
  layer_redoximorphic_geo relative_field_capacity p_p_threshold
  ph_h2o_som_for_grassland zinc_relative_content plant_available_water_capacity
  layer_coarse_fragments_geo layer_coatings_bridges_geo
  labdata_geo layer_consistence_geo layer_permafrost_geo landform_topography_geo
)

if [[ -z "$GEOSERVER_WORKSPACE" ]]; then
  echo 'ERROR: set GEOSERVER_WORKSPACE to the actual GeoServer workspace.' >&2
  exit 2
fi
if [[ ! -f "$MANAGE_PY" ]]; then
  echo "ERROR: cannot find $MANAGE_PY; run from Django project directory or set MANAGE_PY." >&2
  exit 2
fi

ok=0; failed=0
failed_layers=()
count=${#LAYERS[@]}
echo "GeoServer workspace=$GEOSERVER_WORKSPACE store=$GEOSERVER_STORE | owner=$DATASET_OWNER | layers=$count"
for i in "${!LAYERS[@]}"; do
  layer=${LAYERS[$i]}
  echo "[$((i+1))/$count] Registering $layer"
  cmd=("$PYTHON" /usr/src/s4m_catalogue/"$MANAGE_PY" updatelayers
    --workspace "$GEOSERVER_WORKSPACE"
    --store "$GEOSERVER_STORE"
    --filter "$layer"
    --user "$DATASET_OWNER")
  if [[ "$SKIP_REGISTERED" == 1 ]]; then
    cmd+=(--skip-geonode-registered)
  fi
  if "${cmd[@]}"; then
    ((ok+=1))
  else
    ((failed+=1))
    failed_layers+=("$layer")
    echo "ERROR: $layer failed" >&2
    if [[ "$STOP_ON_ERROR" == 1 ]]; then break; fi
  fi
done
printf '\nCompleted: commands successful=%d, failed=%d (total configured=%d)\n' "$ok" "$failed" "$count"
# Apply permissions to all configured datasets, including previously registered ones.
# No user-supplied Python is evaluated; layer names are transferred as JSON.
export MEDSIS_LAYER_NAMES="$(printf '%s\n' "${LAYERS[@]}")"
export MEDSIS_WORKSPACE="$GEOSERVER_WORKSPACE"
export MEDSIS_OWNER="$DATASET_OWNER"
export MEDSIS_MANAGERS_GROUP="$MANAGERS_GROUP"

permission_code=$(cat <<'PYCODE'
import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from geonode.layers.models import Dataset

names = [n for n in os.environ['MEDSIS_LAYER_NAMES'].splitlines() if n]
workspace = os.environ['MEDSIS_WORKSPACE']
owner_name = os.environ['MEDSIS_OWNER']
managers = os.environ['MEDSIS_MANAGERS_GROUP']

if not Group.objects.filter(name=managers).exists():
    raise RuntimeError(f'Missing GeoNode group: {group_name}')

owner = get_user_model().objects.get(username=owner_name)
owner_perms = [
    'view_resourcebase', 'download_resourcebase',
    'change_resourcebase', 'delete_resourcebase',
    'change_resourcebase_permissions', 'change_resourcebase_metadata',
    'publish_resourcebase',
]
read_perms = ['view_resourcebase', 'download_resourcebase']

success = 0
missing = []
errors = []
for name in names:
    # GeoNode Dataset.name is normally workspace:layer.
    qualified_name = f'{workspace}:{name}'
    matches = list(Dataset.objects.filter(name=qualified_name))
    if not matches:
        # Some GeoNode installations store an unqualified Dataset.name.
        # Accept it only if typename explicitly identifies the workspace.
        matches = [d for d in Dataset.objects.filter(name=name)
                   if getattr(d, 'typename', None) == qualified_name]
    if not matches:
        missing.append(qualified_name)
        print(f'MISSING: {qualified_name}')
        continue
    if len(matches) != 1:
        errors.append(qualified_name)
        print(f'AMBIGUOUS: {qualified_name}')
        continue
    dataset = matches[0]
    try:
        perm_spec = {
          "users": {
              owner.username: [
                  "view_resourcebase",
                  "download_resourcebase",
                  "change_resourcebase",
                  "delete_resourcebase",
                  "change_resourcebase_permissions",
                  "change_resourcebase_metadata",
                  "publish_resourcebase",
              ]
          },
          "groups": {
              "data-managers": [
                  "view_resourcebase",
                  "download_resourcebase",
                  "change_resourcebase",
                  "delete_resourcebase",
                  "change_resourcebase_permissions",
                  "change_resourcebase_metadata",
                  "publish_resourcebase",
              ]
          }
        }
        result = dataset.set_permissions(perm_spec)
        if result is not True:
            raise RuntimeError(f'set_permissions returned {result!r}')
        dataset.refresh_from_db()
        actual = dataset.get_all_level_info()
        groups = {g.name: set(perms) for g, perms in actual['groups'].items()}
        if not set(owner_perms).issubset(groups.get(managers, set())):
            raise RuntimeError('data-managers permissions not confirmed')
        success += 1
        print(f'OK permissions: {qualified_name} (PK {dataset.pk})')
    except Exception as exc:
        errors.append(qualified_name)
        print(f'ERROR permissions: {qualified_name}: {exc}')

print(f'Permissions: OK={success}, missing={len(missing)}, errors={len(errors)}')
if missing or errors:
    raise SystemExit(1)
PYCODE
)

echo 'Applying permissions to data-managers...'
if ! "$PYTHON" "$MANAGE_PY" shell -c "$permission_code"; then
  echo 'ERROR: permission configuration incomplete.' >&2
  exit 1
fi
if (( failed > 0 )); then
  printf 'Import commands failed for: %s\n' "${failed_layers[*]}" >&2
  exit 1
fi
echo 'Done. Verify anonymous and authenticated HTTP access before production use.' 

