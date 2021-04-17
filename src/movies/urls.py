from django.urls import path
from .views import movie_page, SearchView, ScoreView, top_250

urlpatterns = [
    path('<int:movie_id>/', movie_page, name="movies.movie_page"),
    path('top250/<str:movie_type>/', top_250, name="movies.top250"),
    path('search/', SearchView.as_view(), name="movies.search"),
    path('score/<int:movie_id>/', ScoreView.as_view(), name="movies.score"),
]
