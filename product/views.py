from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["categories"]
    search_fields = ["title"]
    ordering_fields = ["price", "stock"]

    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related("categories")

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])
