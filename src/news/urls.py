from django.contrib import admin
from django.urls import path

from src.news.views import index

urlpatterns = [
    path('', index),
]
