import os
import django
import pdb
import json
from datetime import datetime
import sys

# Aggiungi i path necessari per il progetto Django
sys.path.append('/Users/ppalla/opt/my_geo')
sys.path.append('/Users/ppalla/opt/my_geo/src')

# Configura l'ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 's4m_catalogue.settings')
django.setup()

# Importa le configurazioni dal settings
from django.conf import settings

# Importa i dati di prova

# Modifica temporaneamente solo l'host e la porta del database
original_db_config = settings.DATABASES['backoffice'].copy()
settings.DATABASES['backoffice'].update({
    'HOST': '127.0.0.1',  # indirizzo IP dell'host
    'PORT': '5432',       # porta mappata nel docker-compose
    'USER': 'backoffice_user',
    'PASSWORD': 'backoffice_pwd',
    'NAME': 'backoffice'
})

print("Configurazione database originale:", original_db_config)
print("Configurazione database modificata:", settings.DATABASES['backoffice'])
print("Router attuali:", settings.DATABASE_ROUTERS if settings.DATABASE_ROUTERS else "Nessun router configurato")

from backoffice.models import XLSxUpload, ProfileGeneral, LandformTopography
from backoffice.services import XLSxUploadService

def test_import():
    try:
        # Recupera un XLSxUpload con stato UPLOADED usando il modello Django
        xlsx_upload = XLSxUpload.objects.using('backoffice').filter(status='UPLOADED').first()
        
        if not xlsx_upload:
            print("Nessun XLSxUpload trovato nel database con stato UPLOADED")
            return
            
        print(f"Trovato XLSxUpload con ID: {xlsx_upload.id}")
        print(f"Stato attuale: {xlsx_upload.status}")
        print(f"Tipo: {xlsx_upload.type}")
        # Inserisci i dati di prova


        # Verifica il contenuto del campo data
        if xlsx_upload.data:
            print("\nContenuto del campo data:")
            print(json.dumps(xlsx_upload.data, indent=2))
        else:
            print("Il campo data è vuoto")
            return
        
        # Imposta un breakpoint per il debug
        #pdb.set_trace()
        
        # Crea un'istanza del servizio
        service = XLSxUploadService()
        
        # Processa i dati
        result = service.process_uploaded_data(xlsx_upload.id)
        
        print("\nRisultato del processing:")
        print(json.dumps(result, indent=2))
        
        # Verifica i dati importati
        print("\nVerifica dei dati importati:")
        
        # Controlla ProfileGeneral
        profiles = ProfileGeneral.objects.using('backoffice').all()
        print(f"\nNumero di profili nel database: {profiles.count()}")
        
        # Controlla LandformTopography
        landforms = LandformTopography.objects.using('backoffice').all()
        print(f"Numero di landform nel database: {landforms.count()}")
        
        # Aggiorna lo stato dell'upload
        xlsx_upload.refresh_from_db()
        print(f"\nStato finale dell'upload: {xlsx_upload.status}")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {str(e)}")
        raise
    finally:
        # Ripristina la configurazione originale
        settings.DATABASES['backoffice'] = original_db_config

if __name__ == "__main__":
    test_import() 