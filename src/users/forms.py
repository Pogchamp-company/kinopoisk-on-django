from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, ValidationError


class LoginForm(ModelForm):
    password = CharField(widget=PasswordInput(), label='Пароль')

    class Meta:
        model = User
        fields = ('email',)


class RegisterForm(ModelForm):
    password = CharField(widget=PasswordInput(), label='Пароль')
    confirm_password = CharField(widget=PasswordInput(), label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "password and confirm_password does not match"
            )
