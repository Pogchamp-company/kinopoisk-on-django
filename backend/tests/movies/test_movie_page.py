import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from movies.models import Movie


@pytest.mark.django_db
class TestMoviePage:
    def test_existing_movie(self, client):
        movie = Movie.objects.first()
        assert movie is not None
        response = client.get(reverse('movies.movie_page', kwargs=dict(movie_id=movie.id)))
        assertTemplateUsed(response, 'movies/movie_page.html')
        assert response.status_code == 200

    def test_not_existing_movie(self, client):
        movie = Movie.objects.last()
        assert movie is not None

        assert client.get(reverse('movies.movie_page', kwargs=dict(movie_id=movie.id + 1))).status_code == 404
