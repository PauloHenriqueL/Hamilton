from django.apps import AppConfig


class Desistencia_altaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'desistencia_alta'

    def ready(self):
        import desistencia_alta.signals 