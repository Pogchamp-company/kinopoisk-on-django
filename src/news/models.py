from django.db import models


class News(models.Model):
    title = models.TextField(max_length=300)
    content = models.TextField()
