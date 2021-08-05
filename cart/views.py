from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from cart.services.cart import Cart
from smokeshop.models import Product
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    """Обработчик для добавления товара в корзину и изменения его количества в корзине"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


@require_POST
def cart_delete_product(request, product_id):
    """Обработчик для удаления товара из корзины"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    """Обработчик для полной очистки корзины"""
    cart = Cart(request)
    cart.clear()
    return redirect('smokeshop:product_list')


def cart_detail(request):
    """Обработчик для отображения продуктовой корзины"""
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], })
    return render(request, 'cart/detail.html')
