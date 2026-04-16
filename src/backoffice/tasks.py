from celery import shared_task
from .services import XLSxUploadService, DatasetService
from .models import XLSxUpload, Dataset
import logging
from django.core.management import call_command

logger = logging.getLogger(__name__)

@shared_task(bind=True, name='backoffice.tasks.process_xlsx_upload', queue='default')
def process_xlsx_upload(self, upload_id):
    """
    Task to elaborate XLSx data in a XLSxUpload object
    """
    upload = None
    try:
        logger.info(f"Starting processing upload {upload_id}")
        # Recupera l'oggetto XLSxUpload
        upload = XLSxUpload.objects.using('backoffice').get(id=upload_id)
        
        # Verifica che lo stato sia IN_PROCESS
        if upload.status != "IN_PROCESS":
            logger.warning(f"Upload {upload_id} is not in IN_PROCESS status  (current state: {upload.status})")
            return False

        logger.info(f"Processing upload {upload_id} data...")
        service = XLSxUploadService()
        report = service.process_uploaded_data(upload_id)
        
        # Aggiorna il report e lo stato
        upload.report = report
        if report.get('errors'):
            upload.status = "IMPORT_WITH_ERROR"
            logger.warning(f"Upload {upload_id} completed with {len(report.get('errors', []))} errors")
            for error in report.get('errors', [])[:5]:  # Log primi 5 errori
                logger.error(f"Upload {upload_id} error: {error}")
        else:
            upload.status = "IMPORT_SUCCESS"
            logger.info(f"Upload {upload_id} completed successfully with {len(report.get('operations', []))} operations")
        upload.save(using='backoffice')
        # ---------------------------------------------------------------------------------------------
        # NUOVO BLOCCO: Trigger updatelayers se l'import è un successo
        # -----------------------------------------------------------
        logger.debug(f"Upload {upload_id} status: {upload.status}")
        if upload.status == "IMPORT_SUCCESS":
            try:
                logger.info(f"Avvio comando updatelayers per upload {upload_id} su store 'backoffice'...")
                
                # Esegue: python manage.py updatelayers --store=backoffice
                call_command('updatelayers', store='backoffice')
                
                logger.info("Comando updatelayers eseguito con successo.")
            except Exception as e:
                # Logghiamo l'errore ma non facciamo fallire l'upload che è già marcato come SUCCESS
                logger.error(f"Errore critico durante l'esecuzione di updatelayers per upload {upload_id}: {str(e)}")
        # -----------------------------------------------------------

        upload.refresh_from_db(using='backoffice')
        logger.info(f"End of upload {upload_id} elaboration with status: {upload.status}")
        
        return True
        
    except XLSxUpload.DoesNotExist:
        logger.error(f"Upload {upload_id} non trovato")
        return False
    except Exception as e:
        logger.error(f"Errors elaborating upload {upload_id}: {str(e)}")
        # Aggiorna lo stato in caso di errore critico
        if upload:
            try:
                upload.status = "CRITICAL_ERROR"
                upload.report = {"critical_error": str(e), "traceback": logger.formatException(e_info=True)}
                upload.save(using='backoffice')
            except Exception as save_e:
                logger.error(f"It is not possible to save the status CRITICAL_ERROR in upload {upload_id}: {save_e}")
        return False

@shared_task(bind=True, name='backoffice.tasks.process_dataset', queue='default')
def process_dataset(self, dataset_id):
    """
    Task to elaborate soil data and finalize a Dataset object
    """
    dataset = None
    try:
        logger.info(f"Starting processing dataset {dataset_id}")
        # Recupera l'oggetto Dataset
        dataset = Dataset.objects.using('backoffice').get(id=dataset_id)
        
        # Verifica che lo stato sia IN_PROCESS
        if dataset.status != "IN_PROCESS" and dataset.status != "IN_PREPROCESS":
            logger.warning(f"Dataset {dataset_id} is not in IN_PROCESS or IN_PREPROCESS status  (current state: {dataset.status})")
            return False
        logger.info(f"Processing dataset {dataset_id} data...")
        service = DatasetService()
        result = False
        if dataset.status == "IN_PROCESS":
            result = service.process_dataset_data(dataset_id)
            if result:
                dataset.status = "PUBLISHED"
                logger.info(f"Dataset {dataset_id} published successfully")
            else:
                dataset.status = "ERRORS"
                logger.warning(f"Dataset {dataset_id} not published")
        else :
            result = service.preprocess_dataset_data(dataset_id)
            if result:
                dataset.status = "PREPROCESSED"
                logger.info(f"Dataset {dataset_id} completed preprocess successfully")
            else:
                dataset.status = "ERRORS"
                logger.warning(f"dataset {dataset_id} preprocess with errors")
            
        dataset.save(using='backoffice')
        # ---------------------------------------------------------------------------------------------
        # NUOVO BLOCCO: Trigger updatelayers se l'import è un successo
        # -----------------------------------------------------------
        return True
        
    except Dataset.DoesNotExist:
        logger.error(f"Dataset {dataset_id} not found")
        return False
    except Exception as e:
        logger.error(f"Errors elaborating dataset {dataset_id}: {str(e)}")
        # Aggiorna lo stato in caso di errore critico
        if dataset:
            try:
                dataset.status = "ERRORS"
                dataset.save(using='backoffice')
            except Exception as save_e:
                logger.error(f"It is not possible to save the status ERRORS in dataset {dataset_id}: {save_e}")
        return False


    