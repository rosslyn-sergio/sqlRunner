from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = "websqlrunner"

    def ready(self):
        import_module("websqlrunner.receivers")
        import_module("websqlrunner.settings")
