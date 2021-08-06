from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import (LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       )
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserForm, UpdateUserForm, UpdateProfileForm
from .models import Profile


class UpdateProfileCustomer(LoginRequiredMixin, UpdateView):
    """Обновляет в моделях User и Profile информацию о пользователе"""
    template_name = 'accounts/profile.html'
    form_class = UpdateUserForm
    profile_form = UpdateProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        """Возврат инстанса пользователя"""
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        """Передача двух форм в контекст шаблона"""
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.get_object())
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form(
                instance=self.get_object().profile
            )
        return context

    def post(self, request, *args, **kwargs):
        """Заполняет 2 формы данными из Post запроса. В случаи валидности этих двух форм,  
        сохраняет данные покупателя в БД. При невалидности одной из форм, 
        возвращает в шадлон обе формы с ошибками для корректировки"""
        self.object = self.get_object()
        form = self.form_class(instance=self.object,
                               data=request.POST)
        profile_form = self.profile_form(
            instance=self.object.profile, data=request.POST)
        if not form.is_valid() or not profile_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, profile_form=profile_form)
            )
        form.save()
        profile_form.save()
        messages.success(self.request, "Данные успешно обновлены")
        return HttpResponseRedirect(self.get_success_url())


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

    def form_valid(self, form, *args, **kwargs):
        """При сохранении в модели юзера, создает профиль в модели"""
        user = form.save()
        Profile.objects.create(user=user)
        return super().form_valid(form, *args, **kwargs)


def create_customer_done(request, *args, **kwargs):
    """Обработчик выводит страницу приветсвия после успешной регистрации покупателя"""
    return render(request, 'accounts/register_done.html')
