from django.contrib import admin
from .models import Genre, Movie, MovieType, Poster

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieType)
admin.site.register(Poster)
