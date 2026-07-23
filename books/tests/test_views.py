import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from books.models import Book
from books.tests.factories import BookFactory
from product.tests.factories import CategoryFactory

User = get_user_model()


@pytest.mark.django_db
class TestBookAPI:
    def test_destroy_soft_deletes_book(self, authenticated_client):
        book = BookFactory(is_active=True)
        response = authenticated_client.delete(reverse("book-detail", args=[book.id]))
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

    def test_search_by_title(self):
        BookFactory(title="Aprendendo Python", stock=5)
        BookFactory(title="História do Brasil", stock=5)
        response = APIClient().get(reverse("book-list") + "?search=Python")
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        assert len(results) == 1
        assert "Python" in results[0]["title"]

    def test_ordering_by_price_descending(self):
        BookFactory(title="Livro Barato", price="15.00", stock=5)
        BookFactory(title="Livro Caro", price="80.00", stock=5)
        response = APIClient().get(reverse("book-list") + "?ordering=-price")
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        prices = [float(b["price"]) for b in results]
        assert prices == sorted(prices, reverse=True)

    def test_filter_by_category(self):
        category = CategoryFactory(name="Programação")
        outra_categoria = CategoryFactory(name="Culinária")
        livro_na_categoria = BookFactory(categories=[category])
        BookFactory(categories=[outra_categoria])
        response = APIClient().get(reverse("book-list") + f"?categories={category.id}")
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        assert len(results) == 1
        assert results[0]["id"] == livro_na_categoria.id

    def test_reactivate_reactivates_inactive_book(self, authenticated_client):
        book = BookFactory(is_active=False)
        response = authenticated_client.post(reverse("book-reactivate", args=[book.id]))
        assert response.status_code == 200
        book.refresh_from_db()
        assert book.is_active is True

    def test_reactivate_requires_authentication(self):
        book = BookFactory(is_active=False)
        response = APIClient().post(reverse("book-reactivate", args=[book.id]))
        assert response.status_code == 403

    def test_list_books_usa_prefetch_e_nao_gera_n_mais_1(self, django_assert_num_queries):
        category = CategoryFactory()
        BookFactory.create_batch(5, categories=[category])

        with django_assert_num_queries(3):  # count (paginação) + select books (JOIN product) + prefetch categories
            response = APIClient().get(reverse("book-list"))

        assert response.status_code == 200