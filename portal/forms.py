from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(
        label='Фамилия Имя Отчество',
        widget=forms.TextInput(
           attrs={'placeholder': 'Введите ФИО',}
           )
        )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(
           attrs={'placeholder': 'Введите e-mail'}
            )
        )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите пароль'}
            )
        )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Подтвердите пароль'}
            )
        )
    
    error_messages = {
        'password_mismatch': 'Пароли не совпадают',
    }
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Эта почта существует в платформе')
        return email

    class Meta:
        model = User
        fields=['full_name', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(
           attrs={'placeholder': 'Введите e-mail'}
        )
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Введите пароль'}
        )
    )