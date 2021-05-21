import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker


@pytest.mark.django_db
class TestUsers:
    def test_registration(self, client):
        register_url = reverse('users.register')
        fake = Faker(locale=['en'])
        name = fake.unique.name()
        latest_users_count = User.objects.count()
        register_data = dict(username=name.replace(" ", "_"),
                             email=f'{name.replace(" ", "_")}@example.example',
                             password='TestUserPassword',
                             confirm_password='TestUserPassword',
                             last_name=name.split()[0],
                             first_name=name.split()[1])

        response = client.post(register_url, data=register_data)
        assert response.status_code == 302
        assert response['Location'] == '/'
        assert User.objects.count() == latest_users_count + 1

        invalid_response = client.post(register_url, data=register_data)
        assert invalid_response.status_code == 302
        assert invalid_response['Location'] == reverse('users.login')
        assert User.objects.count() == latest_users_count + 1

    def test_login(self, client, user_factory):
        assert client.get(reverse('users.login')).status_code == 200

        user = user_factory

        assert client.post(reverse('users.login'),
                           data=dict(email=user.email, password='InvalidUserPassword')).status_code == 200
        correct_login_result = client.post(reverse('users.login'),
                                           data=dict(email=user.email, password='TestUserPassword'))
        assert correct_login_result.status_code == 302
        assert correct_login_result['Location'] == '/'

        assert client.get(reverse('users.profile')).status_code == 200

    def test_access(self, client, user_factory):
        profile_response = client.get(reverse('users.profile'))
        assert profile_response.status_code == 302
        assert profile_response['Location'] == '/users/login/?next=/users/profile/'
