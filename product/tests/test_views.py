import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from product.models import Product
from product.tests.factories import ProductFactory

User = get_user_model()


@pytest.mark.django_db
class TestProductAPI:
    def _authenticated_client(self):
        user = User.objects.create_user(username="cliente", password="senha123")
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_destroy_soft_deletes_product(self):
        product = ProductFactory(is_active=True)
        client = self._authenticated_client()

        response = client.delete(reverse("product-detail", args=[product.id]))

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
