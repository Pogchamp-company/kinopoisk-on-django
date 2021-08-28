import sys
from os import getenv

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .management.commands.add_kp_movie import Command
from .models import Genre, Movie, MovieType, Poster, MovieTrailer

admin.site.register(Genre)
admin.site.register(Movie, change_list_template="admin/movie_change_list.html")
admin.site.register(MovieType)
admin.site.register(Poster)


class MovieTrailerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not form.base_fields['link'].initial:
            form.base_fields['link'].initial = 'https://www.youtube.com/embed/'
        return form


admin.site.register(MovieTrailer, MovieTrailerAdmin)


def add_movie_from_kp(request):
    kp_id = request.POST.get('kp_id')
    print(kp_id)
    if not request.user.is_superuser:
        return 'мудила'

    c = Command()
    c.f(int(kp_id), getenv('KP_API_KEY'))

    return redirect('/admin/movies/movie/')
