import datetime
import uuid

from django.db import models
from django.utils.timezone import utc
from django_minio_backend import MinioBackend, iso_date_prefix


def get_iso_date() -> str:
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    return f"{now.year}-{now.month}-{now.day}"


class Image(models.Model):
    """
    This is just for uploaded image
    """
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='images'))

    class Meta:
        abstract = True
