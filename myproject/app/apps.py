from django.apps import AppConfig


class MovieAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from . import signals, bst
        import sys
        if any(cmd in sys.argv for cmd in ('makemigrations', 'migrate', 'collectstatic')):
            return
        try:
            bst.build_tree()
        except Exception:
            pass