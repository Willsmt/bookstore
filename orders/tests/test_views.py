import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from product.tests.factories import ProductFactory

User = get_user_model()


@pytest.mark.django_db
class TestOrderAPI:
    def test_post_cria_pedido_e_retorna_201(self, authenticated_client):
        product = ProductFactory(stock=5)

        response = authenticated_client.post(
            reverse("order-list"),
            {"product": product.id, "quantity": 2},
            format="json",
        )

        assert response.status_code == 201
        assert response.data["quantity"] == 2

    def test_post_com_estoque_insuficiente_retorna_400(self, authenticated_client):
        product = ProductFactory(stock=1)

        response = authenticated_client.post(
            reverse("order-list"),
            {"product": product.id, "quantity": 5},
            format="json",
        )

        assert response.status_code == 400

    def test_post_anonimo_e_bloqueado(self):
        # o 403 que apareceu no primeiro run nao era bug -- e este teste,
        # so que faltava escrever ele explicitamente.
        product = ProductFactory(stock=5)
        client = APIClient()

        response = client.post(
            reverse("order-list"),
            {"product": product.id, "quantity": 1},
            format="json",
        )

        assert response.status_code == 403