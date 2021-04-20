from django.core.exceptions import ObjectDoesNotExist
from django_minio_backend import MinioBackend, iso_date_prefix

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    birth_date = models.DateField(null=True)
    photo = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='avatars'), null=True)
    # death = models.DateField(null=True, default=datetime.date.today)


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
