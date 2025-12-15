#!/bin/bash
set -a
for f in /root/.override_env /usr/src/s4m_catalogue/.override_env /usr/src/s4m_catalogue/.env; do
    [ -f "$f" ] && source "$f"
done
set +a

export SPATIALITE_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/mod_spatialite.so
cd /usr/src/s4m_catalogue
<<<<<<< HEAD
python manage.py updatelayers -s backoffice --skip-geonode-registered
=======
python manage.py updatelayers -s backoffice
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
