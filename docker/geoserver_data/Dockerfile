ARG BASE_IMAGE_VERSION
FROM geonode/geoserver_data:${BASE_IMAGE_VERSION}

# Copio il workspace geonode in una dir temporanea
# Struttura attesa nel contesto di build:
# geonode_workspaces/geonode/workspace.xml
# geonode_workspaces/geonode/backoffice/...
# geonode_workspaces/geonode/styles/...
COPY geonode_workspaces/geonode /tmp/geonode

RUN set -e \
    # mi assicuro che la directory del workspace geonode esista
    && mkdir -p /geoserver_data/data/workspaces/geonode \
    \
    # 1) workspace.xml: lo copio solo se non esiste già
    && if [ ! -f /geoserver_data/data/workspaces/geonode/workspace.xml ]; then \
           cp /tmp/geonode/workspace.xml /geoserver_data/data/workspaces/geonode/workspace.xml; \
       fi \
    \
    # 2) cartella backoffice: la copio solo se NON esiste già
    && if [ ! -d /geoserver_data/data/workspaces/geonode/backoffice ]; then \
           cp -R /tmp/geonode/backoffice /geoserver_data/data/workspaces/geonode/; \
       fi \
    \
    # 3) cartella styles: la copio solo se non esiste già
    && if [ -d /tmp/geonode/styles ] && [ ! -d /geoserver_data/data/workspaces/geonode/styles ]; then \
           cp -R /tmp/geonode/styles /geoserver_data/data/workspaces/geonode/; \
       fi \
    \
    # 4) permessi (nel nostro caso geoserver gira come root:root -> 0:0)
    && chown -R 0:0 /geoserver_data/data/workspaces/geonode \
    \
    # 5) pulizia della dir temporanea
    && rm -rf /tmp/geonode
