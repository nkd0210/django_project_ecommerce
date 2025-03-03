from django.db import models
from order.models import Order

class Shipping(models.Model):
    order_id = models.CharField(max_length=50, null=True, blank=True)
    recipient_name = models.CharField(max_length=255)  
    recipient_phone = models.CharField(max_length=20)

    address = models.TextField()

    carrier = models.CharField(max_length=50, choices=[
        ('grab', 'Grab'),
        ('j&t', 'J&T'),
        ('ahamove', 'Ahamove'),
        ('viettelpost', 'ViettelPost')
    ], default='j&t', blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipping {self.id} - Order {self.order.id}"
