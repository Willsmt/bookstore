import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def authenticated_client(db):
    user = User.objects.create_user(username="cliente", password="senha123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client