from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from django.http import Http404

from .models import Order
from .forms import OrderCreateForm
from .servive import calculate_transport_cost, add_products_to_order_from_cart


class OrderCreateView(CreateView):
    """Обработчик создания заказа клиента"""
    form_class = OrderCreateForm
    model = Order
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:order_created')

    def get_context_data(self, *args, **kwargs):
        """Добавляем в контекс шаблона актуальную цену доставки из settings"""
        context = super().get_context_data(*args, **kwargs)
        context['transport_cost'] = Decimal(settings.TRANSPORT_COST)
        return context

    def dispatch(self, request, *args, **kwargs):
        """При обращении к обработчику с пустой корзиной поднимаем 404 статус"""
        if not request.session.get(settings.CART_ID):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """До создания инстанса модели добавляем стоимость доставки, а так же добавляем
        к заказу продукты из корзины, очищаем корзину и
        записываем id заказа в сессию клиента"""
        order = form.save(commit=False)
        order.transport_cost = calculate_transport_cost(order)
        order.save()
        add_products_to_order_from_cart(self, order)
        self.request.session['order_id'] = order.id
        return super().form_valid(form)


def order_created_success(request):
    """Обработчик для отображения информации по заказу после его успешного создания. 
    Отображается единожды после создания"""
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    del request.session['order_id']
    return render(request, 'orders/order_complete.html', {'order': order})
