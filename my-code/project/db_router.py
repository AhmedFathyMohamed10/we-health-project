class DatabaseRouter:
    """
    A router to control all database operations on models in specific apps.
    """

    def db_for_read(self, model, **hints):
        """
        Directs read operations to the appropriate database.
        """
        if model._meta.app_label == "mic_api":
            return "default"  # MongoDB
        return "mongodb"  # PostgreSQL

    def db_for_write(self, model, **hints):
        """
        Directs write operations to the appropriate database.
        """
        if model._meta.app_label == "mic_api":
            return "default"  # MongoDB
        return "mongodb"  # PostgreSQL

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the same database is involved.
        """
        db_obj1 = self.db_for_read(obj1)
        db_obj2 = self.db_for_read(obj2)
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that apps only appear in the appropriate database.
        """
        if app_label == "mic_api":
            return db == "default"  # MongoDB
        return db == "mongodb"  # PostgreSQL
