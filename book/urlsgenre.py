from django.urls import path
from . import views

urlpatterns = [
    # Admin-only actions
    path('create-genre', views.create_genre, name='create-genre'),
    path('update-genre/<str:genre_id>', views.update_genre, name='update-genre'),
    path('delete-genre/<str:genre_id>', views.delete_genre, name='delete-genre'),
    
    # Public actions (accessible to everyone)
    path('get-single-genre/<str:genre_id>', views.get_single_genre, name='get-single-genre'),
    path('get-all-genres', views.get_all_genres, name='get-all-genres'),
]