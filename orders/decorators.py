from django.shortcuts import render, get_object_or_404
from django.http import Http404

from .models import Order


def permission_to_order_owner_or_admin(func):
    def wrapper(request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs.get('order_id'))
        if order.user != request.user and not request.user.is_superuser:
            raise Http404
        return func(request, *args, **kwargs)
    return wrapper
