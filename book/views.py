import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Book, Genre
from .serializers import GenreSerializer, BookSerializer, GenreListSerializer
from django.core.exceptions import PermissionDenied
from mongoengine import DoesNotExist

CUSTOMER_SERVICE_URL = "http://localhost:8000/customer"

def is_admin(request):
    try:
        response = requests.get(f"{CUSTOMER_SERVICE_URL}/getCustomer", cookies=request.COOKIES)
        if response.status_code != 200:
            return False  

        customer_data = response.json()
        return customer_data.get("customer_type", "").lower() == "admin"

    except Exception as e:
        print(f"Error in is_admin: {e}")
        return False

@api_view(['POST'])
def create_book(request):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()  # Save the book to MongoDB
        return Response({"message": "Book created successfully!", "book": serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def create_genre(request):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    genre_name = request.data.get('name')
    if not genre_name:
        return Response({"error": "Genre name is required."}, status=400)

    genre = Genre(name=genre_name)
    genre.save()  # Save the genre to MongoDB
    return Response({"message": "Genre created successfully!", "genre": genre.name}, status=201)

@api_view(['PUT'])
def update_book(request, book_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    book = Book.objects.get(id=book_id)
    serializer = BookSerializer(book, data=request.data, partial=True)  # Partial update allowed
    if serializer.is_valid():
        book = serializer.save()
        return Response({"message": "Book updated successfully!", "book": serializer.data}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def update_genre(request, genre_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    genre = Genre.objects.get(id=genre_id)
    genre_name = request.data.get('name')
    if not genre_name:
        return Response({"error": "Genre name is required."}, status=400)
    
    genre.name = genre_name
    genre.save()
    return Response({"message": "Genre updated successfully!", "genre": genre.name}, status=200)

@api_view(['DELETE'])
def delete_book(request, book_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    book = Book.objects.get(id=book_id)

    if book.cover_image and book.cover_image.grid_id:
        book.cover_image.delete()

    book.delete()  # Delete the book from MongoDB
    return Response({"message": f"Book {book_id} deleted successfully!"}, status=204)

@api_view(['DELETE'])
def delete_genre(request, genre_id):
    if not is_admin(request):
        raise PermissionDenied("You do not have permission to perform this action.")
    
    genre = Genre.objects.get(id=genre_id)
    genre.delete()  # Delete the genre from MongoDB
    return Response({"message": f"Genre {genre_id} deleted successfully!"}, status=204)

@api_view(['GET'])
def get_single_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=200)

    except DoesNotExist:
        return Response({"error": "Book not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_single_genre(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    serializer = GenreListSerializer(genre)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_all_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def get_all_genres(request):
    genres = Genre.objects.all()
    serializer = GenreListSerializer(genres, many=True)
    return Response(serializer.data, status=200)