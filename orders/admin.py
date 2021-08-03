from django.contrib import admin

from .models import Order, OrderItem
from smokeshop.models import Product
from .service import (initial_response_for_xlsx,
                      create_report_to_xlsx_for_orders,
                      change_status_order)


class OrderItemInline(admin.TabularInline):
    model = OrderItem


def export_to_xlsx(modeladmin, request, queryset):
    """Формирования отчета по заказам в админке"""
    opts = modeladmin.model._meta
    products = Product.objects.all()
    response = initial_response_for_xlsx()
    return create_report_to_xlsx_for_orders(response, opts, products, queryset)
export_to_xlsx.short_description = 'Сформировать отчет по заказам'


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
        'transport', 'status', 'created'
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
