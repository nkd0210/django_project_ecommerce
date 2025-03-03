from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Cart(models.Model):
    customer_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_type = models.CharField(max_length=255, null=True, blank=True) # Ví dụ: 'book', 'shoes', 'clothes'
    product_id = models.CharField(max_length=255)  # ID của sản phẩm trong bảng tương ứng
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"CartItem: {self.content_type} - {self.object_id} (Qty: {self.quantity})"
