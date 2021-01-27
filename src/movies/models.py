from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)

    birth_date = models.DateField()

    @property
    def fullname(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return self.fullname


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
    year = models.IntegerField(validators=[MinValueValidator(1895)])
    slogan = models.TextField(max_length=500)
    duration = models.DurationField()

    def __str__(self):
        return self.title
