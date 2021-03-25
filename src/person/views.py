from django.shortcuts import render
from .models import Person


def person_page(request, person_id: int):
    person = Person.objects.get(pk=person_id)
    context = dict(
        person=person
    )
    return render(request, 'person.html', context)
