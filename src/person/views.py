from django.shortcuts import render
from .models import Person


def person_page(request, person_id: int):
    person = Person.objects.get(pk=person_id)
    context = dict(
        person=person,
        height=person.height / 100 if person.height else None,
        death='-' if not person.death else person.date_to_string(person.death)
    )
    return render(request, 'person/person.html', context)
