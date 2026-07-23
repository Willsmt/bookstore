from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title", "author"]
    ordering_fields = ["price", "stock", "published_at"]

    def get_queryset(self):
        qs = Book.objects.all()
        if self.action == "reactivate":
            return qs
        return qs.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @action(detail=True, methods=["post"])
    def reactivate(self, request, pk=None):
        book = self.get_object()
        book.is_active = True
        book.save(update_fields=["is_active"])
        serializer = self.get_serializer(book)
        return Response(serializer.data)
