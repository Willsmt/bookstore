import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from books.models import Book
from books.tests.factories import BookFactory

User = get_user_model()


@pytest.mark.django_db
class TestBookAPI:
    def _authenticated_client(self):
        user = User.objects.create_user(username="cliente", password="senha123")
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_destroy_soft_deletes_book(self):
        book = BookFactory(is_active=True)
        client = self._authenticated_client()

        response = client.delete(reverse("book-detail", args=[book.id]))

        assert response.status_code == 204
        book.refresh_from_db()
        assert book.is_active is False
        assert Book.objects.filter(pk=book.pk).exists()

    def test_inactive_book_not_listed(self):
        BookFactory(is_active=False)
        active = BookFactory(is_active=True)

        response = APIClient().get(reverse("book-list"))
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload

        listed_ids = [b["id"] for b in results]
        assert active.id in listed_ids
        assert len(listed_ids) == 1
