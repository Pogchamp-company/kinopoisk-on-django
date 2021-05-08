from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Movie, Score, MovieType
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from .serializers import MovieSerializer, PersonSerializer
from person.models import Person


def movie_page(request, movie_id: int):
    movie = Movie.objects.get(pk=movie_id)
    if not movie:
        raise Http404

    recommendations = (Movie.get_top().filter(~Q(score__user=request.user))[:6]
                       if request.user.is_authenticated else None)

    context = dict(
        movie=movie,
        recommendations=recommendations,
        score=Score.objects.filter(movie=movie, user=request.user).first() if request.user.is_authenticated else 0,

    )
    return render(request, 'movies/movie_page.html', context)


def top_250(request, movie_type: str):
    try:
        movie_type = MovieType.objects.get(title=movie_type)
    except ObjectDoesNotExist:
        raise Http404()

    result = Movie.get_top(movie_type, 250)
    context = dict(
        movies=result,
        movie_type=movie_type,
        title='ТОП 250',
        description=f'Подборка лучших {movie_type.title.lower()}ов, собранная алгоритмами КиноПоиск',
    )

    return render(request, 'movies/top_250.html', context)


def top_popular(request, movie_type: str):
    try:
        movie_type = MovieType.objects.get(title=movie_type)
    except ObjectDoesNotExist:
        raise Http404()

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
        score.created_at = datetime.now()
        score.save()
        return Response({'status': 'Success'}, status.HTTP_200_OK)


class SearchView(APIView):
    movie_serializer_class = MovieSerializer
    person_serializer_class = PersonSerializer

    def get(self, request: Request):
        query_filter = request.GET.get('query')
        if not query_filter:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(
            Q(title__icontains=query_filter) | Q(original_title__icontains=query_filter))[:3]
        persons = Person.objects.filter(
            Q(fullname__icontains=query_filter) | Q(ru_fullname__icontains=query_filter))[:3]

        response = {
            # 'topResult': {},
            'movies': [self.movie_serializer_class(movie).data for movie in movies],
            'persons': [self.person_serializer_class(person).data for person in persons]
        }

        return Response(response, status=status.HTTP_200_OK)
