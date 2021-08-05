from django.contrib import admin
from django.urls import path, reverse   
from django.utils.html import format_html


from .tasks import send_mail_after_change_order
from .models import Order, OrderItem
from smokeshop.models import Product
from .service import (initial_response_for_xlsx,
                      create_report_to_xlsx_for_orders,
                      )


class OrderItemInline(admin.TabularInline):
    model = OrderItem


def order_pdf(obj):
    return format_html('<a href="{}">PDF</a>', 
        reverse('orders:get_pdf_order', args=[obj.id]))
order_pdf.short_description = "Распечатать Pdf"


def export_to_xlsx(modeladmin, request, queryset):
    """Формирования отчета по заказам в админке"""
    opts = modeladmin.model._meta
    products = Product.objects.all()
    response = initial_response_for_xlsx()
    return create_report_to_xlsx_for_orders(response, opts, products, queryset)
export_to_xlsx.short_description = 'Сформировать отчет по заказам'


def change_status_order(queryset, status):
    """функция меняет статус заказа"""
    for order in queryset:
        order.status = status
        order.save()
        send_mail_after_change_order.delay(order.id)


def make_process_status_orders(modeladmin, request, queryset):
    """функция изменяет статус заказа на 'В процессе'"""
    change_status_order(queryset, 'Processing')
make_process_status_orders.short_description = 'Установить статус в процессе'


def make_shipped_status_orders(modeladmin, request, queryset):
    """функция изменяет статус заказа на 'Отправлен'"""
    change_status_order(queryset, 'Shipped')
make_shipped_status_orders.short_description = 'Установить статус отправлен'


def make_ready_status_orders(modeladmin, request, queryset):
    """функция изменяет статус заказа на 'Готов к выдаче'"""
    change_status_order(queryset, 'Ready pickup')
make_ready_status_orders.short_description = 'Установить статус готов'


def make_completed_status_orders(modeladmin, request, queryset):
    """функция изменяет статус заказа на 'Выполнен'"""
    change_status_order(queryset, 'Completed')
make_completed_status_orders.short_description = 'Установить статус выполнен'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name',
        'email', 'address', 'city',
        'transport', 'status', 'created', order_pdf,
    )
    list_filter = ('created', 'status')
    list_editable = ('status',)
    search_fields = ('=first_name', '=last_name', '=id')
    inlines = (OrderItemInline,)
    actions = (
        export_to_xlsx, make_process_status_orders,
        make_shipped_status_orders, make_ready_status_orders, 
        make_completed_status_orders
    )
