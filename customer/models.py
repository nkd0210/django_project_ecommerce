from django.db import models
from django.contrib.auth.hashers import make_password

class CustomerType(models.Model):
    CUSTOMER_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Reduced length for password storage
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  
    customer_type = models.ForeignKey(CustomerType, on_delete=models.PROTECT)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def save(self, *args, **kwargs):
        if not self.customer_type_id:
            self.customer_type = CustomerType.objects.get(name='regular')  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class Address(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='address')  # One-to-One relationship
    house_number = models.CharField(max_length=20, blank=True, null=True)
    road = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.house_number or 'N/A'}, {self.road or 'N/A'}, {self.district or 'N/A'}, {self.city or 'N/A'}"
