class Router1:
    route_app_labels = "musics"

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.route_app_labels:
            return "readonly"
        return None # 回傳 None 等於回傳 default

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.route_app_labels:
            return "primary"
        return None # 回傳 None 等於回傳 default

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
