from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from movies.models import Movie
from movies.serializers import MovieSerializer
from news.models import News
from person.models import Person
from person.serializers import PersonSerializer


def index(request):
    context = dict(
        preview=Movie.objects.order_by("-id")[:3],
        news=News.objects.order_by("-id")[:3]
    )

    return render(request, 'index/home_page.html', context)


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
