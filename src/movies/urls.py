from django.urls import path
from .views import movie_page, SearchView, person_page

urlpatterns = [
    path('<int:movie_id>/', movie_page, name="movies.movie_page"),
    path('search/', SearchView.as_view(), name="movies.search"),
    path('p/<int:person_id>/', person_page, name="person.person_page")
]
