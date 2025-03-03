from mongoengine import Document, StringField, DateField, ListField, ReferenceField, IntField, DecimalField, ImageField
from django.db import models
from django.core.files.storage import default_storage

class Genre(Document):
    meta = {'db_alias': 'book_db'}
    name = StringField(unique=True)

    def __str__(self):
        return self.name

class Book(Document):
    meta = {'db_alias': 'book_db'}
    title = StringField(max_length=200, required=True)
    author = StringField(max_length=200, required=True)
    genre = ListField(ReferenceField(Genre))
    price = DecimalField(max_digits=10, decimal_places=2)
    publish_date = DateField()
    description = StringField()
    stock = IntField(required=True)  # MongoEngine's IntField
    cover_image = ImageField(upload_to='book/', required=False)  # MongoEngine's FileField for storing images

    def __str__(self):
        return self.title
