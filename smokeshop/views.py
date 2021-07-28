from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse

from smokeshop.models import Category, Product, Feedback
from .mixins import CategoryFilterToSlugMixin
from .forms import FeedbackForm


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


class ProductDetailView(FormMixin, CategoryFilterToSlugMixin, DetailView):
    """
    View отвечает за отрисовку детальной информации по товару, а также за обработку формы 
    и создания записи комментария в базу данных.
    """
    model = Product
    template_name = 'smokeshop/product/detail.html'
    queryset = Product.objects.all()
    slug_url_kwarg = 'product_slug'
    form_class = FeedbackForm

    def get_success_url(self):
        return reverse('smokeshop:product_detail',
                       args=[self.object.category.slug, self.object.slug])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.product = self.object
        comment.save()   
        return super().form_valid(form)
