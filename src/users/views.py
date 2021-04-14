from pprint import pprint

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import LoginForm, RegisterForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm(request.POST)
    context = dict(
        form=form,
        register_form=RegisterForm()
    )

    if form.is_valid() and (user := User.objects.filter(email=form.data['email']).first()) and user.check_password(form.data['password']):
        login(request, user=user)
        return redirect('/')

    return render(request, 'users/index.html', context)


def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid() and not User.objects.filter(email=form.data['email']).exists():
        user = User.objects.create_user(username=form.data['username'],
                                        email=form.data['email'],
                                        last_name=form.data['last_name'],
                                        first_name=form.data['first_name'],
                                        )
        user.set_password(form.data['password'])
        user.save()
        login(request, user=user)
        return redirect('/')
    return redirect(reverse('users.login'))


def profile(request):
    return render(request, 'users/profile.html')
