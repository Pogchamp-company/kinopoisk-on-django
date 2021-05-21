import pytest
from django.urls import reverse

from person.models import Person


@pytest.mark.django_db
class TestPersons:
    def test_person(self, client):
        person1 = Person.objects.first()
        person2 = Person.objects.last()
        assert person1 is not None
        assert person2 is not None

        assert client.get(reverse('person.person_page', kwargs=dict(person_id=person1.id))).status_code == 200
        assert client.get(reverse('person.person_page', kwargs=dict(person_id=person2.id + 1))).status_code == 404
