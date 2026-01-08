FROM geonode/geonode-base:latest-ubuntu-24.04
LABEL GeoNode development team

RUN mkdir -p /usr/src/s4m_catalogue

# Install additional packages needed by the project
RUN apt-get update -y \
    && apt-get install --no-install-recommends curl wget unzip gnupg2 saga locales cron libsqlite3-mod-spatialite -y \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Configure locale
RUN sed -i -e 's/# C.UTF-8 UTF-8/C.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Copy local geonode src inside container
COPY src /usr/src/s4m_catalogue/
WORKDIR /usr/src/s4m_catalogue

# Add cron job to update backoffice layers every hour at minute 0
COPY src/backoffice-updatelayers-cron /etc/cron.d/backoffice-updatelayers-cron
RUN chmod 0644 /etc/cron.d/backoffice-updatelayers-cron && \
    touch /var/log/backoffice-updatelayers.log

COPY src/wait-for-databases.sh /usr/bin/wait-for-databases
RUN chmod +x /usr/bin/wait-for-databases
RUN chmod +x /usr/src/s4m_catalogue/tasks.py &&\
    chmod +x /usr/src/s4m_catalogue/entrypoint.sh

COPY src/celery.sh /usr/bin/celery-commands
RUN chmod +x /usr/bin/celery-commands

COPY src/celery-cmd /usr/bin/celery-cmd
RUN chmod +x /usr/bin/celery-cmd

# Install "geonode-contribs" apps (commented out)
# RUN cd /usr/src; git clone https://github.com/GeoNode/geonode-contribs.git -b master
# Install logstash and centralized dashboard dependencies
# RUN cd /usr/src/geonode-contribs/geonode-logstash; pip install --upgrade  -e . \
#     cd /usr/src/geonode-contribs/ldap; pip install --upgrade  -e .

# Update pip and setuptools to latest versions for Python 3.12 compatibility
RUN pip install --upgrade pip setuptools wheel

# Install Shapely 2.x which is compatible with Python 3.12
# GeoNode 4.4.x requires Shapely==1.8.5.post1, but that version doesn't work with Python 3.12
# Shapely 2.x is API-compatible with 1.x for most use cases and works with Python 3.12
RUN pip install --no-cache-dir "Shapely>=2.0.0,<3.0.0"

# Note: The venv is already activated in the base image, no need to activate it manually
# Install dependencies. Shapely 2.x is already installed.
# Workaround for Shapely 1.8.5.post1 incompatibility with Python 3.12:
# Install GeoNode packages with --no-deps, then install dependencies from setup.py
RUN yes w | pip install --src /usr/src -e git+https://github.com/GeoNode/geonode-mapstore-client.git@4.4.x#egg=django_geonode_mapstore_client && \
    yes w | pip install --src /usr/src -e git+https://github.com/GeoNode/geonode-importer.git@1.1.x#egg=geonode-importer && \
    yes w | pip install --src /usr/src -e git+https://github.com/GeoNode/geonode.git@4.4.x#egg=GeoNode --no-deps && \
    # Install GeoNode dependencies from its setup.py, excluding Shapely
    cd /usr/src/geonode && \
    python setup.py egg_info > /dev/null 2>&1 && \
    pip install $(grep -v "^#" *.egg-info/requires.txt 2>/dev/null | grep -v "Shapely" | tr '\n' ' ' || echo "") && \
    cd /usr/src/s4m_catalogue && \
    # Ensure Shapely 2.x is installed (skip incompatible 1.8.5.post1)
    pip install --force-reinstall --no-deps "Shapely>=2.0.0,<3.0.0" && \
    pip install django-extensions && \
    # Install the project itself
    yes w | pip install -e .

# Cleanup apt update lists
RUN apt-get autoremove --purge &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Export ports
# Note: You can choose to keep 8088 or change to 8000
# If changing to 8000, update all references in docker-compose.yml, settings.py, uwsgi.ini, env.txt
EXPOSE 8088

# We provide no command or entrypoint as this image can be used to serve the django project or run celery tasks
# ENTRYPOINT /usr/src/s4m_catalogue/entrypoint.sh

