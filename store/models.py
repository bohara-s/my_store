from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)


    def __str__(self):
        return self.name


from django.contrib.auth.models import User
from django.db import models

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)  # add this
    email = models.EmailField()                    # add this
    address = models.TextField()                    # add this
    city = models.CharField(max_length=100)        # add this
    phone = models.CharField(max_length=20)        # add this

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} by {self.full_name}'

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



from django.db import models

class PaymentInfo(models.Model):
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='payment_qr/')
    
    def __str__(self):
        return f'{self.bank_name} - {self.account_name}'
