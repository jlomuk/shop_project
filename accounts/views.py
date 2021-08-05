from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView)
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from .forms import UserForm


class LoginCustomerView(LoginView):
    """Обработчик отвечат за вход на сайт по учетным данным покупателя"""
    template_name = 'accounts/login.html'


class ChangePasswordCustomerView(PasswordChangeView):
    """Обработчик для смены пароля покупателя"""
    template_name = 'accounts/change_password/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_success')


class CustomerPasswordChangeSuccessView(PasswordChangeDoneView):
    """Вывод страницу после успешной смены пароля"""
    template_name = 'accounts/change_password/password_change_success.html'


class CreateCustomerView(CreateView):
    """Создания учетной записи покупателя с расширеной формой регистрации"""
    template_name = 'accounts/registration.html'
    form_class = UserForm
    success_url = reverse_lazy('accounts:register_done')


def create_customer_done(request, *args, **kwargs):
    """Обработчик выводит страницу приветсвия после успешной регистрации покупателя"""
    return render(request, 'accounts/register_done.html')
