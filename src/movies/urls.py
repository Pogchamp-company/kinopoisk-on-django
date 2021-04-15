from django.urls import path
from .views import movie_page, SearchView, ScoreView

urlpatterns = [
    path('<int:movie_id>/', movie_page, name="movies.movie_page"),
    path('search/', SearchView.as_view(), name="movies.search"),
    path('score/<int:movie_id>/', ScoreView.as_view(), name="movies.score"),
]
