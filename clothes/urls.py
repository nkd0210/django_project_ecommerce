from django.urls import path
from . import views

urlpatterns = [
    # Admin-only actions
    path('create_clothe', views.create_clothe, name='create-clothe'),
    path('update_clothe/<str:clothe_id>', views.update_clothe, name='update-clothe'),
    path('delete_clothe/<str:clothe_id>', views.delete_clothe, name='delete-clothe'),
    
    # Public actions (accessible to everyone)
    path('get_single_clothe/<str:clothe_id>', views.get_single_clothe, name='get-single-clothe'),
    path('get_all_clothes', views.get_all_clothes, name='get-all-clothes'),
]