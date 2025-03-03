from django.urls import path
from . import views

urlpatterns = [
    path('create_order', views.create_order, name='create_order'),
    path('get_customer_orders', views.get_customer_orders, name='get_customer_orders'),
    path('delete_order/<int:order_id>', views.delete_order, name='delete_order'),
    path('get_order_by_id/<int:order_id>', views.get_order_by_id, name='get_order_by_id'),
    path('update_order/<int:order_id>', views.update_order, name='update_order'),
    path('get_all_orders', views.get_all_orders, name='get_all_orders')
]