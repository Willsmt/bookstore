import pytest
from rest_framework.test import APIClient

from books.models import Book
from product.models import Category, Product

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


class TestProductListExcludesBooks:
    """Regressão do bug de MTI: Book não pode aparecer em /api/products/"""

    def test_product_list_does_not_include_books(self, api_client):
        Product.objects.create(title="Mouse Gamer", price="150.00", stock=10)
        Book.objects.create(
            title="Duna",
            price="45.00",
            stock=5,
            author="Frank Herbert",
            isbn="9788576570059",
            published_at="1965-08-01",
        )

        response = api_client.get("/api/products/")

        assert response.data["count"] == 1
        titles = [item["title"] for item in response.data["results"]]
        assert "Duna" not in titles
        assert "Mouse Gamer" in titles

    def test_book_still_appears_in_books_endpoint(self, api_client):
        Book.objects.create(
            title="Duna",
            price="45.00",
            stock=5,
            author="Frank Herbert",
            isbn="9788576570059",
            published_at="1965-08-01",
        )

        response = api_client.get("/api/books/")

        assert response.data["count"] == 1


class TestCategoryFilterExcludesInactive:
    def test_inactive_category_not_assignable_via_product_creation(
        self, authenticated_client
    ):
        inactive = Category.objects.create(
            name="Descontinuada", slug="descontinuada", is_active=False
        )

        response = authenticated_client.post(
            "/api/products/",
            {
                "title": "Produto Teste",
                "price": "99.90",
                "stock": 5,
                "category_ids": [inactive.id],
            },
        )

        assert response.status_code == 400


class TestPaginationLimits:
    """Regressão da Aula 5: max_page_size precisa travar mesmo se o cliente pedir mais"""

    def test_page_size_respects_max_page_size(self, api_client):
        Product.objects.bulk_create(
            [Product(title=f"Produto {i}", price="10.00", stock=1) for i in range(150)]
        )

        response = api_client.get("/api/products/?page_size=99999")

        assert (
            len(response.data["results"]) <= 100
        )  # max_page_size do ProductPagination
