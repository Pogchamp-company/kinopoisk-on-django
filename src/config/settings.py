"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import sys
from urllib.parse import urlparse
from pathlib import Path
from os import getenv
from datetime import timedelta
from typing import List, Tuple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@oowa+)%q57uxhffto99*-b+mt%63!@r&*#17mqstv&%fr9*2*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(getenv('DEBUG', False))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'rest_framework',
    'django_minio_backend',
    'ckeditor',

    'movies.apps.MoviesConfig',
    'news.apps.NewsConfig',
    'person.apps.PersonConfig',
    'users.apps.UsersConfig',
    'index.apps.IndexConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if not DEBUG:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', 'static'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

__database_info = urlparse(getenv('DATABASE_URI', 'postgresql+psycopg2://postgres@localhost:5432/KOD'))
__db_password = p.split('@')[0] if (p := __database_info.netloc.split(':')[1]) and '@' in p else None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': __database_info.path.removesuffix('/'),
        'USER': __database_info.username,
        'PASSWORD': __db_password,
        'HOST': __database_info.hostname,
        'PORT': __database_info.port,
    },
    # 'AUTOCOMMIT': False,
}

del __database_info, __db_password, p

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

IGNORE_SCORE_PERIOD = timedelta(hours=12)
MIN_SCORE_COUNT_FOR_AVERAGE = 100
MIN_SCORE_COUNT_FOR_TOP_250 = 500

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

if 'collectstatic' in sys.argv or not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_URL = '/static/'

# #################### #
# django_minio_backend #
# #################### #

dummy_policy = {"Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:GetBucketLocation",
                        "Resource": f"arn:aws:s3:::django-backend-dev-private"
                    },
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:ListBucket",
                        "Resource": f"arn:aws:s3:::django-backend-dev-private"
                    },
                    {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::django-backend-dev-private/*"
                    }
                ]}

MINIO_ENDPOINT = getenv('MINIO_ENDPOINT', '127.0.0.1:9001')
MINIO_ACCESS_KEY = getenv('MINIO_ACCESS_KEY', 'minio')
MINIO_SECRET_KEY = getenv('MINIO_SECRET_KEY', 'minio123')
MINIO_USE_HTTPS = bool(getenv('MINIO_USE_HTTPS', False))
MINIO_PRIVATE_BUCKETS = [
    'images',
    'news-images'
]
MINIO_PUBLIC_BUCKETS = [
    'avatars'
]
MINIO_URL_EXPIRY_HOURS = timedelta(days=1)  # Default is 7 days (longest) if not defined
MINIO_CONSISTENCY_CHECK_ON_START = True
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = [
    # ('django-backend-dev-private', dummy_policy)
]
LOGIN_URL = '/users/login/'

# import django_on_heroku
# django_on_heroku.settings(locals())
