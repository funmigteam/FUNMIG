from django.apps import AppConfig
from django.db.models.signals import post_save


def _optimize_uploaded_image(sender, instance, created, update_fields=None, **kwargs):
    from .images import optimize_instance
    if update_fields and not set(update_fields) & {'avatar', 'image', 'file', 'cover'}:
        return
    optimize_instance(instance)


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from .images import IMAGE_FIELDS
        for app_label, model_name in IMAGE_FIELDS:
            post_save.connect(
                _optimize_uploaded_image,
                sender=f'{app_label}.{model_name}',
                dispatch_uid=f'optimize-{model_name}',
            )
