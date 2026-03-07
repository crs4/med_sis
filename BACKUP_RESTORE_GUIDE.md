# Backup and Restore Guide

This document describes the backup and restore procedures for the Med_SIS GeoNode/GeoServer stack. All scripts are Bash-based and use Docker Compose.

---

## Overview

The system performs a **full backup** of GeoNode metadata, GeoServer configuration, and PostgreSQL databases. Restore can target either:

- **Test environment** (`s4m_catalogue_test`) — isolated from production, uses port 8081
- **Production environment** (`s4m_catalogue`) — live system on port 80

---

## Files Involved

| File | Role |
|------|------|
| `lib_common.sh` | Shared functions (DB wait, restore, GeoServer fixes, etc.) |
| `complete_backup.sh` | Full backup: GeoNode + GeoServer + databases |
| `restore_on_test.sh` | Restore to isolated test environment |
| `restore_on_production.sh` | Restore to production environment |
| `cleanup_test.sh` | Stops test stack, removes artifacts, restarts production |

---

## Backup Procedure

### Script: `complete_backup.sh`

**Usage:**
```bash
./complete_backup.sh
```

**Prerequisites:** Production stack must be running (`docker-compose up -d`).

**What it does:**

1. **Preventive restart** — Restarts Django and GeoServer for a clean state.
2. **GeoNode backup** — Runs `manage.py backup` (official GeoNode backup). Output: `YYYYMMDD-HHMMSS.zip` in `./backups/`.
3. **GeoServer datastores** — Archives all `datastore.xml` files from GeoServer workspaces. Output: `geoserver-datastores-YYYYMMDD-HHMMSS.tar.gz`.
4. **Geodata dump** — `pg_dump` of `my_geo_data` (shapefile tables). Output: `backup-geodata-YYYYMMDD-HHMMSS.dump`.
5. **Backoffice dump** — `pg_dump` of `backoffice`. Output: `backup-backoffice-YYYYMMDD-HHMMSS.dump`.

**Output directory:** `./backups/`

---

## Restore Procedure

### Test Environment: `restore_on_test.sh`

**Usage:**
```bash
./restore_on_test.sh                                    # Auto-discover latest backups in ./backups/
./restore_on_test.sh /path/to/backup.zip /path/to/backoffice.dump   # Explicit files
```

**Behaviour:**

- **Auto-discovery:** With no arguments, searches `./backups/` (or `$BACKUP_SEARCH_DIR`) for the most recent `.zip`, `backup-backoffice-*.dump`, `backup-geodata-*.dump`, and `geoserver-datastores-*.tar.gz`.
- **Explicit files:** With two arguments, uses the given GeoNode backup and backoffice dump; geodata and datastores are auto-discovered in the same directory as the GeoNode backup.

**Phases:**

1. **Shutdown** — Stops production containers on conflicting ports (nginx, geoserver), then stops the test stack.
2. **Data restore** — Prepares test DBs (`test_my_geo`, `test_my_geo_data`, `test_backoffice`), restores backoffice and geodata dumps, extracts GeoServer catalog from the GeoNode zip, runs migrations, injects datastores (with DB name substitution), runs `manage.py restore`, fixes URLs in the DB, and runs `migrate_baseurl`.
3. **Startup** — Starts the full test stack, waits for Django health, and applies GeoServer styles fix.
4. **Verification** — Prints status and URLs.

**Test URL:** `http://localhost:8081`  
**Production:** Unchanged at `http://localhost`

---

### Production Environment: `restore_on_production.sh`

**Usage:**
```bash
./restore_on_production.sh                              # Auto-discover latest backups
./restore_on_production.sh /path/to/backup.zip /path/to/backoffice.dump   # Explicit files
```

**Behaviour:**

- Same auto-discovery and explicit-file logic as the test restore.

**Phases:**

1. **Partial shutdown** — Stops Django, GeoNode, Celery, GeoServer, data-dir-conf. Database stays up.
2. **DB preparation** — Prepares `my_geo`, `my_geo_data`, `backoffice`.
3. **Database restore** — Restores backoffice and geodata dumps.
4. **Migration + GeoNode restore** — Runs migrations, starts GeoServer, runs `manage.py restore`, injects datastores (no DB name substitution).
5. **Full restart** — Starts all services and applies GeoServer styles fix.

---

## Cleanup: `cleanup_test.sh`

**Usage:**
```bash
./cleanup_test.sh
```

**What it does:**

1. Stops the test environment and removes volumes.
2. Deletes `./geoserver_data_dir_test`.
3. Renames `docker-compose.override.yml` → `docker-compose.override.yml.backup` (so production does not use test override).
4. Restarts the production stack.

---

## Shared Library: `lib_common.sh`

**Usage:** All scripts source it with:

```bash
source "$(dirname "$0")/lib_common.sh"
```

**Main functions:**

| Function | Purpose |
|----------|---------|
| `find_latest_file DIR PATTERN` | Returns the most recent file matching the pattern in `DIR` |
| `wait_for_db CONTAINER [USER] [MAX]` | Waits for PostgreSQL to accept connections |
| `grant_db_permissions CONTAINER DB OWNER [USER]` | Grants schema/table permissions to the application user |
| `fix_fixture_fk_violations CONTAINER DB [USER]` | Removes orphan records that block fixture loading |
| `prepare_db CONTAINER DB OWNER [USER]` | Drops, recreates, enables PostGIS, sets permissions |
| `restore_pg_dump CONTAINER DUMP DB [USER]` | Copies dump into container and runs `pg_restore` |
| `apply_manage_restore COMPOSE DJANGO CONTAINER ZIP CONFIG` | Runs `manage.py restore` with a `curs.close()` bug patch |
| `wait_for_geoserver CONTAINER [MAX]` | Waits for GeoServer to respond (HTTP 200/302/401/403) |
| `fix_geoserver_styles_after_startup CONTAINER` | Fixes corrupted GeoServer styles (backup SLD, reload catalog, register via REST, fix layer associations) |
| `inject_geoserver_datastores CONTAINER ARCHIVE [DB_MAP]` | Injects `datastore.xml` files; optionally substitutes DB names for test |

---

## Backup File Naming

| Pattern | Purpose |
|---------|---------|
| `*.zip` | GeoNode backup (metadata, layers, GeoServer catalog) |
| `backup-backoffice-*.dump` | Backoffice PostgreSQL dump |
| `backup-geodata-*.dump` | `my_geo_data` (shapefile tables) dump |
| `geoserver-datastores-*.tar.gz` | GeoServer datastore.xml backup |

---

## Environment Variables

| Variable | Default | Used by |
|----------|---------|---------|
| `BACKUP_SEARCH_DIR` | `./backups` | `restore_on_test.sh` (auto-discovery) |
| `SITEURL` | `http://localhost` | `restore_on_production.sh` (final message) |
| `COMPOSE_PROJECT_NAME` | `s4m_catalogue` / `s4m_catalogue_test` | All scripts |

---

## Quick Reference

```bash
# Backup (production must be running)
./complete_backup.sh

# Restore to test
./restore_on_test.sh

# Restore to production
./restore_on_production.sh

# Cleanup test and restart production
./cleanup_test.sh
```
