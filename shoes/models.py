from mongoengine import Document, StringField, DecimalField, IntField, ImageField, DateTimeField
from django.db import models
from django.core.files.storage import default_storage
from datetime import datetime

class Shoes(Document):

    meta = {'db_alias': 'shoes_db'}
    
    brand = StringField(max_length=100, required=True)
    model = StringField(max_length=100, required=True, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = IntField(required=True)
    size = StringField(max_length=10, required=True)
    color = StringField(max_length=50)
    category = StringField(max_length=100)
    material = StringField(max_length=100, required=False)
    gender = StringField(max_length=10, required=False)
    image = ImageField(upload_to='shoes/', required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.size} - {self.color}"
