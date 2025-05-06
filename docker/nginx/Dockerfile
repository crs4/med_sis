ARG BASE_IMAGE_VERSION
FROM geonode/nginx:${BASE_IMAGE_VERSION}

# copy local src inside container
COPY ./geonode.conf.envsubst /etc/nginx/sites-enabled/ 
