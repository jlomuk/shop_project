from decimal import Decimal

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.conf import settings
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required

from .models import Order
from .forms import OrderCreateForm
from .service import (calculate_transport_cost,
                      add_products_to_order_from_cart,
                      create_order_pay_action,
                      forming_report_order_to_pdf,
                      get_customer_profile, 
                      )
from .tasks import send_mail_after_create_order


class OrderCreateView(CreateView):
    """Обработчик создания заказа клиента"""
    form_class = OrderCreateForm
    model = Order
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:order_created')

    def get_context_data(self, *args, **kwargs):
        """Добавляем в контекс шаблона актуальную цену доставки из settings.
        Если пользователь прошел аутентификациюб то заполняем поля заказа из профиля"""
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            initial_data = get_customer_profile(self.request)
            context['form'] = self.form_class(initial=initial_data)
        context['transport_cost'] = Decimal(settings.TRANSPORT_COST)
        return context

    def dispatch(self, request, *args, **kwargs):
        """При обращении к обработчику с пустой корзиной поднимаем 404 статус"""
        if not request.session.get(settings.CART_ID):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """До создания инстанса модели добавляем стоимость доставки, а так же добавляем
        к заказу продукты из корзины, проводим оплату заказа, отправляем письмо и очищаем корзину. 
        записываем id заказа в сессию клиента"""
        order = form.save(commit=False)
        order.transport_cost = calculate_transport_cost(order)
        order.save()
        add_products_to_order_from_cart(self, order)
        create_order_pay_action(self.request, order)
        send_mail_after_create_order.delay(order.id)
        self.request.session['order_id'] = order.id
        return super().form_valid(form)


def order_created_success(request):
    """Обработчик для отображения информации по заказу после его успешного создания. 
    Отображается единожды после создания"""
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    del request.session['order_id']
    return render(request, 'orders/order_complete.html', {'order': order})


@staff_member_required
def get_pdf_order(request, order_id):
    """Обработчик отвечает за формирование информации по заказу в виде pdf"""
    order = get_object_or_404(Order, id=order_id)
    response = forming_report_order_to_pdf(order)
    return response
