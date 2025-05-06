class BackofficeRouter:
    """
    Un router per controllare tutte le operazioni di database per i modelli dell'app backoffice
    """
    def db_for_read(self, model, **hints):
        """
        I modelli dell'app backoffice vanno sul database 'backoffice'
        """
        if model._meta.app_label == 'backoffice':
            return 'backoffice'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        I modelli dell'app backoffice vanno sul database 'backoffice'
        """
        if model._meta.app_label == 'backoffice':
            return 'backoffice'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permette le relazioni se un modello nell'app backoffice è coinvolto
        """
        if obj1._meta.app_label == 'backoffice' or obj2._meta.app_label == 'backoffice':
            return True
        elif 'backoffice' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Assicura che l'app backoffice venga migrata solo sul database 'backoffice'
        """
        if app_label == 'backoffice':
            return db == 'backoffice'
        return db == 'default'