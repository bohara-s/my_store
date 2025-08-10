from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Order
from .models import OrderItem
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test




def home(request):
    return render(request, 'store/home.html')

def admin_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and u.is_staff
    )(view_func)
    return decorated_view_func

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('product_list')

def view_cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'store/cart.html', {'products': products})
def buy_now(request, product_id):
    # Clear existing cart
    request.session['cart'] = []

    # Add this product to cart
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('checkout')  # Checkout page URL name राख्नुहोस

@login_required
def checkout(request):
    cart = request.session.get('cart', [])  # list of product IDs

    products = Product.objects.filter(id__in=cart)

    total_price = sum(product.price for product in products)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            for product in products:
                OrderItem.objects.create(order=order, product=product, quantity=1)

            request.session['cart'] = []  # clear cart after order

            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form,
        'products': products,
        'total_price': total_price,
    })


    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    total_price = sum(product.price for product in products)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Add items to OrderItem
            for product in products:
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=1
    )

            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = total_price
            order.save()

            # Clear the cart
            request.session['cart'] = []

            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form, 'products': products, 'total_price': total_price})
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_confirmation.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

@admin_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.is_canceled = True
        order.canceled_at = timezone.now()
        order.save()
        messages.success(request, 'Order cancelled successfully.')
        return redirect('order_list')
    return render(request, 'store/cancel_order_confirm.html', {'order': order})


# store/views.py
from django.shortcuts import render
from .models import PaymentInfo

def payment_info_view(request):
    payment_info = PaymentInfo.objects.first()  # Assume one payment info only
    context = {
        'payment_info': payment_info
    }
    return render(request, 'store/payment_info.html', context)
