#!/bin/bash
# ===========================================================================
# restore_on_production.sh — Full restore to production environment
# ===========================================================================
set -euo pipefail
source "$(dirname "$0")/lib_common.sh"

# --- Configuration ---
COMPOSE_PROJECT_NAME="s4m_catalogue"
DJANGO_CONTAINER="django4${COMPOSE_PROJECT_NAME}"
DB_CONTAINER="db4${COMPOSE_PROJECT_NAME}"
GEOSERVER_CONTAINER="geoserver4${COMPOSE_PROJECT_NAME}"
CONFIG_FILE_PATH="/usr/src/s4m_catalogue/s4m_catalogue/br/settings_docker.ini"
PG_SUPERUSER="postgres"
BACKUP_SEARCH_DIR="./backups"
COMPOSE="docker-compose"

# Production database and owner
get_prod_db_owner() {
    case "$1" in
        "my_geo")      echo "my_geo" ;;
        "my_geo_data") echo "my_geo_data" ;;
        "backoffice")  echo "backoffice_user" ;;
        *) echo "" ;;
    esac
}

# ===========================================================================
# Backup file auto-discovery
# ===========================================================================
if [ "$#" -eq 2 ]; then
    GEONODE_BACKUP_ZIP="$1"
    BACKOFFICE_BACKUP_DUMP="$2"
    BACKUP_BASE_DIR="$(dirname "$1")"
    GEODATA_DUMP=$(find_latest_file "$BACKUP_BASE_DIR" "backup-geodata-*.dump")
    DATASTORES_ARCHIVE=$(find_latest_file "$BACKUP_BASE_DIR" "geoserver-datastores-*.tar.gz")
elif [ "$#" -eq 0 ]; then
    log_info "No files specified — searching for latest backups in '${BACKUP_SEARCH_DIR}'..."
    GEONODE_BACKUP_ZIP=$(find_latest_file "$BACKUP_SEARCH_DIR" "*.zip")
    BACKOFFICE_BACKUP_DUMP=$(find_latest_file "$BACKUP_SEARCH_DIR" "backup-backoffice-*.dump")
    GEODATA_DUMP=$(find_latest_file "$BACKUP_SEARCH_DIR" "backup-geodata-*.dump")
    DATASTORES_ARCHIVE=$(find_latest_file "$BACKUP_SEARCH_DIR" "geoserver-datastores-*.tar.gz")
    [ -z "$GEONODE_BACKUP_ZIP" ]     && { log_err "No .zip found in '${BACKUP_SEARCH_DIR}'."; exit 1; }
    [ -z "$BACKOFFICE_BACKUP_DUMP" ] && { log_err "No backoffice .dump found in '${BACKUP_SEARCH_DIR}'."; exit 1; }
    echo "   📦 GeoNode backup   : $GEONODE_BACKUP_ZIP"
    echo "   📦 Backoffice dump  : $BACKOFFICE_BACKUP_DUMP"
    [ -n "$GEODATA_DUMP" ]        && echo "   📦 Geodata dump     : $GEODATA_DUMP"
    [ -n "$DATASTORES_ARCHIVE" ]  && echo "   📦 GS datastores    : $DATASTORES_ARCHIVE"
else
    log_err "Provide zero or two arguments."
    echo "   Usage: $0 [/path/geonode-backup.zip /path/backup-backoffice.dump]"
    exit 1
fi

[ ! -f "$GEONODE_BACKUP_ZIP" ]     && { log_err "File not found: $GEONODE_BACKUP_ZIP"; exit 1; }
[ ! -f "$BACKOFFICE_BACKUP_DUMP" ] && { log_err "File not found: $BACKOFFICE_BACKUP_DUMP"; exit 1; }

echo ""
echo "--- STARTING PRODUCTION RESTORE ---"
echo ""

# ===========================================================================
# PHASE 1 — Partial shutdown (DB stays up)
# ===========================================================================
echo "🛑 1/5: Stopping application services..."
$COMPOSE stop django geonode celery geoserver data-dir-conf

# ===========================================================================
# PHASE 2 — Production DB preparation
# ===========================================================================
echo "🛠️ 2/5: Preparing production database..."
$COMPOSE up -d db
wait_for_db "$DB_CONTAINER" "$PG_SUPERUSER"

for db_name in my_geo my_geo_data backoffice; do
    prepare_db "$DB_CONTAINER" "$db_name" "$(get_prod_db_owner "$db_name")" "$PG_SUPERUSER"
done

# ===========================================================================
# PHASE 3 — Database restore
# ===========================================================================
echo "💾 3/5: Restoring databases..."

# 3a: backoffice
echo "   Restoring 'backoffice'..."
restore_pg_dump "$DB_CONTAINER" "$BACKOFFICE_BACKUP_DUMP" "backoffice" "$PG_SUPERUSER"
grant_db_permissions "$DB_CONTAINER" "backoffice" "$(get_prod_db_owner "backoffice")" "$PG_SUPERUSER"

# 3b: geodata (shapefile tables)
if [ -n "${GEODATA_DUMP:-}" ] && [ -f "${GEODATA_DUMP:-}" ]; then
    echo "   Restoring 'my_geo_data' (geodatabase)..."
    restore_pg_dump "$DB_CONTAINER" "$GEODATA_DUMP" "my_geo_data" "$PG_SUPERUSER"
    grant_db_permissions "$DB_CONTAINER" "my_geo_data" "$(get_prod_db_owner "my_geo_data")" "$PG_SUPERUSER"
else
    log_warn "No geodata dump — shapefile layers will not be restored."
fi

# ===========================================================================
# PHASE 4 — Migration + GeoNode restore
# ===========================================================================
echo "📦 4/5: Migration and GeoNode restore..."

echo "Running migrations on 'my_geo'..."
$COMPOSE run --rm --entrypoint "" django python manage.py migrate --noinput \
    || { log_err "GeoNode migration error."; exit 1; }
grant_db_permissions "$DB_CONTAINER" "my_geo" "$(get_prod_db_owner "my_geo")" "$PG_SUPERUSER"
grant_db_permissions "$DB_CONTAINER" "my_geo_data" "$(get_prod_db_owner "my_geo_data")" "$PG_SUPERUSER"

echo "Starting GeoServer..."
$COMPOSE up -d geoserver
wait_for_geoserver "$GEOSERVER_CONTAINER" || exit 1

echo "Running manage.py restore..."
apply_manage_restore "$COMPOSE" "$DJANGO_CONTAINER" "$GEONODE_BACKUP_ZIP" "$CONFIG_FILE_PATH"
if [ $? -ne 0 ]; then
    log_warn "manage.py restore reported errors — attempting fixture correction..."
    grant_db_permissions "$DB_CONTAINER" "my_geo" "$(get_prod_db_owner "my_geo")" "$PG_SUPERUSER"
    fix_fixture_fk_violations "$DB_CONTAINER" "my_geo" "$PG_SUPERUSER"
fi

# Datastore injection (no name substitution: production)
inject_geoserver_datastores "$GEOSERVER_CONTAINER" "${DATASTORES_ARCHIVE:-}" ""

# ===========================================================================
# PHASE 5 — Full restart + styles fix
# ===========================================================================
echo "🚀 5/5: Full stack restart..."
$COMPOSE up -d || { log_err "Error starting services."; exit 1; }

# GeoServer styles fix (after startup: cleanup + reload + REST registration + layer fix)
fix_geoserver_styles_after_startup "$GEOSERVER_CONTAINER"

echo ""
echo "--- ✅ PRODUCTION RESTORE COMPLETED ---"
echo "Check application at: ${SITEURL:-http://localhost}"
