from django.http import Http404
from django.shortcuts import render
from .models import Movie


def movie_page(request, movie_id: int):
    movie = Movie.objects.get(pk=movie_id)
    if not movie:
        raise Http404

    context = dict(
        movie=movie
    )
    return render(request, 'movie_page.html', context)
