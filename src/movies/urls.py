from django.urls import path

from .views import movie_page, SearchView

urlpatterns = [
    path('<int:movie_id>/', movie_page, name="movies.movie_page"),
    path('search/', SearchView.as_view(), name="movies.search")
]
