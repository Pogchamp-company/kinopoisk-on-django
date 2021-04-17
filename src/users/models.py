from django_minio_backend import MinioBackend, iso_date_prefix

from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfilePhoto(models.Model):
    image = models.ImageField(upload_to=iso_date_prefix, storage=MinioBackend(bucket_name='avatars'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    birth_date = models.DateField(null=True)
    photo = models.OneToOneField(ProfilePhoto, on_delete=models.CASCADE, null=True)
    # death = models.DateField(null=True, default=datetime.date.today)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not instance.profile:
        instance.profile = Profile()

    instance.profile.save()
