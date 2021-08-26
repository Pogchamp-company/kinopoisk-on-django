import math
import random
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q

from movies.models import Movie, Score
from argparse import ArgumentParser


class Command(BaseCommand):
    help = 'Create test scores'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('--percentage', type=int, default=100, choices=range(1, 101))
        parser.add_argument('--median', type=float, default=7)
        parser.add_argument('--max_commit_count', type=int, default=1000)

    def handle(self, *args, **options):
        percentage = options['percentage']
        users = User.objects.filter(Q(username__startswith='TestUser')).all()
        users_to_score = int(len(users) / 100 * percentage)
        median: float = options['median'] - 1
        assert 0 <= median <= 9
        max_commit_count = options['max_commit_count']
        Score.objects.filter(user__username__startswith='TestUser').delete()
        program_start = time.time()
        scores = []
        for movie in Movie.objects.all():
            start = time.time()
            print(movie)
            # weights = random.choices(range(1, 11), k=10)
            weights: list = [1, 2] + [3] * 5 + [10] * 3
            if not median.is_integer():
                remains = int(median * 10) % 10
                weights[math.floor(median)] = 60 + (15 - remains * 1.5)
                weights[math.ceil(median)] = 60 + remains * 1.5
            else:
                weights[int(median)] = 135
            if movie.title == 'Комната':
                weights[9] = math.inf
            scores.extend([Score(movie=movie,
                                 user=user,
                                 value=random.choices(range(1, 11), weights, k=1)[0])
                           for user in random.choices(users, k=users_to_score)])
            if len(scores) >= max_commit_count:
                print(f'Bulk dump for {len(scores)} entries')
                Score.objects.bulk_create(scores)
                scores.clear()
            print(f'Time: {time.time() - start}')
        print(f'Score collected! Time: {time.time() - program_start}')
        Score.objects.bulk_create(scores)
        print(f'Final Time: {time.time() - program_start}')
