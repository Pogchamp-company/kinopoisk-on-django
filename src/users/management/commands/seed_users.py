import time
from argparse import ArgumentParser

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = 'Create test users'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('users_count', type=int)
        parser.add_argument('--max_commit_count', type=int, default=1000)
        parser.add_argument('--progress_bar_size', type=int, default=10)

    def handle(self, *args, **options):
        users_count = options['users_count']
        max_commit_count = options['max_commit_count']
        progress_bar_size = options['progress_bar_size']
        user: User = User.objects.filter(Q(username__startswith='TestUser')).last()
        start = int(user.username.removeprefix('TestUser')) + 1 if user else 1
        users = []
        users_per_bar = users_count // progress_bar_size
        next_bar_left = users_per_bar
        program_start = time.time()

        print('Seeding progress:\n[----------]\n[', end='')
        for i in range(start, start + users_count):
            user = User(username=f'TestUser{i}',
                        email=f'testuser{i}@app.test',
                        first_name='TestUser',
                        last_name=str(i))
            user.set_password('TestUserPassword')
            users.append(user)

            if len(users) >= max_commit_count:
                User.objects.bulk_create(users)
                users.clear()

            next_bar_left -= 1
            if next_bar_left == 0:
                print('#', end='')
                next_bar_left = users_per_bar
        print(']\nFinal committing...')
        User.objects.bulk_create(users)
        print('Seeded successfully')
        print(f'Final Time: {time.time() - program_start}')
