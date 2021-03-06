from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models
import uuid
import datetime
from django.db import models
from django.db.models.fields.files import FieldFile
from django.utils.timezone import utc
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django_minio_backend import MinioBackend, iso_date_prefix


def get_iso_date() -> str:
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    return f"{now.year}-{now.month}-{now.day}"


class Image:
    """
    This is just for uploaded image
    """
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='images'))


class Poster(models.Model):
    movie = models.ForeignKey('Movie', related_name='posters', on_delete=models.CASCADE)
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='images'))


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)


class Genre(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Actor(models.Model):
    role_name = models.CharField(max_length=100)

    person = models.ForeignKey('Person', on_delete=models.CASCADE)
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
    directors = models.ManyToManyField('Person', related_name='directed_movies')
    writers = models.ManyToManyField('Person', related_name='wrote_movies')
    producers = models.ManyToManyField('Person', related_name='produced_movies')
    operators = models.ManyToManyField('Person', related_name='operated_movies')
    composers = models.ManyToManyField('Person', related_name='composed_movies')
    production_designers = models.ManyToManyField('Person', related_name='production_designed_movies')
    editors = models.ManyToManyField('Person', related_name='edited_movies')
    actors = models.ManyToManyField('Person', through='Actor', related_name='actor_in_movies')

    # User relationships
    scores = models.ManyToManyField(User, through='Score', related_name='movies_scores')

    def __str__(self):
        return self.title
