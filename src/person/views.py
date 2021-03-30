from django.shortcuts import render
from .models import Person


def person_page(request, person_id: int):
    person = Person.objects.get(pk=person_id)
    context = dict(
        person=person,
        height=person.height / 100 if person.height else None
    )
    return render(request, 'person.html', context)
