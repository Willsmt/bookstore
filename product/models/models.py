from django.core.validators import MinValueValidator
from django.db import models
from product.models.category import Category


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
