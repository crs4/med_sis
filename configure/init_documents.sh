#!/usr/bin/env bash
set -Eeuo pipefail

# Run inside the Django container, from the directory containing manage.py.
# All paths below must be visible INSIDE that container.
PYTHON_BIN="${PYTHON_BIN:-python}"
MANAGE_PY="${MANAGE_PY:-manage.py}"
DOCUMENT_OWNER="${DOCUMENT_OWNER:-admin}"
DOCUMENT_GROUP="${DOCUMENT_GROUP:-registered-members}"

# Format: "path|title". Replace with your eight real files/titles.
DOCUMENTS=(
  "manuals/MED-SIS-Manual-Generic_User.pdf|MED-SIS Manual for Generic User"
  "manuals/MED-SIS-Manual-Administrators.pdf|MED-SIS Manual for Administrators"
  "manuals/MED-SIS-Manual-Data_Managers.pdf|MED-SIS Manual for Data Managers"
  "manuals/MED-SIS-Manual-ISO_28258|MED-SIS Manual Interoperability and ISO 28258"
  "manuals/MED-SIS-Manual-Point_Soil_Data_Template_Guidelines.pdf|MED-SIS Point Soil Data XLSx Template Guidelines"
  "manuals/MED-SIS-Manual-Point_Soil_Data.pdf|MED-SIS Manual - Point Soil Data Descriptors"
  "manuals/MED-SIS-Manual-Soil_Indicators.pdf|MED-SIS Manual - Health Soil Indicator Descriptors"
  "manuals/MED-SIS-Manual-Taxonomies.pdf|MED-SIS Manual - Taxonomies"
)

if [[ ! -f "$MANAGE_PY" ]]; then
  echo "ERROR: manage.py not found: $MANAGE_PY" >&2
  exit 2
fi

# Validate all files before changing anything.
for entry in "${DOCUMENTS[@]}"; do
  path="${entry%%|*}"
  title="${entry#*|}"
  if [[ "$entry" != *'|'* || -z "$path" || -z "$title" ]]; then
    echo "ERROR: invalid document entry: $entry" >&2
    exit 2
  fi
  if [[ ! -f "$path" ]]; then
    echo "ERROR: missing document inside Django container: $path" >&2
    exit 2
  fi
done

failures=0
for entry in "${DOCUMENTS[@]}"; do
  path="${entry%%|*}"
  title="${entry#*|}"
  printf '\n==> Import/permissions: %s\n' "$title"
  if ! "$PYTHON_BIN" "$MANAGE_PY" import_manuals \
      --file "$path" \
      --title "$title" \
      --owner "admin" \
      --group "registered_user" \
      --skip-existing; then
    echo "FAILED: $title" >&2
    failures=$((failures + 1))
  fi
done

if (( failures > 0 )); then
  echo "Completed with $failures failure(s)." >&2
  exit 1
fi
echo 'All documents processed successfully.'
