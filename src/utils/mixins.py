import uuid
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix


class Image(models.Model):
    """
    This is just for uploaded image
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='images'))

    class Meta:
        abstract = True
