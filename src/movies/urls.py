from django.urls import path

from .views import movie_page

urlpatterns = [
    path('<int:movie_id>/', movie_page),
]
