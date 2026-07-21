import factory

from books.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
