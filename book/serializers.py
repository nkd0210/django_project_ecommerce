from rest_framework import serializers
from .models import Book, Genre

class GenreListSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField(max_length=100)

class GenreSerializer(serializers.Serializer):
    id = serializers.CharField()

class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=100)
    genre = serializers.ListField(child=serializers.CharField())
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    publish_date = serializers.DateField()  
    description = serializers.CharField()
    stock = serializers.IntegerField(min_value=0)
    cover_image = serializers.ImageField(allow_null=True, required=False)

    def create(self, validated_data):
        genres_ids = validated_data.pop('genre')
        book = Book(**validated_data)
        book.save()
        
        # Fetch genres by their IDs and associate them with the book
        for genre_id in genres_ids:
            try:
                genre = Genre.objects.get(id=genre_id)
                book.genre.append(genre)
            except Genre.DoesNotExist:
                raise serializers.ValidationError(f"Genre with id {genre_id} does not exist")
        
        book.save()
        return book

    def update(self, instance, validated_data):
        # Update genre field if provided
        if 'genre' in validated_data:
            genres_ids = validated_data.pop('genre')
            instance.genre = []  # Clear existing genres
            for genre_id in genres_ids:
                try:
                    genre = Genre.objects.get(id=genre_id)
                    instance.genre.append(genre)
                except Genre.DoesNotExist:
                    raise serializers.ValidationError(f"Genre with id {genre_id} does not exist")

        # Update other fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Custom representation of the book instance
        """
        return {
            'id': str(instance.id),
            'title': instance.title,
            'author': instance.author,
            'genre': [str(genre.id) for genre in instance.genre],
            'price': float(instance.price),
            'publish_date': instance.publish_date.isoformat() if instance.publish_date else None,
            'description': instance.description,
            'stock': instance.stock,
            'cover_image': instance.cover_image.url if instance.cover_image else None
        }