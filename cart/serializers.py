from rest_framework import serializers
from .models import Cart, CartItem
from book.models import Book, Genre
from mobile.models import Mobile
from clothes.models import Clothes
from shoes.models import Shoes
from django.core.exceptions import ObjectDoesNotExist

class CartItemSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_type', 'product_id', 'quantity', 'price', 'product_info']

    def get_product_info(self, obj):
        if obj.product_type == 'book':
            try:
                book = Book.objects.get(id=obj.product_id)
                genres = [genre.name for genre in book.genre]
                return {
                    'title': book.title,
                    'author': book.author,
                    'description': book.description,
                    'cover_image': book.cover_image.url if book.cover_image else None,
                    'genre': genres
                }
            except ObjectDoesNotExist:
                return None

        elif obj.product_type == 'mobile':
            try:
                mobile = Mobile.objects.get(id=obj.product_id)
                return {
                    'type': 'mobile',
                    'brand': mobile.brand,
                    'model': mobile.model,
                    'price': float(mobile.price),
                    'stock': mobile.stock,
                    'specifications': mobile.specifications,
                    'image': mobile.image.url if mobile.image else None
                }
            except ObjectDoesNotExist:
                return None
        
        elif obj.product_type == 'clothes':
            try:
                clothes = Clothes.objects.get(id=obj.product_id)
                return {
                    'type': 'clothes',
                    'name': clothes.name,
                    'brand': clothes.brand,
                    'size': clothes.size,
                    'color': clothes.color,
                    'category': clothes.category,
                    'price': float(clothes.price),
                    'stock': clothes.stock,
                    'material': clothes.material,
                    'gender': clothes.gender,
                    'image': clothes.image.url if clothes.image else None
                }
            except ObjectDoesNotExist:
                return None
        
        elif obj.product_type == 'shoes':
            try:
                shoes = Shoes.objects.get(id=obj.product_id)
                return {
                    'type': 'shoes',
                    'brand': shoes.brand,
                    'model': shoes.model,
                    'size': shoes.size,
                    'color': shoes.color,
                    'category': shoes.category,
                    'price': float(shoes.price),
                    'stock': shoes.stock,
                    'material': shoes.material,
                    'gender': shoes.gender,
                    'image': shoes.image.url if shoes.image else None
                }
            except ObjectDoesNotExist:
                return None
                
        return obj.product_info

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'created_at', 'updated_at', 'items']
