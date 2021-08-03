from django.contrib import admin

from .models import Order, OrderItem
from smokeshop.models import Product
from .service import initial_response_for_xlsx, create_report_to_xlsx_for_orders


class OrderItemInline(admin.TabularInline):
    model = OrderItem


def export_to_xlsx(modeladmin, request, queryset):
    """Формирования отчета по заказам в админке"""
    opts = modeladmin.model._meta
    products = Product.objects.all()
    response = initial_response_for_xlsx()
    return create_report_to_xlsx_for_orders(response, opts, products, queryset)
export_to_xlsx.short_description = 'Export to XLSX'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name',
        'email', 'address', 'city',
        'transport', 'status', 'created'
    )
    list_filter = ('created',)
    list_editable = ('status',)
    search_fields = ('=first_name', '=last_name', '=id')
    inlines = (OrderItemInline,)
    actions = (export_to_xlsx, )
