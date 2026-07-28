from rest_framework import serializers
from product.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "is_active"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="categories",
        write_only=True,
        many=True,
        required=False,
    )

    class Meta:
        model = Product
        fields = ["id", "title", "price", "stock", "is_active", "categories", "category_ids", "created_at"]
