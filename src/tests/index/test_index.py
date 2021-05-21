import json

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from movies.models import Movie


@pytest.mark.django_db
class TestIndex:
    def test_index(self, client):
        response = client.get('/')
        assertTemplateUsed(response, 'news/home_page.html')
        assert response.status_code == 200

    def test_search(self, client):
        movie = Movie.objects.first()
        response = client.get(reverse('search'), data=dict(query=movie.title[:-1]))
        assert response.status_code == 200
        json_response = json.loads(response.content)
        assert len(json_response['movies']) >= 1
        for json_movie in json_response['movies']:
            if json_movie['id'] == movie.id:
                break
        else:
            assert 0
