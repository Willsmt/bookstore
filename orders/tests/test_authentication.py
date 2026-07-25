import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from product.tests.factories import ProductFactory  # <- confirma esse path, ver abaixo

User = get_user_model()


@pytest.fixture
def order_token(db):
    user = User.objects.create_user(username="orders_user", password="senha123")
    return Token.objects.create(user=user)


@pytest.mark.django_db
class TestOrderTokenAuthentication:

    def test_token_valido_autoriza_criacao(self, order_token):
        product = ProductFactory(stock=10)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {order_token.key}")

        response = client.post(
            reverse("order-list"), {"product": product.id, "quantity": 1}, format="json"
        )

        assert response.status_code == 201

    def test_sem_token_permite_leitura(self):
        client = APIClient()
        response = client.get(reverse("order-list"))
        assert response.status_code == 200

    def test_sem_token_bloqueia_escrita(self):
        product = ProductFactory(stock=10)
        client = APIClient()

        response = client.post(
            reverse("order-list"), {"product": product.id, "quantity": 1}, format="json"
        )

        assert response.status_code == 401
        assert response.data["detail"] == "Authentication credentials were not provided."

    def test_token_invalido_rejeita_mesmo_em_leitura(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token token_forjado_qualquer")

        response = client.get(reverse("order-list"))

        assert response.status_code == 401
        assert response.data["detail"] == "Invalid token."

    def test_sessao_valida_nao_autentica_em_orders(self):
        User.objects.create_user(username="session_user", password="senha123")
        product = ProductFactory(stock=10)
        client = APIClient()
        client.login(username="session_user", password="senha123")

        response = client.post(
            reverse("order-list"), {"product": product.id, "quantity": 1}, format="json"
        )

        assert response.status_code == 401