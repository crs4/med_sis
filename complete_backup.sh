#!/bin/bash
# ===========================================================================
# complete_backup.sh — Full GeoNode + GeoServer + DB backup
# ===========================================================================
set -euo pipefail
source "$(dirname "$0")/lib_common.sh"

# --- Configuration ---
COMPOSE_PROJECT_NAME="s4m_catalogue"
DJANGO_CONTAINER="django4${COMPOSE_PROJECT_NAME}"
DB_CONTAINER="db4${COMPOSE_PROJECT_NAME}"
GEOSERVER_CONTAINER="geoserver4${COMPOSE_PROJECT_NAME}"
CONFIG_FILE_PATH="/usr/src/s4m_catalogue/s4m_catalogue/br/settings_docker.ini"
PG_USER="postgres"
BACKUP_DIR="$(pwd)/backups"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

mkdir -p "$BACKUP_DIR"
chmod 777 "$BACKUP_DIR"

echo "🔄 Preventive container restart for clean state..."
docker-compose restart django geoserver
echo "Waiting 15 seconds for stabilization..."
sleep 15

echo "--- STARTING FULL BACKUP ---"

# --- 1/4: GeoNode + GeoServer official backup ---
echo "📦 1/4: Official GeoNode backup..."
docker exec -t "$DJANGO_CONTAINER" python manage.py backup \
    --verbosity 3 \
    --force \
    --backup-dir=/backup_restore \
    --skip-read-only \
    --config="$CONFIG_FILE_PATH"

LATEST_GEONODE_BACKUP=$(docker exec "$DJANGO_CONTAINER" bash -c "ls -t /backup_restore/*.zip | head -n 1")
[ -z "$LATEST_GEONODE_BACKUP" ] && { log_err "No GeoNode backup found in /backup_restore."; exit 1; }

GEONODE_BACKUP_FILENAME=$(basename "$LATEST_GEONODE_BACKUP")
docker cp "${DJANGO_CONTAINER}:${LATEST_GEONODE_BACKUP}" "${BACKUP_DIR}/${GEONODE_BACKUP_FILENAME}"
log_ok "GeoNode backup: ${BACKUP_DIR}/${GEONODE_BACKUP_FILENAME}"

# --- 2/4: GeoServer datastore.xml backup ---
echo "📦 2/4: GeoServer datastore.xml backup..."
DATASTORES_FILENAME="${BACKUP_DIR}/geoserver-datastores-${TIMESTAMP}.tar.gz"

DATASTORE_FILES=$(docker exec "$GEOSERVER_CONTAINER" \
    find /geoserver_data/data/workspaces -name "datastore.xml" 2>/dev/null)

if [ -z "$DATASTORE_FILES" ]; then
    log_warn "No datastore.xml found in GeoServer."
    DATASTORES_FILENAME=""
else
    docker exec "$GEOSERVER_CONTAINER" \
        tar -czf /tmp/geoserver_datastores.tar.gz \
        -C /geoserver_data/data \
        $(echo "$DATASTORE_FILES" | sed 's|/geoserver_data/data/||g' | tr '\n' ' ') \
        2>/dev/null
    docker cp "${GEOSERVER_CONTAINER}:/tmp/geoserver_datastores.tar.gz" "$DATASTORES_FILENAME"
    docker exec "$GEOSERVER_CONTAINER" rm -f /tmp/geoserver_datastores.tar.gz 2>/dev/null || true

    if [ -f "$DATASTORES_FILENAME" ]; then
        DATASTORE_COUNT=$(echo "$DATASTORE_FILES" | wc -l | tr -d ' ')
        log_ok "$DATASTORE_COUNT datastore.xml saved to: $DATASTORES_FILENAME"
    else
        log_warn "Error backing up datastores. Fallback: copying workspaces."
        WORKSPACES_BACKUP="${BACKUP_DIR}/geoserver-workspaces-${TIMESTAMP}"
        mkdir -p "$WORKSPACES_BACKUP"
        docker cp "${GEOSERVER_CONTAINER}:/geoserver_data/data/workspaces/." "$WORKSPACES_BACKUP/"
        DATASTORES_FILENAME=""
    fi
fi

# --- 3/4: my_geo_data geodatabase backup ---
echo "📦 3/4: Backing up 'my_geo_data' geodatabase..."
GEODATA_FILENAME="${BACKUP_DIR}/backup-geodata-${TIMESTAMP}.dump"
docker exec "$DB_CONTAINER" bash -lc "pg_dump -U '$PG_USER' -d 'my_geo_data' -F c -f /tmp/geodata.dump" \
    || { log_err "pg_dump error for my_geo_data."; exit 1; }
docker cp "${DB_CONTAINER}:/tmp/geodata.dump" "$GEODATA_FILENAME" \
    || { log_err "Error copying geodata dump."; exit 1; }
docker exec "$DB_CONTAINER" rm -f /tmp/geodata.dump >/dev/null 2>&1 || true
log_ok "Geodata dump: ${GEODATA_FILENAME}"

# --- 4/4: backoffice database backup ---
echo "📦 4/4: Backing up 'backoffice' database..."
BACKOFFICE_FILENAME="${BACKUP_DIR}/backup-backoffice-${TIMESTAMP}.dump"
docker exec "$DB_CONTAINER" bash -lc "pg_dump -U '$PG_USER' -d 'backoffice' -F c -f /tmp/backoffice.dump" \
    || { log_err "pg_dump error for backoffice."; exit 1; }
docker cp "${DB_CONTAINER}:/tmp/backoffice.dump" "$BACKOFFICE_FILENAME" \
    || { log_err "Error copying backoffice dump."; exit 1; }
docker exec "$DB_CONTAINER" rm -f /tmp/backoffice.dump >/dev/null 2>&1 || true
log_ok "Backoffice dump: ${BACKOFFICE_FILENAME}"

# --- Summary ---
echo ""
echo "--- 🎉 BACKUP COMPLETED ---"
echo ""
echo "Output files in '${BACKUP_DIR}':"
echo "  📦 GeoNode backup  : ${BACKUP_DIR}/${GEONODE_BACKUP_FILENAME}"
[ -n "$DATASTORES_FILENAME" ] && echo "  📦 GS datastores   : ${DATASTORES_FILENAME}"
echo "  📦 Geodata dump    : ${GEODATA_FILENAME}"
echo "  📦 Backoffice dump : ${BACKOFFICE_FILENAME}"
echo ""
echo "To run restore in test environment:"
echo "  ./restore_on_test.sh"
echo ""
echo "To run restore in production:"
echo "  ./restore_on_production.sh"
