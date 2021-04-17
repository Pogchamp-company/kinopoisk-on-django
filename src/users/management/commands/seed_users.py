from argparse import ArgumentParser

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = 'Create test users'

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('users_count', type=int)

    def handle(self, *args, **options):
        users_count = options['users_count']
        user: User = User.objects.filter(Q(username__startswith='TestUser')).last()
        start = int(user.username.removeprefix('TestUser')) + 1 if user else 1
        users = []
        for i in range(start, start + users_count):
            user = User(username=f'TestUser{i}',
                        email=f'testuser{i}@app.test',
                        first_name='TestUser',
                        last_name=str(i))
            user.set_password('TestUserPassword')
            users.append(user)
        User.objects.bulk_create(users)
