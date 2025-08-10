from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order-history/', views.order_history, name='order_history'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('payment/', views.payment_info_view, name='payment_info'),
]
