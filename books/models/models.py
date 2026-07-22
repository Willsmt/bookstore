from django.db import models
from product.models import Product

class Book(Product):
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_at = models.DateField()
