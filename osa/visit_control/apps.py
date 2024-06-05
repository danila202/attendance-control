from django.apps import AppConfig


class VisitControlConfig(AppConfig):
    name = 'visit_control'

    def ready(self):
        import visit_control.signals




