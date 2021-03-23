import uuid
from utils.enums import ChoiceEnum
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix


class Image(models.Model):
    """
    This is just for uploaded image
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='images'))

    class OrientationType(ChoiceEnum):
        VERTICAL = "Вертикальный"
        HORIZONTAL = "Горизонтальный"

    orientation = models.CharField(max_length=10, choices=OrientationType.choices())

    class FormatType(ChoiceEnum):
        LARGE = "Большой"  # 800×800
        MEDIUM = "Средний"  # 400×400
        SMALL = "Маленький"  # 240×240

    format = models.CharField(max_length=10, choices=FormatType.choices())

    class Meta:
        abstract = True
