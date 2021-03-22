from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.templatetags.static import static
from utils.mixins import Image


class Poster(Image):
    movie = models.ForeignKey('Movie', related_name='posters', on_delete=models.CASCADE)


class Score(models.Model):
    value = models.IntegerField(validators=[MinLengthValidator(1), MaxLengthValidator(10)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)


class Genre(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Actor(models.Model):
    role_name = models.CharField(max_length=100)

    person = models.ForeignKey('person.Person', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)


class MovieType(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150)
    genres = models.ManyToManyField('Genre', related_name='movies')
    movie_type = models.ForeignKey('MovieType', on_delete=models.PROTECT, related_name='movies', null=True)
    year = models.IntegerField(validators=[MinValueValidator(1895)])
    slogan = models.TextField(max_length=500)
    duration = models.DurationField()
    budget = models.IntegerField(validators=[MinValueValidator(0)])

    # Person relationships
    # directors = models.ManyToManyField(Person, related_name='directed_movies')
    # writers = models.ManyToManyField(Person, related_name='wrote_movies')
    # producers = models.ManyToManyField(Person, related_name='produced_movies')
    # operators = models.ManyToManyField(Person, related_name='operated_movies')
    # composers = models.ManyToManyField(Person, related_name='composed_movies')
    # production_designers = models.ManyToManyField(Person, related_name='production_designed_movies')
    # editors = models.ManyToManyField(Person, related_name='edited_movies')
    # actors = models.ManyToManyField('person.Person', through='Actor', related_name='actor_in_movies')

    # User relationships
    scores = models.ManyToManyField(User, through='Score', related_name='movies_scores')

    def __str__(self):
        return self.title

    @property
    def first_poster_url(self):
        poster = self.posters.first()
        if not poster:
            return static('icon/poster_1.jpg')
        return poster.image.url
