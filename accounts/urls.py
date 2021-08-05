from django.urls import path
from django.urls import reverse_lazy

from accounts import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'


urlpatterns = [
    # login/logout
    path('login/', views.LoginCustomerView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # смена пароля
    path('password_change/', views.ChangePasswordCustomerView.as_view(),
         name='password_change'),
    path('password_change/success/', views.CustomerPasswordChangeSuccessView.as_view(),
         name='password_change_success'),
    # регистрация
    path('registration/done/', views.create_customer_done, name='register_done'),
    path('registration/', views.CreateCustomerView.as_view(), name='registration'),
    # cброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('accounts:password_reset_done')),
        name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
