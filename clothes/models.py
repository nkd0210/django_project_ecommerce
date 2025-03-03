from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField, DecimalField, ImageField
from django.db import models
from django.core.files.storage import default_storage
from datetime import datetime

class Clothes(Document):

    meta = {'db_alias': 'clothes_db'}
    
    name = StringField(max_length=255, required=True)
    description = StringField()
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = IntField(required=True)
    size = StringField(max_length=10)
    color = StringField(max_length=50)
    category = StringField(max_length=100)
    brand = StringField(max_length=100)
    material = StringField(max_length=100)
    gender = StringField(max_length=10)
    image = ImageField(upload_to='clothes/', required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.size} - {self.color}"
