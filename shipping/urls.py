from django.urls import path
from . import views

urlpatterns = [
    path('create_shipping', views.create_shipping, name='create_shipping'),
    path('delete_shipping/<int:order_id>', views.delete_shipping, name='delete_shipping')
]