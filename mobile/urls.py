from django.urls import path
from . import views

urlpatterns = [
    # Admin-only actions
    path('create_mobile', views.create_mobile, name='create-mobile'),
    path('update_mobile/<str:mobile_id>', views.update_mobile, name='update-mobile'),
    path('delete_mobile/<str:mobile_id>', views.delete_mobile, name='delete-mobile'),
    
    # Public actions (accessible to everyone)
    path('get_single_mobile/<str:mobile_id>', views.get_single_mobile, name='get-single-mobile'),
    path('get_all_mobiles', views.get_all_mobiles, name='get-all-mobiles'),
]