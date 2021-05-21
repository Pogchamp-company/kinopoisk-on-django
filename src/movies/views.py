from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from person.models import PersonRole
from .models import Movie, Score, MovieType


def movie_page(request, movie_id: int):
    movie = get_object_or_404(Movie, pk=movie_id)

    recommendations = (Movie.get_top().filter(~Q(score__user=request.user))[:6]
                       if request.user.is_authenticated else None)

    context = dict(
        movie=movie,
        recommendations=recommendations,
        score=Score.objects.filter(movie=movie, user=request.user).first() if request.user.is_authenticated else 0,
        directors=movie.get_person_in_role(PersonRole.RoleType.DIRECTOR, 3),
        producers=movie.get_person_in_role(PersonRole.RoleType.PRODUCER, 3),
        writers=movie.get_person_in_role(PersonRole.RoleType.WRITER, 3),
    )
    return render(request, 'movies/movie_page.html', context)


def movie_cast(request, movie_id: int):
    movie = get_object_or_404(Movie, pk=movie_id)

    context = dict(
        movie=movie,
    )
    return render(request, 'movies/movie_cast.html', context)


def top_250(request, movie_type: str):
    movie_type = get_object_or_404(MovieType, title=movie_type)

    result = Movie.get_top(movie_type, 250)
    context = dict(
        movies=result,
        movie_type=movie_type,
        title='ТОП 250',
        description=f'Подборка лучших {movie_type.title.lower()}ов, собранная алгоритмами КиноПоиск',
    )

    return render(request, 'movies/top_250.html', context)


def top_popular(request, movie_type: str):
    movie_type = get_object_or_404(MovieType, title=movie_type)

    result = Movie.get_popular(movie_type, 250)
    context = dict(
        movies=result,
        movie_type=movie_type,
        title=f'Популярные {movie_type.title.lower()}ы',
        description=f'Подборка популярных {movie_type.title.lower()}ов',
    )

    return render(request, 'movies/top_250.html', context)


class ScoreView(APIView):
    def put(self, request: Request, movie_id: int):
        score_value = int(request.GET['score'])
        if request.user.is_anonymous:
            return Response({'message': 'Login required'}, status=status.HTTP_403_FORBIDDEN)
        movie = Movie.objects.get(pk=movie_id)
        if not movie:
            return Response({'message': 'Movie not found'}, status.HTTP_404_NOT_FOUND)
        score = Score.objects.filter(movie=movie, user=request.user).first()
        if not score:
            score = Score(movie=movie,
                          user=request.user)
        score.value = score_value
        score.save()
        return Response({'status': 'Success'}, status.HTTP_200_OK)
