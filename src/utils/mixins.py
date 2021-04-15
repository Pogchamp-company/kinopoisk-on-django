import uuid
from os.path import join
from django.db import models
from django.templatetags.static import static
from django_minio_backend import MinioBackend, iso_date_prefix
from utils.enums import ChoiceEnum


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
        LARGE = "Большой"  # 800×600
        MEDIUM = "Средний"  # 400×300
        SMALL = "Маленький"  # 240×180

    format = models.CharField(max_length=10, choices=FormatType.choices())

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.image.name}: ' \
               f'{getattr(self.OrientationType, self.orientation).value}, ' \
               f'{getattr(self.FormatType, self.format).value}'


class ImageProperties:
    @property
    def default_images_folder(self) -> str:
        raise NotImplementedError

    @property
    def images(self):
        raise NotImplementedError

    def _get_image_url_by_filter(self, orientation: Image.OrientationType, format: Image.FormatType, default_url: str):
        return image.image.url if (image :=
                                   (self.images.filter(orientation=orientation.name, format=format.name).first() or
                                    self.images.filter(orientation=orientation.name).first() or
                                    self.images.filter(format=format.name).first() or
                                    self.images.first())) else default_url

    @property
    def big_vertical_image(self):
        return self._get_image_url_by_filter(Image.OrientationType.VERTICAL, Image.FormatType.LARGE,
                                             static(join(self.default_images_folder, "big_vertical.webp")))

    @property
    def medium_vertical_image(self):
        return self._get_image_url_by_filter(Image.OrientationType.VERTICAL, Image.FormatType.MEDIUM,
                                             static(join(self.default_images_folder, "medium_vertical.webp")))

    @property
    def small_vertical_image(self):
        return self._get_image_url_by_filter(Image.OrientationType.VERTICAL, Image.FormatType.SMALL,
                                             static(join(self.default_images_folder, "small_vertical.webp")))

    @property
    def big_horizontal_image(self):
        return self._get_image_url_by_filter(Image.OrientationType.HORIZONTAL, Image.FormatType.LARGE,
                                             static(join(self.default_images_folder, "big_horizontal.webp")))

    @property
    def medium_horizontal_image(self):
        return self._get_image_url_by_filter(Image.OrientationType.HORIZONTAL, Image.FormatType.MEDIUM,
                                             static(join(self.default_images_folder, "medium_horizontal.webp")))

    @property
    def small_horizontal_image(self):
        return self._get_image_url_by_filter(Image.OrientationType.HORIZONTAL, Image.FormatType.SMALL,
                                             static(join(self.default_images_folder, "small_horizontal.webp")))

