from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    password = CharField(widget=PasswordInput())
