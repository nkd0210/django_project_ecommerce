from rest_framework import serializers
from .models import Order, OrderItem
from book.models import Book
from paying.models import Payment
from shipping.models import Shipping
from mobile.models import Mobile
from paying.serializers import PaymentSerializer
from shipping.serializers import ShippingSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_type', 'product_id', 'quantity', 'price', 'product_info']
    
    def get_product_info(self, obj):
        if obj.product_type == 'book':
            try:
                book = Book.objects.get(id=obj.product_id)
                return {
                    'title': book.title,
                    'author': book.author,
                    'description': book.description,
                    'cover_image': book.cover_image.url if book.cover_image else None,
                }
            except Book.DoesNotExist:
                return None

        elif obj.product_type == 'mobile':
            try:
                mobile = Mobile.objects.get(id=obj.product_id)
                return {
                    'brand': mobile.brand,
                    'model': mobile.model,
                    'specifications': mobile.specifications,
                    'image': mobile.image.url if mobile.image else None
                }
            except Mobile.DoesNotExist:
                return None

        return None

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'method', 'created_at']

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['recipient_name', 'recipient_phone', 'address', 'carrier', 'status', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Trả về danh sách OrderItem
    payment = PaymentSerializer(read_only=True)  # Thông tin thanh toán
    shipping = ShippingSerializer(read_only=True) # Thông tin vận chuyển

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'total_price', 'status', 'is_paid', 'created_at', 'updated_at', 'items', 'payment', 'shipping']
