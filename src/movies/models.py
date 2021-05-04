from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Q, QuerySet
from django.templatetags.static import static
from django.utils.functional import cached_property

from utils.enums import ChoiceEnum
from utils.mixins import Image, ImageProperties

from person.models import PersonRole, Person


class Poster(Image):
    movie = models.ForeignKey('Movie', related_name='posters', on_delete=models.CASCADE, verbose_name='Фильм')

    class Meta:
        verbose_name = 'Постер'
        verbose_name_plural = 'Постеры'


class Score(models.Model):
    # created_at = models.DateTimeField(auto_now_add=True)

    value = models.IntegerField(validators=[MinLengthValidator(1), MaxLengthValidator(10)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)


class Genre(models.Model):
    title = models.CharField(max_length=30, verbose_name='Название')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.title


class MovieType(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'Тип Фильма'
        verbose_name_plural = 'Типы фильмов'

    def __str__(self):
        return self.title


class MovieTrailer(models.Model):
    movie = models.ForeignKey('Movie', related_name='trailers', on_delete=models.CASCADE, verbose_name='Фильм')
    link = models.URLField(verbose_name='Ссылка на трейлер (youtube)')

    class Meta:
        verbose_name = 'Трейлер'
        verbose_name_plural = 'Трейлеры'


class Movie(models.Model, ImageProperties):
    title = models.CharField(max_length=150, verbose_name='Название')
    original_title = models.CharField(max_length=150, verbose_name='Оригинальное название')
    genres = models.ManyToManyField('Genre', related_name='movies', verbose_name='Жанры')
    movie_type = models.ForeignKey('MovieType', on_delete=models.PROTECT, related_name='movies', null=True,
                                   verbose_name='Тип')
    year = models.IntegerField(validators=[MinValueValidator(1895)], verbose_name='Год выхода')
    slogan = models.CharField(max_length=500, verbose_name='Слоган')
    description = models.TextField(null=True, verbose_name='Описание')
    duration = models.DurationField(verbose_name='Продолжительность')
    budget = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Бюджет')
    premiere = models.DateField(null=True, verbose_name='Премьера (мир)')
    premiere_ru = models.DateField(null=True, verbose_name='Премьера (Россия)')

    class MpaaRate(ChoiceEnum):
        G = 'G'
        PG = 'PG'
        PG_13 = 'PG-13'
        R = 'R'
        NC_17 = 'NC-17'

    rating_mpaa = models.CharField(max_length=5, choices=MpaaRate.choices(), null=True, verbose_name='Рейтинг MPAA')
    age_rating = models.SmallIntegerField(validators=[MinValueValidator(0), MaxLengthValidator(18)], null=True,
                                          verbose_name='Возрастное ограничение')

    # User relationships
    scores = models.ManyToManyField(User, through='Score', related_name='movies_scores')

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def get_person_in_role(self, role_type: PersonRole.RoleType) -> list[Person]:
        return list(map(lambda role: role.person, self.roles.filter(role_type=role_type.name).all()))

    @cached_property
    def average_score(self):
        return round(Score.objects.filter(movie=self).aggregate(Avg('value'))['value__avg'] or 0.0, 1)

    @property
    def score_count(self):
        return Score.objects.filter(movie=self).count()

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

    @classmethod
    def get_top(cls, movie_type: MovieType = None, limit: int = None) -> QuerySet:
        q = cls.objects.annotate(avg_score=Avg('score__value')).filter(~Q(avg_score=None))
        if movie_type:
            q = q.filter(movie_type=movie_type)
        q = q.order_by('-avg_score')
        if limit:
            q = q[:limit]
        return q
