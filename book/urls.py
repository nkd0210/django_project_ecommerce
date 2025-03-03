from django.urls import path
from . import views

urlpatterns = [
    # Admin-only actions
    path('create-book/', views.create_book, name='create-book'),
    path('create-genre/', views.create_genre, name='create-genre'),
    path('update-book/<str:book_id>/', views.update_book, name='update-book'),
    path('update-genre/<str:genre_id>/', views.update_genre, name='update-genre'),
    path('delete-book/<str:book_id>/', views.delete_book, name='delete-book'),
    path('delete-genre/<str:genre_id>/', views.delete_genre, name='delete-genre'),
    
    # Public actions (accessible to everyone)
    path('get-single-book/<str:book_id>/', views.get_single_book, name='get-single-book'),
    path('get-single-genre/<str:genre_id>/', views.get_single_genre, name='get-single-genre'),
    path('get-all-books/', views.get_all_books, name='get-all-books'),
    path('get-all-genres/', views.get_all_genres, name='get-all-genres'),
]
