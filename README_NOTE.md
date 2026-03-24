
change name to med_sis

python manage.py set_layers_permissions --help 

*all'inizializzazione SOLO una volta
python manage.py set_layers_permissions -g data-managers -p manage -d
python manage.py updatelayers --skip-geonode-registered --remove-deleted -s backoffice

*ad ogni modifica
python manage.py updatelayers -s backoffice
python manage.py sync_geonode_datasets