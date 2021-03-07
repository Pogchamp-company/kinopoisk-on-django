from django.db import models
from utils.mixins import Image


class Photo(Image):
    person = models.ForeignKey('Person', related_name='photos', on_delete=models.CASCADE)


class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=100)

    birth_date = models.DateField()

    @property
    def fullname(self):
        return f'{self.name} {self.surname}'

    def __str__(self):
        return self.fullname
