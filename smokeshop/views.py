from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from smokeshop.models import Category, Product 


class ProductListView(ListView):
    """Вьюшка выводит по дефолту список всех товаров. При передачи в Get-запросе
    slug категории товара, отображает только товар выбранной категории"""
    model = Product
    template_name = 'smokeshop/product/product_list.html'
    queryset = Product.objects.all()


    def get_queryset(self, *args, **kwargs):
        qs = self.queryset
        if self.kwargs.get('category_slug'):
            qs = qs.filter(category__slug=self.kwargs['category_slug'])
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = Category.objects.all()
        request_category = Category.objects.filter(slug=self.kwargs.get('category_slug')).first
        print(request_category)
        context['categories'] = categories
        context['request_category'] = request_category
        return context

