from rest_framework import serializers
from books.models import Book
from product.serializers import CategorySerializer
from product.models import Category

class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="categories",
        write_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Book
        fields = [
            "id", "title", "author", "isbn", "price", "published_at",
            "is_active", "stock", "categories", "category_ids",
        ]
