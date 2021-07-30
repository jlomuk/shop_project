from django.urls import path

from orders import views


app_name = 'orders'

urlpatterns = [
    path('created/', views.order_created_success, name='order_created'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),

]
