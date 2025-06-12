from celery import shared_task
from .services import XLSxUploadService
from .models import XLSxUpload
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, name='backoffice.tasks.process_xlsx_upload', queue='default')
def process_xlsx_upload(self, upload_id):
    """
    Task per elaborare un file XLSx caricato
    """
    upload = None
    try:
        # Recupera l'oggetto XLSxUpload
        upload = XLSxUpload.objects.using('backoffice').get(id=upload_id)
        
        # Verifica che lo stato sia IN_PROCESS
        if upload.status != "IN_PROCESS":
            logger.warning(f"Upload {upload_id} non è in stato IN_PROCESS (stato attuale: {upload.status})")
            return False

        # Elabora i dati utilizzando il servizio
        #service = XLSxUploadService(upload)
        service = XLSxUploadService()
        report = service.process_uploaded_data(upload_id)
        
        # Aggiorna il report e lo stato
        upload.report = report
        if report.get('errors'):
            upload.status = "IMPORT_WITH_ERROR"
        else:
            upload.status = "IMPORT_SUCCESS"
        upload.save()

        upload.refresh_from_db(using='backoffice')
        logger.info(f"Elaborazione per upload {upload_id} completata con stato: {upload.status}")
        
        return True
        
    except XLSxUpload.DoesNotExist:
        logger.error(f"Upload {upload_id} non trovato")
        return False
    except Exception as e:
        logger.error(f"Errore durante l'elaborazione dell'upload {upload_id}: {str(e)}")
        # Aggiorna lo stato in caso di errore critico
        if upload:
            try:
                upload.status = "CRITICAL_ERROR"
                upload.report = {"critical_error": str(e), "traceback": logger.formatException(e_info=True)}
                upload.save(using='backoffice')
            except Exception as save_e:
                logger.error(f"Impossibile salvare lo stato CRITICAL_ERROR per l'upload {upload_id}: {save_e}")
        return False

    """     try:
            upload.status = "CRITICAL_ERROR"
            upload.report = {"error": str(e)}
            upload.save()
        except:
            pass
        return False """ 