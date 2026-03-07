#!/bin/bash
# ===========================================================================
# restore_on_test.sh — Restore to isolated test environment
#
# Project name "s4m_catalogue_test" ensures complete isolation from
# production: containers, volumes and network have distinct names.
# ===========================================================================
set -euo pipefail
export COMPOSE_PROJECT_NAME="s4m_catalogue_test"
source "$(dirname "$0")/lib_common.sh"

# Restore test override if missing
if [ ! -f "docker-compose.override.yml" ] && [ -f "docker-compose.override.yml.backup" ]; then
    echo "Restoring docker-compose.override.yml from .backup..."
    mv docker-compose.override.yml.backup docker-compose.override.yml
fi

COMPOSE="docker-compose \
    -f docker-compose.yml \
    -f docker-compose.override.yml \
    -p ${COMPOSE_PROJECT_NAME}"

# --- Production containers that may conflict ---
PROD_NGINX_CONTAINER="nginx4s4m_catalogue"
PROD_GEOSERVER_CONTAINER="geoserver4s4m_catalogue"

# --- Test containers ---
DJANGO_CONTAINER="django4${COMPOSE_PROJECT_NAME}"
DB_CONTAINER="db4${COMPOSE_PROJECT_NAME}"
GEOSERVER_CONTAINER="geoserver4${COMPOSE_PROJECT_NAME}"

# --- Configuration ---
CONFIG_FILE_PATH="/usr/src/s4m_catalogue/s4m_catalogue/br/settings_docker.ini"
PG_SUPERUSER="postgres"
BACKUP_SEARCH_DIR="${BACKUP_SEARCH_DIR:-./backups}"

# Test database and owner
get_test_db_owner() {
    case "$1" in
        "test_my_geo")      echo "my_geo" ;;
        "test_my_geo_data") echo "my_geo_data" ;;
        "test_backoffice")  echo "backoffice_user" ;;
        *) echo "" ;;
    esac
}

# DB map for substitution in datastore.xml
DS_DB_MAP="my_geo_data:test_my_geo_data my_geo:test_my_geo backoffice:test_backoffice"

# Production → test URLs
PROD_GEOSERVER_URL="http://localhost/geoserver/"
PROD_GEONODE_URL="http://localhost/"
PROD_GEONODE_URL_NOSLASH="http://localhost"
TEST_GEOSERVER_URL="http://localhost:8081/geoserver/"
TEST_GEONODE_URL="http://localhost:8081/"
TEST_GEONODE_URL_NOSLASH="http://localhost:8081"

# ---------------------------------------------------------------------------
# fix_geoserver_urls_in_db
#   Aligns all URLs in the DB from production to test
# ---------------------------------------------------------------------------
fix_geoserver_urls_in_db() {
    echo "🔧 Aligning GeoServer/GeoNode URLs in test DB..."
    local db="test_my_geo"

    # Helper for safe UPDATE (ignore error if table does not exist)
    safe_update() {
        docker exec "$DB_CONTAINER" psql -U "$PG_SUPERUSER" -d "$db" \
            -v ON_ERROR_STOP=1 -c "$1" 2>/dev/null || true
    }

    safe_update "
        UPDATE base_resourcebase
        SET thumbnail_url = REPLACE(thumbnail_url,
            '${PROD_GEOSERVER_URL}', '${TEST_GEOSERVER_URL}')
        WHERE thumbnail_url LIKE '%localhost/geoserver/%';
    "
    safe_update "
        UPDATE base_link
        SET url = REPLACE(url,
            '${PROD_GEOSERVER_URL}', '${TEST_GEOSERVER_URL}')
        WHERE url LIKE '%localhost/geoserver/%';
    "
    safe_update "
        UPDATE base_link
        SET url = REPLACE(url, '${PROD_GEONODE_URL}', '${TEST_GEONODE_URL}')
        WHERE url LIKE 'http://localhost/%' AND url NOT LIKE 'http://localhost:8081/%';
    "
    safe_update "
        UPDATE base_link
        SET url = REPLACE(url, '${PROD_GEONODE_URL_NOSLASH}', '${TEST_GEONODE_URL_NOSLASH}')
        WHERE url = '${PROD_GEONODE_URL_NOSLASH}' OR url LIKE '${PROD_GEONODE_URL_NOSLASH}/%';
    "
    safe_update "
        UPDATE services_service
        SET base_url = REPLACE(base_url,
            '${PROD_GEOSERVER_URL}', '${TEST_GEOSERVER_URL}')
        WHERE base_url LIKE '%localhost/geoserver/%';
    "
    safe_update "
        UPDATE base_sitepreferences
        SET siteurl = '${TEST_GEONODE_URL}'
        WHERE siteurl LIKE 'http://localhost/%' AND siteurl NOT LIKE 'http://localhost:8081/%';
    "

    # Check for remaining production URLs
    local remaining
    remaining=$(docker exec "$DB_CONTAINER" psql -U "$PG_SUPERUSER" -d "$db" -t -A -c "
        SELECT COUNT(*) FROM base_link
        WHERE url LIKE 'http://localhost/%' AND url NOT LIKE 'http://localhost:8081/%';
    " 2>/dev/null | tr -d ' ' || echo "0")

    if [ "${remaining:-0}" != "0" ]; then
        log_warn "${remaining} records in base_link still have production URLs."
    else
        log_ok "GeoServer/GeoNode URLs updated in database."
    fi
}

# ---------------------------------------------------------------------------
# restore_geoserver_catalog_files
#   Extracts geoserver_catalog.zip and updates URLs for test environment
# ---------------------------------------------------------------------------
restore_geoserver_catalog_files() {
    local backup_zip="$1"
    local test_gs_dir="./geoserver_data_dir_test"

    echo "Restoring GeoServer files from catalog..."
    rm -rf "$test_gs_dir"
    mkdir -p "$test_gs_dir"

    local tmp_dir="/tmp/geoserver_catalog_zip_$$"
    rm -rf "$tmp_dir" && mkdir -p "$tmp_dir"
    unzip -o "$backup_zip" "geoserver_catalog.zip" -d "$tmp_dir" > /dev/null 2>&1

    if [ ! -f "$tmp_dir/geoserver_catalog.zip" ]; then
        log_warn "'geoserver_catalog.zip' not found in backup."
        rm -rf "$tmp_dir"
        return 1
    fi

    unzip -o "$tmp_dir/geoserver_catalog.zip" -d "$test_gs_dir" > /dev/null
    log_ok "GeoServer files restored to '$test_gs_dir'."
    rm -rf "$tmp_dir"

    # Align proxyBaseUrl
    local gs_url_test="http://localhost:8081/geoserver"
    local gn_url_test="http://localhost:8081"

    echo "   🔧 Aligning proxyBaseUrl and OAuth2..."
    for xml_file in "${test_gs_dir}/global.xml" "${test_gs_dir}/settings.xml"; do
        [ ! -f "$xml_file" ] && continue
        if sed --version >/dev/null 2>&1; then
            sed -i "s|<proxyBaseUrl>http://localhost/geoserver</proxyBaseUrl>|<proxyBaseUrl>${gs_url_test}</proxyBaseUrl>|" "$xml_file" || true
        else
            sed -i '' "s|<proxyBaseUrl>http://localhost/geoserver</proxyBaseUrl>|<proxyBaseUrl>${gs_url_test}</proxyBaseUrl>|" "$xml_file" || true
        fi
    done

    local oauth_cfg="${test_gs_dir}/security/filter/geonode-oauth2/config.xml"
    if [ -f "$oauth_cfg" ]; then
        local sed_inplace
        sed --version >/dev/null 2>&1 && sed_inplace="sed -i" || sed_inplace="sed -i ''"
        $sed_inplace "s|http://localhost/o/authorize/|${gn_url_test}/o/authorize/|g" "$oauth_cfg" || true
        $sed_inplace "s|http://localhost/geoserver/index.html|${gs_url_test}/geoserver/index.html|g" "$oauth_cfg" || true
        $sed_inplace "s|http://localhost/account/logout/|${gn_url_test}/account/logout/|g" "$oauth_cfg" || true
        log_ok "OAuth2 endpoints aligned."
    fi
}

# ===========================================================================
# BACKUP FILE AUTO-DISCOVERY
# ===========================================================================
if [ "$#" -eq 2 ]; then
    GEONODE_BACKUP_ZIP="$1"
    BACKOFFICE_BACKUP_DUMP="$2"
    BACKUP_BASE_DIR="$(dirname "$1")"
    DATASTORES_ARCHIVE=$(find_latest_file "$BACKUP_BASE_DIR" "geoserver-datastores-*.tar.gz")
    GEODATA_DUMP=$(find_latest_file "$BACKUP_BASE_DIR" "backup-geodata-*.dump")
elif [ "$#" -eq 0 ]; then
    log_info "No files specified — searching for latest backups in '${BACKUP_SEARCH_DIR}'..."
    GEONODE_BACKUP_ZIP=$(find_latest_file "$BACKUP_SEARCH_DIR" "*.zip")
    BACKOFFICE_BACKUP_DUMP=$(find_latest_file "$BACKUP_SEARCH_DIR" "backup-backoffice-*.dump")
    DATASTORES_ARCHIVE=$(find_latest_file "$BACKUP_SEARCH_DIR" "geoserver-datastores-*.tar.gz")
    GEODATA_DUMP=$(find_latest_file "$BACKUP_SEARCH_DIR" "backup-geodata-*.dump")
    [ -z "$GEONODE_BACKUP_ZIP" ]     && { log_err "No .zip found in '${BACKUP_SEARCH_DIR}'."; exit 1; }
    [ -z "$BACKOFFICE_BACKUP_DUMP" ] && { log_err "No backoffice .dump found in '${BACKUP_SEARCH_DIR}'."; exit 1; }
    echo "   📦 GeoNode backup   : $GEONODE_BACKUP_ZIP"
    echo "   📦 Backoffice dump  : $BACKOFFICE_BACKUP_DUMP"
    [ -n "${DATASTORES_ARCHIVE:-}" ]  && echo "   📦 GS datastores    : $DATASTORES_ARCHIVE"
    [ -n "${GEODATA_DUMP:-}" ]        && echo "   📦 Geodata dump     : $GEODATA_DUMP"
else
    log_err "Provide zero or two arguments."
    echo "   Usage: $0 [/path/geonode-backup.zip /path/backup-backoffice.dump]"
    exit 1
fi

[ ! -f "$GEONODE_BACKUP_ZIP" ]     && { log_err "File not found: $GEONODE_BACKUP_ZIP"; exit 1; }
[ ! -f "$BACKOFFICE_BACKUP_DUMP" ] && { log_err "File not found: $BACKOFFICE_BACKUP_DUMP"; exit 1; }

echo ""
echo "=================================================================="
echo "  TEST ENVIRONMENT: ${COMPOSE_PROJECT_NAME}"
echo "  (production 's4m_catalogue' is NOT touched)"
echo "=================================================================="
echo ""

echo "🛑 Stopping production containers on same ports..."
docker stop "$PROD_NGINX_CONTAINER" "$PROD_GEOSERVER_CONTAINER" >/dev/null 2>&1 || true

# ===========================================================================
# PHASE 1 — Shutdown test stack
# ===========================================================================
echo "🛑 1/4: Stopping existing test environment..."
$COMPOSE down --remove-orphans || { log_err "Error stopping test containers."; exit 1; }

# ===========================================================================
# PHASE 2 — DB preparation and data restore
# ===========================================================================
echo "🛠️ 2/4: Preparing and restoring data..."
$COMPOSE up -d db
wait_for_db "$DB_CONTAINER" "$PG_SUPERUSER"
sleep 5

# Create/validate application DB roles
echo "Verifying/creating application DB roles..."
for attempt in 1 2 3 4 5; do
    docker exec "$DB_CONTAINER" psql -U "$PG_SUPERUSER" -v ON_ERROR_STOP=1 -d postgres -c "
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'my_geo') THEN
        CREATE ROLE my_geo LOGIN PASSWORD 'my_geo';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'my_geo_data') THEN
        CREATE ROLE my_geo_data LOGIN PASSWORD 'my_geo_data';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'backoffice_user') THEN
        CREATE ROLE backoffice_user LOGIN PASSWORD 'backoffice_pwd';
    END IF;
END
\$\$;
" 2>/dev/null && break
    echo "  DB not ready — retry $attempt/5 in 5 seconds..."
    sleep 5
done

# Prepare test databases
for db_name in test_my_geo test_my_geo_data test_backoffice; do
    prepare_db "$DB_CONTAINER" "$db_name" "$(get_test_db_owner "$db_name")" "$PG_SUPERUSER"
done

echo "Starting Django..."
$COMPOSE up -d django || { log_err "Error starting Django."; exit 1; }

# Restore backoffice
echo "Restoring 'test_backoffice'..."
restore_pg_dump "$DB_CONTAINER" "$BACKOFFICE_BACKUP_DUMP" "test_backoffice" "$PG_SUPERUSER"
grant_db_permissions "$DB_CONTAINER" "test_backoffice" "$(get_test_db_owner "test_backoffice")" "$PG_SUPERUSER"

# Restore geodata
if [ -n "${GEODATA_DUMP:-}" ] && [ -f "${GEODATA_DUMP:-}" ]; then
    echo "Restoring 'test_my_geo_data' (geodatabase)..."
    restore_pg_dump "$DB_CONTAINER" "$GEODATA_DUMP" "test_my_geo_data" "$PG_SUPERUSER"
    grant_db_permissions "$DB_CONTAINER" "test_my_geo_data" "$(get_test_db_owner "test_my_geo_data")" "$PG_SUPERUSER"
else
    log_warn "No geodata dump — shapefile layers will not be restored."
fi

# Restore GeoServer files from catalog
restore_geoserver_catalog_files "$GEONODE_BACKUP_ZIP"

# GeoNode migration
echo "Running GeoNode migration..."
$COMPOSE run --rm --no-deps --entrypoint "" django python manage.py migrate --noinput \
    || { log_err "Migration error."; exit 1; }
grant_db_permissions "$DB_CONTAINER" "test_my_geo" "$(get_test_db_owner "test_my_geo")" "$PG_SUPERUSER"
grant_db_permissions "$DB_CONTAINER" "test_my_geo_data" "$(get_test_db_owner "test_my_geo_data")" "$PG_SUPERUSER"

# Start GeoServer
echo "Starting GeoServer and dependencies..."
$COMPOSE up -d geoserver
wait_for_geoserver "$GEOSERVER_CONTAINER" || exit 1

# Datastore injection (before restore)
inject_geoserver_datastores "$GEOSERVER_CONTAINER" "${DATASTORES_ARCHIVE:-}" "$DS_DB_MAP"

# manage.py restore
apply_manage_restore "$COMPOSE" "$DJANGO_CONTAINER" "$GEONODE_BACKUP_ZIP" "$CONFIG_FILE_PATH"
MANAGE_RESTORE_EXIT=$?

if [ $MANAGE_RESTORE_EXIT -ne 0 ]; then
    log_warn "manage.py restore exit $MANAGE_RESTORE_EXIT — fixing fixtures..."
    grant_db_permissions "$DB_CONTAINER" "test_my_geo" "$(get_test_db_owner "test_my_geo")" "$PG_SUPERUSER"
    grant_db_permissions "$DB_CONTAINER" "test_my_geo_data" "$(get_test_db_owner "test_my_geo_data")" "$PG_SUPERUSER"
    fix_fixture_fk_violations "$DB_CONTAINER" "test_my_geo" "$PG_SUPERUSER"
    $COMPOSE run --rm --no-deps --entrypoint "" django \
        python manage.py loaddata --ignorenonexistent \
        /usr/src/venv/lib/python3.12/site-packages/geonode/base/fixtures/initial_data.json \
        2>/dev/null || true
    $COMPOSE run --rm --no-deps --entrypoint "" django \
        python manage.py migrate --noinput 2>/dev/null || true
    log_ok "Restore completed with fixture correction."
fi

# Post-restore permissions
grant_db_permissions "$DB_CONTAINER" "test_my_geo" "$(get_test_db_owner "test_my_geo")" "$PG_SUPERUSER"
grant_db_permissions "$DB_CONTAINER" "test_my_geo_data" "$(get_test_db_owner "test_my_geo_data")" "$PG_SUPERUSER"

# URL alignment in DB
fix_geoserver_urls_in_db

# migrate_baseurl
echo "Running migrate_baseurl (prod → test)..."
$COMPOSE run --rm --no-deps --entrypoint "" django python manage.py migrate_baseurl \
    -f --source-address="${PROD_GEONODE_URL}" --target-address="${TEST_GEONODE_URL}" \
    2>/dev/null || log_warn "migrate_baseurl not available or already updated."

# Re-inject datastores post-restore (manage.py restore may have overwritten them)
inject_geoserver_datastores "$GEOSERVER_CONTAINER" "${DATASTORES_ARCHIVE:-}" "$DS_DB_MAP"

# ===========================================================================
# PHASE 3 — Full test environment startup
# ===========================================================================
echo "🚀 3/4: Starting test environment..."
$COMPOSE up -d db django geoserver geonode \
    || { log_err "Error starting final environment."; exit 1; }

echo "Waiting for Django to be healthy (max ~5 min)..."
DJANGO_HEALTHY=0
for i in $(seq 1 60); do
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' "$DJANGO_CONTAINER" 2>/dev/null)
    [ "$STATUS" = "healthy" ] && { DJANGO_HEALTHY=1; break; }
    sleep 5
done
[ "$DJANGO_HEALTHY" -ne 1 ] \
    && log_warn "Django did not reach 'healthy'. Check: docker logs $DJANGO_CONTAINER" \
    || log_ok "Django healthy."

# GeoServer styles fix (after full startup: cleanup + reload + REST registration + layer fix)
fix_geoserver_styles_after_startup "$GEOSERVER_CONTAINER"

# ===========================================================================
# PHASE 4 — Final verification
# ===========================================================================
echo ""
$COMPOSE ps
echo ""
echo "=================================================================="
echo "  ✅ TEST ENVIRONMENT READY: ${COMPOSE_PROJECT_NAME}"
echo "  GeoNode backup used: $GEONODE_BACKUP_ZIP"
echo "  Backoffice backup used: $BACKOFFICE_BACKUP_DUMP"
[ -n "${DATASTORES_ARCHIVE:-}" ] \
    && echo "  GS Datastores used: $DATASTORES_ARCHIVE" \
    || echo "  GS Datastores: ⚠️  not found"
echo "=================================================================="
echo ""
echo "  Check application at: ➡️  http://localhost:8081"
echo "  Production still running at: ➡️  http://localhost (unchanged)"
echo ""
echo "  When done, run: ./cleanup_test.sh"
