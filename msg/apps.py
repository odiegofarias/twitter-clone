from django.apps import AppConfig


class MsgConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'msg'

    def ready(self) -> None:
        import msg.signals
        
        return super().ready()
    