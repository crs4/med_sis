
ARG BASE_IMAGE_VERSION=${BASE_IMAGE_VERSION:-15-3.5-latest}
FROM geonode/postgis:${BASE_IMAGE_VERSION}

ARG BACKOFFICE_DATABASE_PASSWORD
ARG BACKOFFICE_DATABASE_USER
RUN echo "CREATE USER "${BACKOFFICE_DATABASE_USER}" WITH PASSWORD '"${BACKOFFICE_DATABASE_PASSWORD}"';" > /docker-entrypoint-initdb.d/01-create-backoffice-db.sql
RUN echo "CREATE DATABASE backoffice WITH OWNER "${BACKOFFICE_DATABASE_USER}";" >> /docker-entrypoint-initdb.d/01-create-backoffice-db.sql
RUN echo "\c backoffice" >> /docker-entrypoint-initdb.d/01-create-backoffice-db.sql
RUN echo "CREATE EXTENSION postgis;" >> /docker-entrypoint-initdb.d/01-create-backoffice-db.sql
RUN echo "GRANT ALL PRIVILEGES ON DATABASE backoffice TO "${BACKOFFICE_DATABASE_USER}"; " >> /docker-entrypoint-initdb.d/01-create-backoffice-db.sql
RUN cat  /docker-entrypoint-initdb.d/01-create-backoffice-db.sql