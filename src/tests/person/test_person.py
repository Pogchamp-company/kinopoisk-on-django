import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from person.models import Person


@pytest.mark.django_db
class TestPersons:
    def test_existing_person(self, client):
        person = Person.objects.first()
        assert person is not None
        response = client.get(reverse('person.person_page', kwargs=dict(person_id=person.id)))
        assertTemplateUsed(response, 'person/person.html')
        assert response.status_code == 200

    def test_not_existing_person(self, client):
        person2 = Person.objects.last()
        assert person2 is not None

        assert client.get(reverse('person.person_page', kwargs=dict(person_id=person2.id + 1))).status_code == 404
