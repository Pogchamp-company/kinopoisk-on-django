from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import login_view, register

urlpatterns = [
    path('login/', login_view, name="users.login"),
    path('logout/', LogoutView.as_view(next_page='/'), name="users.logout"),
    path('register/', register, name="users.register")
]
