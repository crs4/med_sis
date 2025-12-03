FROM geonode/geonode-base:latest-ubuntu-22.04
RUN sed -i 's|http://archive.ubuntu.com/ubuntu|http://security.ubuntu.com/ubuntu|g' /etc/apt/sources.list
LABEL GeoNode development team

RUN mkdir -p /usr/src/s4m_catalogue

RUN apt-get update -y \
&& apt-get install --no-install-recommends curl wget unzip gnupg2 saga locales cron libsqlite3-mod-spatialite -y \
&& rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN sed -i -e 's/# C.UTF-8 UTF-8/C.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# add bower and grunt command
COPY src /usr/src/s4m_catalogue/
WORKDIR /usr/src/s4m_catalogue

## Add cron job to update backoffice layers every hour at minute 0
COPY src/backoffice-updatelayers-cron /etc/cron.d/backoffice-updatelayers-cron
RUN chmod 0644 /etc/cron.d/backoffice-updatelayers-cron && \
    #crontab /etc/cron.d/backoffice-updatelayers-cron && \
    touch /var/log/backoffice-updatelayers.log

#COPY src/monitoring-cron /etc/cron.d/monitoring-cron
#RUN chmod 0644 /etc/cron.d/monitoring-cron
#RUN crontab /etc/cron.d/monitoring-cron
#RUN touch /var/log/cron.log
#RUN service cron start

COPY src/wait-for-databases.sh /usr/bin/wait-for-databases
RUN chmod +x /usr/bin/wait-for-databases
RUN chmod +x /usr/src/s4m_catalogue/tasks.py &&\
    chmod +x /usr/src/s4m_catalogue/entrypoint.sh

COPY src/celery.sh /usr/bin/celery-commands
RUN chmod +x /usr/bin/celery-commands

COPY src/celery-cmd /usr/bin/celery-cmd
RUN chmod +x /usr/bin/celery-cmd

# Install "geonode-contribs" apps
# RUN cd /usr/src; git clone https://github.com/GeoNode/geonode-contribs.git -b master
# Install logstash and centralized dashboard dependencies
# RUN cd /usr/src/geonode-contribs/geonode-logstash; pip install --upgrade  -e . \
#     cd /usr/src/geonode-contribs/ldap; pip install --upgrade  -e .

RUN yes w | pip install --src /usr/src -r requirements.txt &&\
    yes w | pip install -e .

# Cleanup apt update lists
RUN apt-get autoremove --purge &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Export ports
EXPOSE 8088

# We provide no command or entrypoint as this image can be used to serve the django project or run celery tasks
# ENTRYPOINT /usr/src/s4m_catalogue/entrypoint.sh
