from ckeditor.fields import RichTextField
from django.db import models
# from utils.mixins import Image
from django_minio_backend import MinioBackend, iso_date_prefix


# class NewsPhoto(Image):
#     news_item = models.OneToOneField(
#         'News',
#         on_delete=models.CASCADE,
#         related_name='photo',
#     )

    # person = models.ForeignKey('News', related_name='photos', on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=300)
    preview_content = RichTextField()

    # content = models.TextField()
    content = RichTextField()
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='news-images'), null=True)

    def __str__(self):
        return self.title
