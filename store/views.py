from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Order
from .models import OrderItem
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'store/home.html')

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

def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total_price = sum(product.price for product in products)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_price = total_price
            order.save()

            for product in products:
                OrderItem.objects.create(order=order, product=product, quantity=1)

            request.session['cart'] = []
            return redirect('order_confirmation', order_id=order.id)
        else:
            # form invalid - don't use 'order' here
            pass
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form, 'products': products, 'total_price': total_price})

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

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
    return redirect('order_history')



@login_required
def payment_info(request):
    # Store account details hardcoded or from settings
    context = {
        'account_name': 'My Store Pvt. Ltd.',
        'account_number': '1234567890',
        'bank_name': 'Nepal Bank Ltd.',
        'qr_code_url': '/static/img/payment-qr.png',  # QR image file path in static folder
    }
    return render(request, 'store/payment_info.html', context)