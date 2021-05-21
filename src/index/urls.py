from django.urls import path
from .views import SearchView, index

urlpatterns = [
    path('', index),
    path('search/', SearchView.as_view(), name="search"),
]
