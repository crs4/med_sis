#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== MED-SIS initialization ==="

echo "=== Initializing GeoWebCache ==="
bash "$SCRIPT_DIR/init_geowebcache.sh"

echo "=== Initializing GeoNode datasets ==="
bash "$SCRIPT_DIR/init_geoserver_datasets.sh"

echo "=== Initializing documents ==="
bash "$SCRIPT_DIR/init_documents.sh"

echo "=== MED-SIS initialization completed ==="
