from django.db import models
from utils.mixins import Image, ImageProperties


class NewsPhoto(Image):
    news_item = models.OneToOneField(
        'News',
        on_delete=models.CASCADE,
        related_name='photo',
    )
    # person = models.ForeignKey('News', related_name='photos', on_delete=models.CASCADE)


class News(models.Model):
    title = models.TextField(max_length=300)
    content = models.TextField()
    # photo = models.OneToOneField('NewsPhoto', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
