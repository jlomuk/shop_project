from cart.services.cart import Cart


def cart(request):
    """Глобальное добавление контекста продуктовой 
    корзины на все страницы проекта"""
    return {'cart': Cart(request)}
