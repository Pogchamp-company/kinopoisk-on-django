from itertools import starmap
from random import randint
from typing import TYPE_CHECKING

from django.db import models
from django.utils.functional import cached_property
from utils.enums import ChoiceEnum
from utils.mixins import Image, ImageProperties
from datetime import date, datetime
import bisect

if TYPE_CHECKING:
    from movies.models import Movie


class Photo(Image):
    person = models.ForeignKey('Person', related_name='photos', on_delete=models.CASCADE, verbose_name='Персона')

    class Meta:
        verbose_name = 'Фото персоны'
        verbose_name_plural = 'Фотографии персон'


class PersonRole(models.Model):
    class RoleType(ChoiceEnum):
        DIRECTOR = 'Режиссер'
        WRITER = 'Сценарист'
        PRODUCER = 'Продюсер'
        OPERATOR = 'Оператор'
        COMPOSER = 'Композитор'
        EDITOR = 'Монтажер'
        ACTOR = 'Актер'
        DESIGN = 'Постановщик'
        VOICE_DIRECTOR = 'Звукорежиссер'
        TRANSLATOR = 'Переводчик'

    role_name = models.CharField(max_length=1000, null=True, verbose_name='Название роли')
    role_type = models.CharField(max_length=20, choices=RoleType.choices(), verbose_name='Тип')

    person = models.ForeignKey('Person', on_delete=models.CASCADE, related_name='roles', verbose_name='Персона')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='roles', verbose_name='Фильм')

    class Meta:
        verbose_name = 'Роль в фильме'
        verbose_name_plural = 'Роли в фильмах'

    def __str__(self):
        f_role_name = f' ({self.role_name})' if self.role_name else ''
        return f'<{self.__class__.__name__} ({self.person}, ' \
               f'{getattr(self.RoleType, self.role_type).value}{f_role_name}, {self.movie})>'


class Person(models.Model, ImageProperties):
    kp_id = models.PositiveIntegerField(unique=True)
    fullname = models.CharField(max_length=150, verbose_name='Полное имя')
    ru_fullname = models.CharField(max_length=150, null=True, verbose_name='Полное имя (На русском)')

    birth_date = models.DateField(null=True, verbose_name='Дата рождения')
    death = models.DateField(null=True, verbose_name='Дата смерти')

    height = models.PositiveIntegerField(null=True, verbose_name='Рост в сантиметрах')

    class SexEnum(ChoiceEnum):
        MALE = 'Мужчина'
        FEMALE = 'Женщина'

    sex = models.CharField(max_length=6, choices=SexEnum.choices(), verbose_name='Пол')

    movies = models.ManyToManyField('movies.Movie', through='PersonRole', related_name='persons')

    class Meta:
        verbose_name = 'Персона'
        verbose_name_plural = 'Персоны'

    @property
    def movies_genres(self) -> set['Movie']:
        genres = set()
        for movie in self.movies.all():
            genres = genres.union(movie.genres.all())
        return genres

    @property
    def movies_info(self) -> str:
        query = self.movies.order_by('year')
        return f'{len(set(self.movies.all()))}, {query.first().year} - {query.last().year}'

    @cached_property
    def existing_roles(self) -> list[PersonRole.RoleType]:
        return list(filter(lambda rel_name: self.roles.filter(role_type=rel_name.name).exists(),
                           PersonRole.RoleType))

    @cached_property
    def roles_with_movies(self) -> list[tuple[PersonRole.RoleType, list['Movie']]]:
        return [(role, list(map(lambda role: role.movie, roles))) for role in PersonRole.RoleType if
                (roles := self.roles.filter(role_type=role.name).all())]

    @property
    def formatted_roles(self) -> list[str]:
        return list(starmap(lambda role_type, _: role_type.value, self.roles_with_movies))

    @property
    def age_word(self) -> str:
        last_digit_of_age = self.age % 10
        if last_digit_of_age == 1:
            return 'год'
        if 2 <= last_digit_of_age <= 4:
            return 'года'
        return 'лет'

    @cached_property
    def age(self) -> int:
        last_date = self.death if self.death else date.today()
        try:
            birthday = self.birth_date.replace(year=last_date.year)
        except ValueError:  # raised when birthdate is February 29 and the current year is not a leap year
            birthday = self.birth_date.replace(year=last_date.year, month=self.birth_date.month + 1, day=1)
        return last_date.year - self.birth_date.year - 1 if birthday > last_date else last_date.year - self.birth_date.year

    @property
    def zodiac_sign(self) -> str:
        tdays = [19, 49, 80, 110, 141, 173, 204,
                 235, 256, 296, 327, 356, 366]
        zod = ["Козерог", "Водолей", "Рыбы", "Овен",
               "Телец", "Близнецы", "Рак", "Лев",
               "Дева", "Весы", "Скорпион",
               "Стрелец", "Козерог"]
        d, m = self.birth_date.day, self.birth_date.month
        return zod[bisect.bisect_left(tdays, (datetime(2021, m, d) - datetime(2020, 12, 31)).days)]

    @staticmethod
    def date_to_string(date):
        months = ('января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря')
        return f'{date.day} {months[date.month - 1]}, {date.year}'

    @property
    def formatted_birth_date(self) -> str:
        if not self.birth_date:
            return '-'

        return f'{self.date_to_string(self.birth_date)} • {self.zodiac_sign} • {self.age} {self.age_word}'

    def __str__(self):
        return self.ru_fullname or self.fullname

    @property
    def images(self):
        return self.photos

    @property
    def default_images_folder(self) -> str:
        return 'icon/default_photos'
