from django.urls import path
from . import views

urlpatterns = [
    # Admin-only actions
    path('create-book', views.create_book, name='create-book'),
    path('update-book/<str:book_id>', views.update_book, name='update-book'),
    path('delete-book/<str:book_id>', views.delete_book, name='delete-book'),
    
    # Public actions (accessible to everyone)
    path('get-single-book/<str:book_id>', views.get_single_book, name='get-single-book'),
    path('get-all-books', views.get_all_books, name='get-all-books'),
]