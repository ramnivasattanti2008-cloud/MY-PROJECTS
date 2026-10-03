from . import views as cart_views


def cart(request):
    return {
        'cart_count': cart_views.cart_count(request),
        'cart_total': cart_views.cart_total(request)
    }
