
class SttpappRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'sttpapp':  # Ensure app label is in lowercase
            return 'sttpnew'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'sttpapp':  # Ensure app label is in lowercase
            return 'sttpnew'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'sttpapp' or obj2._meta.app_label == 'sttpapp':  # Ensure app label is in lowercase
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'sttpapp':  # Ensure app label is in lowercase
            return db == 'sttpnew'
        return db == 'default'
