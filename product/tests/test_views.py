import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from product.models import Product
from product.tests.factories import CategoryFactory, ProductFactory

User = get_user_model()


@pytest.mark.django_db
class TestProductAPI:
    def test_destroy_soft_deletes_product(self, authenticated_client):
        product = ProductFactory(is_active=True)
        response = authenticated_client.delete(reverse("product-detail", args=[product.id]))
        assert response.status_code == 204
        product.refresh_from_db()
        assert product.is_active is False
        assert Product.objects.filter(pk=product.pk).exists()

    def test_inactive_product_not_listed(self):
        ProductFactory(is_active=False)
        active = ProductFactory(is_active=True)
        response = APIClient().get(reverse("product-list"))
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        listed_ids = [p["id"] for p in results]
        assert active.id in listed_ids
        assert len(listed_ids) == 1

    def test_ordering_by_price_ascending(self):
        ProductFactory(title="Caro", price="100.00", stock=5)
        ProductFactory(title="Barato", price="10.00", stock=5)
        response = APIClient().get(reverse("product-list") + "?ordering=price")
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        prices = [float(p["price"]) for p in results]
        assert prices == sorted(prices)

    def test_search_by_title(self):
        ProductFactory(title="Django para Iniciantes", stock=5)
        ProductFactory(title="Culinária Italiana", stock=5)
        response = APIClient().get(reverse("product-list") + "?search=Django")
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        assert len(results) == 1
        assert "Django" in results[0]["title"]

    def test_filter_by_category(self):
        category = CategoryFactory(name="Programação")
        outra_categoria = CategoryFactory(name="Culinária")
        produto_na_categoria = ProductFactory(categories=[category])
        ProductFactory(categories=[outra_categoria])
        response = APIClient().get(reverse("product-list") + f"?categories={category.id}")
        payload = response.json()
        results = payload["results"] if isinstance(payload, dict) and "results" in payload else payload
        assert len(results) == 1
        assert results[0]["id"] == produto_na_categoria.id

    def test_reactivate_reactivates_inactive_product(self, authenticated_client):
        product = ProductFactory(is_active=False)
        response = authenticated_client.post(reverse("product-reactivate", args=[product.id]))
        assert response.status_code == 200
        product.refresh_from_db()
        assert product.is_active is True

    def test_reactivate_requires_authentication(self):
        product = ProductFactory(is_active=False)
        response = APIClient().post(reverse("product-reactivate", args=[product.id]))
        assert response.status_code == 403

    def test_create_product_com_preco_negativo_retorna_400(self, authenticated_client):
        response = authenticated_client.post(
            reverse("product-list"),
            {"title": "Produto Teste", "price": "-10.00", "stock": 5},
            format="json",
        )
        assert response.status_code == 400
        assert "price" in response.json()

    def test_list_products_usa_prefetch_e_nao_gera_n_mais_1(self, django_assert_num_queries):
        category = CategoryFactory()
        ProductFactory.create_batch(5, categories=[category])

        with django_assert_num_queries(3):
            response = APIClient().get(reverse("product-list"))

        assert response.status_code == 200