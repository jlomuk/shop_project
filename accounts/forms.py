from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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


class UpdateUserForm(UserChangeForm):
    """Форма для обновление полей пользователя"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = kwargs.get('instance')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        customer = User.objects.filter(email=email)
        if customer.exists() and customer.last() != self.user:
            raise ValidationError("Пользователь с такой почтой уже существует")
        return email


class UpdateProfileForm(forms.ModelForm):
    """Форма для заполнения и обновление полей профиля"""
    class Meta:
        model = Profile
        fields = ('phone', 'address', 'postal_code', 'city')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not (10 <= len(phone) <= 11) or not phone.isdigit():
            raise ValidationError("Некорректный номер телефона")
        return phone
