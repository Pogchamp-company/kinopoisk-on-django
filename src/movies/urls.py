from django.urls import path

from .admin import add_movie_from_kp
from .views import movie_page, ScoreView, top_250, top_popular, movie_cast

urlpatterns = [
    path('<int:movie_id>/', movie_page, name="movies.movie_page"),
    path('info/<int:movie_id>/', movie_cast, name="movies.movie_info"),
    path('top250/<str:movie_type>/', top_250, name="movies.top250"),
    path('popular/<str:movie_type>/', top_popular, name="movies.popular"),
    path('score/<int:movie_id>/', ScoreView.as_view(), name="movies.score"),
    path('add_movie_from_kp/', add_movie_from_kp, name="movies.add_movie_from_kp"),
]
