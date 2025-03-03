from rest_framework import serializers
from mobile.models import Mobile

class MobileSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    brand = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    specifications = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(allow_null=True, required=False)

    def create(self, validated_data):
        """
        Tạo một đối tượng Mobile mới từ dữ liệu đã được xác thực.
        """
        return Mobile(**validated_data).save()

    def update(self, instance, validated_data):
        """
        Cập nhật một đối tượng Mobile với dữ liệu đã được xác thực.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
