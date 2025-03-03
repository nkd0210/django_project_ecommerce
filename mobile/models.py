from mongoengine import Document, StringField, DateField, ListField, ReferenceField, IntField, DecimalField, ImageField
from django.db import models
from django.core.files.storage import default_storage

class Mobile(Document):

    meta = {'db_alias': 'mobile_db'}
    
    brand = StringField(max_length=100, required=True)
    model = StringField(max_length=100, required=True, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2)
    stock = IntField(required=True)
    specifications = StringField()
    image = ImageField(upload_to='mobile/', required=False)

    def __str__(self):
        return f"{self.brand} {self.model}"
