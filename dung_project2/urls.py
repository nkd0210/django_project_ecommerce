from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('book/', include('book.urlsbook')),
    path('genre/', include('book.urlsgenre')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('paying/', include('paying.urls')),
    path('shipping/', include('shipping.urls')),
    path('mobile/', include('mobile.urls')),
    path('clothes/', include('clothes.urls')),
    path('shoes/', include('shoes.urls'))
]
