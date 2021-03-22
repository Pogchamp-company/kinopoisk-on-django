from django.contrib import admin
from .models import Person, Photo, PersonRole

admin.site.register(Person)
admin.site.register(Photo)
admin.site.register(PersonRole)
