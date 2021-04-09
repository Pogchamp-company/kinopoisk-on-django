from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render

from users.forms import LoginForm


# from src.users.forms import LoginForm


def login_f(request):
    form = LoginForm(request.POST)
    context = dict(
        form=form
    )
    if form.is_valid():
        print('asdasdsd', form.data)
        login(request, user=User.objects.filter(email=form.data['email']).first())
        # user = User.objects.create_user(username='john',
        #                                 email=form.data['email'],
        #                                 password=form.data['password'])
        # user.save()
    else:
        print('wewerwer', request.POST, form.errors, form.__dict__)

    return render(request, 'users/index.html', context)
