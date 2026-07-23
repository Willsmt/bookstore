from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from product.models import Category, Product
from product.serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = Category.objects.all()
        if self.action == "reactivate":
            return qs
        return qs.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        category = self.get_object()
        category.is_active = True
        category.save(update_fields=["is_active"])
        serializer = self.get_serializer(category)
        return Response(serializer.data)



class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["categories"]
    search_fields = ["title"]
    ordering_fields = ["price", "stock"]

    def get_queryset(self):
        qs = Product.objects.prefetch_related("categories")
        if self.action == "reactivate":
            return qs
        return qs.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        product = self.get_object()
        product.is_active = True
        product.save(update_fields=["is_active"])
        serializer = self.get_serializer(product)
        return Response(serializer.data)
