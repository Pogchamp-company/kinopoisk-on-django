import pytest
from django.contrib.auth.models import User
from faker import Faker


@pytest.fixture
def user_factory():
    fake = Faker(locale=['en'])
    name = fake.unique.name()
    user = User.objects.create_user(username=name,
                                    email=f'{name.replace(" ", "_")}@example.example',
                                    password='TestUserPassword')

    user.save()
    return user
