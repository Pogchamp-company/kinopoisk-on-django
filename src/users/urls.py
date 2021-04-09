from django.urls import path

from .views import login_f

urlpatterns = [
    path('login/',  login_f, name="users.login")
]
