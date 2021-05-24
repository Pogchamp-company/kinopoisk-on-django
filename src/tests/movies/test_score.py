from random import randint

import pytest
from django.urls import reverse
from movies.models import Movie, Score


@pytest.mark.django_db
class TestMoviePage:
    def test_success_create_score(self, client, user_factory):
        score_val = randint(1, 10)
        movie = Movie.objects.first()
        user = user_factory

        client.force_login(user)

        response = client.put(f"{reverse('movies.score', kwargs=dict(movie_id=movie.id))}?score={score_val}")
        assert response.status_code == 200
        assert response.json()['status'] == 'Success'
        assert Score.objects.filter(movie=movie, user=user, value=score_val).first()

    def test_success_update_score(self, client):
        score_val = randint(1, 10)

        score = Score.objects.first()
        movie = score.movie
        user = score.user

        client.force_login(user)

        response = client.put(f"{reverse('movies.score', kwargs=dict(movie_id=movie.id))}?score={score_val}")
        assert response.status_code == 200
        assert response.json()['status'] == 'Success'
        assert Score.objects.filter(movie=movie, user=user, value=score_val).first()

    def test_forbidden_create_score(self, client):
        score_val = randint(1, 10)
        movie = Movie.objects.first()
        response = client.put(f"{reverse('movies.score', kwargs=dict(movie_id=movie.id))}?score={score_val}")
        assert response.status_code == 403
        assert response.json()['status'] == 'Failed'

    def test_movie_not_found(self, client, user_factory):
        score_val = randint(1, 10)
        movie = Movie.objects.last()
        user = user_factory
        client.force_login(user)
        response = client.put(f"{reverse('movies.score', kwargs=dict(movie_id=movie.id + 1))}?score={score_val}")
        assert response.status_code == 404
        assert response.json()['status'] == 'Failed'

    def test_with_incorrect_score(self, client, user_factory):
        score_val = 'aboba'
        movie = Movie.objects.first()
        user = user_factory
        client.force_login(user)
        response = client.put(f"{reverse('movies.score', kwargs=dict(movie_id=movie.id))}?score={score_val}")
        assert response.status_code == 400
