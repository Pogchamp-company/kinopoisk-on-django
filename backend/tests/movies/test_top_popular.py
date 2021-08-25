import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from movies.models import MovieType


@pytest.mark.django_db
class TestTop250:
    def test_existing_movie(self, client):
        movie_type: MovieType = MovieType.objects.first()
        assert movie_type is not None
        response = client.get(reverse('movies.popular', kwargs=dict(movie_type=movie_type.title)))
        assertTemplateUsed(response, 'movies/top_250.html')
        assert response.status_code == 200

    def test_not_existing_movie(self, client):
        assert client.get(reverse('movies.popular', kwargs=dict(movie_type='qknwjxgnwqzuilzwqh;dn'))).status_code == 404
