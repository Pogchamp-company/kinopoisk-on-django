import pytest
from django.contrib.auth.models import User
from faker import Faker
from news.models import News


@pytest.fixture
def user_factory():
    fake = Faker(locale=['en'])
    name = fake.unique.name()
    user = User.objects.create_user(username=name,
                                    email=f'{name.replace(" ", "_")}@example.example',
                                    password='TestUserPassword')

    user.save()
    return user


@pytest.fixture
def news_factory():
    fake = Faker(locale=['en'])
    title = fake.name()
    preview_content = fake.name()
    content = f'{title}\n{preview_content}'
    news = News(title=title,
                preview_content=preview_content,
                content=content)
    news.save()
    return news
