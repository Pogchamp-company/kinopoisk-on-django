import pytest

from person.models import Person


@pytest.mark.django_db
class TestPersons:
    def test_person(self):
        assert Person.objects.first() is not None
