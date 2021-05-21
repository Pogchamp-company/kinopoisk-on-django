from django.urls import path
from .views import single_news_page

urlpatterns = [
    path('<int:news_id>/', single_news_page),
]
