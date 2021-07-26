from django.shortcuts import render

from smokeshop.models import Category, Product 


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'smokeshop/product/product_list.html', context)