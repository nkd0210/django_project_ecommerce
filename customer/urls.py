from django.urls import path
from . import views

app_name='customer'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('getCustomer', views.getCustomer, name='get_customer'),
    path('updateCustomer', views.updateCustomer, name='update_customer'),
    path('deleteAccount', views.deleteAccount, name='delete_customer'),
    path('getAllCustomers', views.getAllCustomers, name='get_all_customers'),
    path('updateCustomerForAdmin/<int:customer_id>', views.updateCustomerForAdmin, name='admin_update_customer')
]
