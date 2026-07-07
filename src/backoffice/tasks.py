from celery import shared_task
from .services import XLSxUploadService, DatasetService, BaseDatasetService
from .models import XLSxUpload, Dataset, BaseDataset
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
        if dataset.status != "IN_PROCESS":
            logger.warning(f"Dataset {dataset_id} is not in IN_PROCESS status  (current state: {dataset.status})")
            return False
        logger.info(f"Processing dataset {dataset_id} data...")
        service = DatasetService()
        report = service.process_dataset_data(dataset_id)
        if report:
            dataset.report = report
            for msg in report.get('msgs'):
                logger.info(f"msg: {msg}")
            if report.get('success'):
                dataset.status = "PUBLISHED"
                logger.info(f"Dataset {dataset_id} published")
            else:
                dataset.status = "ERRORS"
                logger.warning(f"Dataset {dataset_id} not published")
            dataset.save(using='backoffice')
            return True
        return False
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

@shared_task(bind=True, name='backoffice.tasks.process_base_dataset', queue='default')
def process_base_dataset(self, dataset_id):
    """
    Task to create a base dataset in the catalogue and manage its metadata
    """
    dataset = None
    try:
        logger.info(f"Starting processing base dataset {dataset_id}")
        # Recupera l'oggetto Dataset
        dataset = BaseDataset.objects.using('backoffice').get(code=dataset_id)
        
        # Verifica che lo stato sia IN_PROCESS
        if dataset.status != "IN_PROCESS":
            logger.warning(f"Dataset {dataset_id} is not in IN_PROCESS status  (current state: {dataset.status})")
            return False
        logger.info(f"Processing base dataset {dataset_id} data...")
        service = BaseDatasetService()
        report = service.process_base_dataset_data(dataset_id)
        if report:
            for msg in report.get('msgs'):
                logger.info(f"msg: {msg}")
            if report.get('success'):
                dataset.status = "PUBLISHED"
                dataset.geonode_id = report.get('geonode')
                logger.info(f"Dataset {dataset_id} published")
            else:
                dataset.status = "ERRORS"
                logger.warning(f"Dataset {dataset_id} not published")
            dataset.save(using='backoffice')
            return True
        return False
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
    
@shared_task(bind=True, name='backoffice.tasks.process_hydro_ptf_model', queue='default')
def process_hydro_ptf_model(self, dataset_id):
    return False;

@shared_task(bind=True, name='backoffice.tasks.process_hydro_ptf_elaboration', queue='default')
def process_hydro_ptf_elaboration(self, dataset_id):
    return False;
    