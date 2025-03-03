from django.urls import path
from . import views

urlpatterns = [
    # Admin-only actions
    path('create_shoe', views.create_shoe, name='create-shoe'),
    path('update_shoe/<str:shoe_id>', views.update_shoe, name='update-shoe'),
    path('delete_shoe/<str:shoe_id>', views.delete_shoe, name='delete-shoe'),
    
    # Public actions (accessible to everyone)
    path('get_single_shoe/<str:shoe_id>', views.get_single_shoe, name='get-single-shoe'),
    path('get_all_shoes', views.get_all_shoes, name='get-all-shoes'),
]
