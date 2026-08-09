ARG BASE_IMAGE_VERSION
#### nginx vulnerability -> version 1.31.3 not pesent in geonode
FROM geonode/nginx:${BASE_IMAGE_VERSION}
#FROM nginx:${BASE_IMAGE_VERSION}

#RUN apt-get update && apt-get install procps -y

# copy local src inside container
COPY ./geonode.conf.envsubst /etc/nginx/sites-enabled/
#COPY ./nginx.https.available.conf.envsubst /etc/nginx/
#COPY ./nginx.conf.envsubst /etc/nginx/

#COPY ./docker-entrypoint.sh /
RUN ls -la  /etc/nginx/


