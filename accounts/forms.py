from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
        if phone == '' or (10 <= len(phone) <= 11 and phone.isdigit()):
            return phone
        raise ValidationError("Некорректный номер телефона")
