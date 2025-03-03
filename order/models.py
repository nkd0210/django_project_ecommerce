from django.db import models

class Order(models.Model):
    customer_id = models.IntegerField()  # ID khách hàng từ MySQL
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - Customer {self.customer_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    
    # Thay vì dùng ContentType, ta sẽ lưu trực tiếp loại sản phẩm và ID
    product_type = models.CharField(max_length=255)  # Loại sản phẩm (book, shoes, clothes)
    product_id = models.CharField(max_length=255)  # ID sản phẩm trong MongoDB
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá của sản phẩm tại thời điểm đặt hàng

    def __str__(self):
        return f"OrderItem {self.id} - Order {self.order.id} - {self.product_type} ({self.product_id})"