from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

from .models import Profile

class UserForm(UserCreationForm):
    """Расширенная форма регистрации пользователя"""
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError("Пользователь с такой почтой уже существует")
        return email


class UpdateUserForm(forms.ModelForm):
    """Форма для обновление полей пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UpdateProfileForm(forms.ModelForm):
    """Форма для заполнения и обновление полей профиля"""
    class Meta:
        model = Profile
        fields = ('phone', 'address', 'postal_code', 'city')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) > 11:
            raise ValidationError("Некорректный номер телефона")
        return phone
