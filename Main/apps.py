from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'Main'
    def ready(self):
        from . import signals