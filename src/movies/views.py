from django.http import Http404
from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Movie
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import status
from .serializers import MovieSerializer, PersonSerializer
from person.models import Person


def movie_page(request, movie_id: int):
    movie = Movie.objects.get(pk=movie_id)
    if not movie:
        raise Http404

    context = dict(
        movie=movie,
        recommendations=Movie.objects.filter(~Q(id=movie_id))[:6]
    )
    return render(request, 'movie_page.html', context)


class SearchView(APIView):
    movie_serializer_class = MovieSerializer
    person_serializer_class = PersonSerializer

    def get(self, request: Request):
        query_filter = request.GET.get('query')
        if not query_filter:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        movies = Movie.objects.filter(
            Q(title__icontains=query_filter) | Q(original_title__icontains=query_filter))
        persons = Person.objects.filter(
            Q(fullname__icontains=query_filter) | Q(ru_fullname__icontains=query_filter))

        response = {
            # 'topResult': {},
            'movies': [self.movie_serializer_class(movie).data for movie in movies],
            'persons': [self.person_serializer_class(person).data for person in persons],
            'window': render_to_string('search_result.html', dict(movies=movies, persons=persons), request),
        }

        return Response(response, status=status.HTTP_200_OK)
