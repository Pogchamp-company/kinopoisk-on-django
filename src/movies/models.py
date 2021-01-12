from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


class Score(models.Model):
    value = models.IntegerField(validators=[MinLengthValidator(1), MaxLengthValidator(10)])
    user = models.ForeignKey(User, models.CASCADE, related_name="movie_score")
    movie = models.ForeignKey('Movie', models.CASCADE, related_name="scores")


class Genre(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=150)
    original_name = models.CharField(max_length=150)
    genres = models.ManyToManyField('Genre', related_name='movies')

    def __str__(self):
        return self.title
