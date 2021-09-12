from django.urls import path
from .views import SearchView, index, react_index

urlpatterns = [
    path('', index),
    path('react/', react_index),
    path('react/<str:page>', react_index),
    path('search/', SearchView.as_view(), name="search"),
]
