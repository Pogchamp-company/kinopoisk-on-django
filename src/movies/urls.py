from django.urls import path
from .views import movie_page, SearchView, ScoreView, top_250, top_popular, movie_info

urlpatterns = [
    path('<int:movie_id>/', movie_page, name="movies.movie_page"),
    path('info/<int:movie_id>/', movie_info, name="movies.movie_info"),
    path('top250/<str:movie_type>/', top_250, name="movies.top250"),
    path('popular/<str:movie_type>/', top_popular, name="movies.popular"),
    path('search/', SearchView.as_view(), name="movies.search"),
    path('score/<int:movie_id>/', ScoreView.as_view(), name="movies.score"),
]
