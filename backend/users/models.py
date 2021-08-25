from django.core.exceptions import ObjectDoesNotExist
from django_minio_backend import MinioBackend, iso_date_prefix

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')

    birth_date = models.DateField(null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='avatars'), null=True,
                              verbose_name='Аватар')

    class Meta:
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профили пользователей'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    try:
        instance.profile
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
