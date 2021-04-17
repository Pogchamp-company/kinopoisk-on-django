from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, ValidationError, TextInput, Form, DateField, DateInput, \
    ImageField

from .models import Profile


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
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(
                "password and confirm_password does not match"
            )


class EditForm(ModelForm):
    last_name = CharField(label='Фамилия', widget=TextInput(attrs={'class': "form__input"}), required=False)
    first_name = CharField(label='Имя', widget=TextInput(attrs={'class': "form__input"}), required=False)
    birth_date = DateField(label='Дата рождения', widget=DateInput(attrs={'class': "form__input", 'type': 'date'}), required=False)
    photo = ImageField(required=False)

    class Meta:
        model = User
        fields = ()
