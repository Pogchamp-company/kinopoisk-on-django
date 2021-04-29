from django.contrib import admin
from .models import Genre, Movie, MovieType, Poster, MovieTrailer

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(MovieType)
admin.site.register(Poster)


class MovieTrailerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not form.base_fields['link'].initial:
            form.base_fields['link'].initial = 'https://www.youtube.com/embed/'
        return form


admin.site.register(MovieTrailer, MovieTrailerAdmin)
