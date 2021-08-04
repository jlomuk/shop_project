from django.urls import path

from accounts import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'


urlpatterns = [
    path('login/', views.LoginCustomerView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.ChangePasswordCustomerView.as_view(),
         name='password_change'),
    path('password_change/success/', views.CustomerPasswordChangeSuccessView.as_view(),
         name='password_change_success'),
    path('registration/done/', views.create_customer_done, name='register_done'),
    path('registration/', views.CreateCustomerView.as_view(), name='registration'),

]
