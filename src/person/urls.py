from django.urls import path
from .views import person_page

urlpatterns = [
    path('<int:person_id>/',  person_page, name="person.person_page")
]
