from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account.user'
    label = 'account'

    def ready(self):
        import account.user.signals
