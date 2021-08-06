from django.urls import path

from orders import views


app_name = 'orders'

urlpatterns = [
    path('created/', views.order_created_success, name='order_created'),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('admin/order/<int:order_id>/pdf/', views.get_pdf_order, name='get_pdf_order'),
    path('order/<order_id>/', views.get_order_detail, name='get_order_detail'),

]
