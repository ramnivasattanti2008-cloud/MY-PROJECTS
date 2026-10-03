from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Product, Order, OrderItem


def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart_count(request):
    cart = get_cart(request)
    return sum(item['quantity'] for item in cart.values())


def cart_total(request):
    cart = get_cart(request)
    total = Decimal('0.00')
    for item in cart.values():
        total += Decimal(str(item['price'])) * item['quantity']
    return total


def product_list(request):
    products = Product.objects.filter(available=True)
    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    return render(request, 'store/product_detail.html', {'product': product})


def cart_view(request):
    cart = get_cart(request)
    items = []
    for product_id, item in cart.items():
        product = get_object_or_404(Product, pk=int(product_id))
        items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': Decimal(str(item['price'])),
            'subtotal': Decimal(str(item['price'])) * item['quantity']
        })
    total = sum(item['subtotal'] for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, available=True)
    cart = get_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {
            'quantity': quantity,
            'price': str(product.price)
        }
    save_cart(request, cart)
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')


def cart_remove(request, product_id):
    cart = get_cart(request)
    if str(product_id) in cart:
        del cart[str(product_id)]
        save_cart(request, cart)
        messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('product-list')
    if request.method == 'POST':
        cart_items = []
        total = Decimal('0.00')
        for product_id, item in cart.items():
            product = get_object_or_404(Product, pk=int(product_id))
            item_total = Decimal(str(item['price'])) * item['quantity']
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'subtotal': item_total
            })
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            postal_code=request.POST.get('postal_code'),
            total=total
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        save_cart(request, {})
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order-list')
    return render(request, 'store/checkout.html')


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})
