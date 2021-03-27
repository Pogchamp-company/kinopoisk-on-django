from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.templatetags.static import static

from utils.enums import ChoiceEnum
from utils.mixins import Image, ImageProperties

from person.models import PersonRole, Person


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


class MovieType(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Movie(models.Model, ImageProperties):
    title = models.CharField(max_length=150)
    original_title = models.CharField(max_length=150)
    genres = models.ManyToManyField('Genre', related_name='movies')
    movie_type = models.ForeignKey('MovieType', on_delete=models.PROTECT, related_name='movies', null=True)
    year = models.IntegerField(validators=[MinValueValidator(1895)])
    slogan = models.CharField(max_length=500)
    description = models.TextField(null=True)
    duration = models.DurationField()
    budget = models.IntegerField(validators=[MinValueValidator(0)])
    premiere = models.DateField(null=True)
    premiere_ru = models.DateField(null=True)

    class MpaaRate(ChoiceEnum):
        G = 'G'
        PG = 'PG'
        PG_13 = 'PG-13'
        R = 'R'
        NC_17 = 'NC-17'

    rating_mpaa = models.CharField(max_length=5, choices=MpaaRate.choices(), null=True)
    age_rating = models.SmallIntegerField(validators=[MinValueValidator(0), MaxLengthValidator(18)], null=True)

    # User relationships
    scores = models.ManyToManyField(User, through='Score', related_name='movies_scores')

    def get_person_in_role(self, role_type: PersonRole.RoleType) -> list[Person]:
        return list(map(lambda role: role.person, self.roles.filter(role_type=role_type.name).all()))

    @property
    def directors(self) -> list[Person]:
        return self.get_person_in_role(PersonRole.RoleType.DIRECTOR)

    @property
    def producers(self) -> list[Person]:
        return self.get_person_in_role(PersonRole.RoleType.PRODUCER)

    @property
    def writers(self) -> list[Person]:
        return self.get_person_in_role(PersonRole.RoleType.WRITER)

    @property
    def actors(self) -> list[PersonRole]:
        return self.roles.filter(role_type=PersonRole.RoleType.ACTOR.name).all()

    def __str__(self):
        return self.title

    @property
    def first_poster_url(self):
        poster = self.posters.first()
        if not poster:
            return static('icon/default_poster.webp')
        return poster.image.url

    @property
    def images(self):
        return self.posters

    @property
    def default_images_folder(self) -> str:
        return 'icon/default_posters'
