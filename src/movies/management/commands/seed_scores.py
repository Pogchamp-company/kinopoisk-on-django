import math
import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q

from movies.models import Movie, Score
from argparse import ArgumentParser


class Command(BaseCommand):
    help = 'Create test scores'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--percentage', type=int, default=100)

    def handle(self, *args, **options):
        percentage = options['percentage']
        users = User.objects.filter(Q(username__startswith='TestUser')).all()
        users_to_score = int(len(users) / 100 * percentage)
        for movie in Movie.objects.all():
            print(movie)
            weights = random.choices(range(1, 11), k=10)
            if movie.title == 'Комната':
                weights[9] = math.inf
            for user in random.choices(users, k=users_to_score):
                score = Score.objects.filter(movie=movie, user=user).first()
                if not score:
                    score = Score(movie=movie,
                                  user=user)
                score.value = random.choices(range(1, 11), weights, k=1)[0]
                score.save()
