from django.urls import path
from . import views

urlpatterns = [
    path('create_payment', views.create_payment, name='create_payment'),
    path('delete_payment/<int:order_id>', views.delete_payment, name='delete_payment'),
]