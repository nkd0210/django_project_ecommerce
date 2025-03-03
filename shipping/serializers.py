from rest_framework import serializers
from .models import Shipping

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['recipient_name', 'recipient_phone', 'address', 'carrier', 'status', 'created_at']
