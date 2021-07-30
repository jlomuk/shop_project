from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


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
