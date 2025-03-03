from rest_framework import serializers
from clothes.models import Clothes

class ClothesSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    size = serializers.CharField(max_length=10)
    color = serializers.CharField(max_length=50)
    category = serializers.CharField(max_length=100)
    brand = serializers.CharField(max_length=100, required=False, allow_blank=True)
    material = serializers.CharField(max_length=100, required=False, allow_blank=True)
    gender = serializers.CharField(max_length=10)
    image = serializers.ImageField(allow_null=True, required=False)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def create(self, validated_data):
        """
        Tạo một đối tượng Clothes mới từ dữ liệu đã được xác thực.
        """
        return Clothes(**validated_data).save()

    def update(self, instance, validated_data):
        """
        Cập nhật một đối tượng Clothes với dữ liệu đã được xác thực.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S") if obj.created_at else None

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M:%S") if obj.updated_at else None