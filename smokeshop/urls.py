from django.urls import path

from smokeshop import views 


app_name = 'smokeshop'

urlpatterns = [
    path('<slug:category_slug>/', views.ProductListView.as_view(), 
                            name='product_list_by_category'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('', views.ProductListView.as_view(), name='product_list'),
    
]