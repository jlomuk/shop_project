from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from smokeshop.models import Category, Product
from .mixins import CategoryFilterToSlugMixin


class ProductListView(CategoryFilterToSlugMixin, ListView):
    """Вьюшка выводит по дефолту список всех товаров. При передачи в Get-запросе
    slug категории товара, отображает только товар выбранной категории"""
    model = Product
    template_name = 'smokeshop/product/product_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = Category.objects.all()
        request_category = Category.objects.filter(
            slug=self.kwargs.get('category_slug')).first
        context['categories'] = categories
        context['request_category'] = request_category
        return context


class ProductDetailView(CategoryFilterToSlugMixin, DetailView):
    """View отвечает за отрисовку детальной информации по товару"""
    model = Product
    template_name = 'smokeshop/product/detail.html'
    queryset = Product.objects.all()
    slug_url_kwarg = 'product_slug'
