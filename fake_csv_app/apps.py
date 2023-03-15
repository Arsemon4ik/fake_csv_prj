from django.apps import AppConfig


class FakeCsvAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fake_csv_app'

    # def ready(self):
    #     import fake_csv_app.signals