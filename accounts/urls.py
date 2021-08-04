from django.urls import path

from accounts import views
from django.contrib.auth.views import LogoutView


app_name = 'accounts'


urlpatterns = [
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/done/', views.create_customer_done, name='register_done'),
    path('registration/', views.CreateCustomerView.as_view(), name='registration'),

]
