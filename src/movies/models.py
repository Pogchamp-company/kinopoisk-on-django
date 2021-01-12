from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


class Score(models.Model):
    value = models.IntegerField(validators=[MinLengthValidator(1), MaxLengthValidator(10)])
    user = models.ForeignKey(User, models.CASCADE)
    movie = models.ForeignKey('Movie', models.CASCADE)


class Genre(models.Model):
    title = models.CharField(max_length=30)


class Movie(models.Model):
    title = models.CharField(max_length=150)
    original_name = models.CharField(max_length=150)
    genres = models.ManyToManyField('Genre', related_name='movies')
