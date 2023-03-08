import os

from .models import DataSet
from django.db import models
from django.dispatch import receiver


@receiver(models.signals.post_delete, sender=DataSet)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `DataSet` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
