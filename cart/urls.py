from django.urls import path

from cart import views


app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('delete/<int:product_id>', views.cart_delete_product, name='cart_delete_product'),
    path('', views.cart_detail, name='cart_detail'),

]
