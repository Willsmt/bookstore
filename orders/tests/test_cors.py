import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCorsHeaders:
    def test_origem_permitida_recebe_header_cors(self):
        client = APIClient()
        response = client.get(
            reverse("product-list"), HTTP_ORIGIN="http://localhost:3000"
        )
        assert response.status_code == 200
        assert (
            response.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
        )

    def test_origem_nao_permitida_nao_recebe_header_cors(self):
        client = APIClient()
        response = client.get(
            reverse("product-list"), HTTP_ORIGIN="http://site-nao-autorizado.com"
        )
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" not in response.headers

    def test_requisicao_sem_origin_funciona_normalmente(self):
        client = APIClient()
        response = client.get(reverse("product-list"))
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" not in response.headers
