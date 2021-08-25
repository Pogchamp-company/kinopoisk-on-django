from ckeditor.fields import RichTextField
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix


class News(models.Model):
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    preview_content = RichTextField(verbose_name='Превью')

    content = RichTextField(verbose_name='Содержание')
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='news-images'), null=True,
                              verbose_name='Иллюстрация')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
