from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm, CustomerForm
from .models import Customer
from django.contrib import messages

@login_required
def profile_view(request):
    user = request.user
    orders = user.order_set.all() if hasattr(user, 'order_set') else []
    return render(request, 'customer/profile.html', {
        'user': user,
        'orders': orders
    })


@login_required
def edit_profile(request):
    customer = Customer.objects.get(user=request.user)  # वा CustomerProfile
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=customer)

    return render(request, 'customer/edit_profile.html', {
        'user_form': user_form,
        'customer_form': customer_form
    })
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect('profile')

    else:
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=customer)

    return render(request, 'customer/edit_profile.html', {
        'user_form': user_form,
        'customer_form': customer_form
    })