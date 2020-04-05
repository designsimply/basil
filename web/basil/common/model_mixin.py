from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


@receiver(
    pre_save,
    sender=TimestampMixin,
)
def update_timestamp_model(sender, instance, *args, **kwargs):
    """ Update the timestamps when model is save() is called """
    if not instance.pk:
        instance.created_at = timezone.now()
    instance.updated_at = timezone.now()
