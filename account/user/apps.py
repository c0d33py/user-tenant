from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account.user'
    label = 'account'

    def ready(self):
        # Django signals enabled
        import account.user.signals
