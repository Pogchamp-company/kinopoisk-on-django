from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import LoginForm, RegisterForm, EditUserForm, EditProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm(request.POST)
    context = dict(
        form=form,
        register_form=RegisterForm()
    )

    if form.is_valid() and (user := User.objects.filter(email=form.data['email']).first()) and user.check_password(
            form.data['password']):
        login(request, user=user)
        return redirect('/')

    return render(request, 'users/index.html', context)


def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid() and not User.objects.filter(email=form.data['email']).exists():
        user = User.objects.create_user(form.data['username'],
                                        form.data['email'],
                                        form.data['password'],
                                        last_name=form.data['last_name'],
                                        first_name=form.data['first_name'],
                                        )
        user.save()
        login(request, user=user)
        return redirect('/')
    return redirect(reverse('users.login'))


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form_user = EditUserForm(data=request.POST, instance=request.user)
        form_profile = EditProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
    else:
        form_user = EditUserForm(instance=request.user)
        form_profile = EditProfileForm(instance=request.user.profile)
    context = dict(
        form_user=form_user,
        form_profile=form_profile,
    )

    if request.method == 'POST' and form_user.is_valid() and form_profile.is_valid():
        form_user.save()
        form_profile.save()
        return redirect(reverse('users.profile'))
    return render(request, 'users/profile_edit.html', context)
