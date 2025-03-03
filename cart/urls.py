from django.urls import path
from . import views

urlpatterns = [
    path('create_cart', views.create_cart, name='create_cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('update_item_in_cart', views.update_item_in_cart, name='update_item_in_cart'),
    path('get_customer_cart', views.get_customer_cart, name='get_customer_cart'),
    path('delete_cart/<int:customer_id>', views.delete_cart, name='delete_cart'),
    path('remove_item_in_cart', views.remove_item_in_cart, name='remove_item_in_cart'),
]
