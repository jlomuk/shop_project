from django.urls import path

from smokeshop import views 


app_name = 'smokeshop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
]