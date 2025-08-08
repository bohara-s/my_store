from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'user']  
    inlines = [OrderItemInline]

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
