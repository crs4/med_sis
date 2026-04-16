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
RUN chmod +x /usr/src/s4m_catalogue/cron-backoffice-updatelayers.sh

COPY src/celery.sh /usr/bin/celery-commands
RUN chmod +x /usr/bin/celery-commands

COPY src/celery-cmd /usr/bin/celery-cmd
RUN chmod +x /usr/bin/celery-cmd

RUN python -m pip install -U pip setuptools wheel
RUN yes w | pip install --src /usr/src -r requirements.txt

RUN apt-get autoremove --purge &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

COPY src/ /usr/src/project/
RUN yes w | pip install -e .

EXPOSE 8000

