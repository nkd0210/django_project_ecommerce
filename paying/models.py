from django.db import models
from order.models import Order

class Payment(models.Model):
    order_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cod', 'Cash on Delivery')
    ], default='cod')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - Order {self.order.id}"
