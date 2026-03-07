#!/bin/bash

echo "--- STARTING TEST ENVIRONMENT CLEANUP PROCEDURE ---"

# --- Configuration ---
TEST_PROJECT_NAME="s4m_catalogue_test"
PROD_PROJECT_NAME="s4m_catalogue"
TEST_GEOSERVER_DATA_DIR="./geoserver_data_dir_test"

# --- Phase 1: Shutting down the Test Environment ---
echo "🛑 1/3: Stopping the test environment..."

# Usiamo un COMPOSE_PROJECT_NAME diverso per avere volumi separati
export COMPOSE_PROJECT_NAME="$TEST_PROJECT_NAME"
TEST_COMPOSE="docker-compose -f docker-compose.yml -f docker-compose.override.yml -p ${TEST_PROJECT_NAME}"

# Spegniamo solo lo stack di TEST (container, rete e volumi test_*)
${TEST_COMPOSE} down -v --remove-orphans || true

# --- Phase 2: Cleaning Test Artifacts ---
echo "🗑️ 2/3: Cleaning test data..."
echo "Deleting GeoServer test data directory..."
rm -rf "$TEST_GEOSERVER_DATA_DIR"

# --- Phase 3: Restarting the Production Environment ---
echo "🚀 3/3: Restarting the production environment..."

# Per sicurezza rinominiamo l'override di TEST in modo che
# non venga usato accidentalmente per la produzione.
if [ -f "docker-compose.override.yml" ]; then
  echo "Renaming docker-compose.override.yml -> docker-compose.override.yml.backup"
  mv docker-compose.override.yml docker-compose.override.yml.backup
fi

# Ripristiniamo il COMPOSE_PROJECT_NAME di produzione prima di riavviare lo stack prod
export COMPOSE_PROJECT_NAME="$PROD_PROJECT_NAME"
PROD_COMPOSE="docker-compose -f docker-compose.yml -p ${PROD_PROJECT_NAME}"

${PROD_COMPOSE} up -d

echo "--- ✅ CLEANUP COMPLETED. The production environment is active again at http://localhost ---"