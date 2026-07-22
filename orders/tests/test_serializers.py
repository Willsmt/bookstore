import pytest
from orders.serializers import OrderSerializer
from product.tests.factories import ProductFactory


@pytest.mark.django_db
class TestOrderSerializer:
    def test_quantidade_zero_e_invalida(self):
        product = ProductFactory(stock=10)
        serializer = OrderSerializer(data={"product": product.id, "quantity": 0})
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors

    def test_produto_inativo_nao_pode_ser_pedido(self):
        product = ProductFactory(stock=10, is_active=False)
        serializer = OrderSerializer(data={"product": product.id, "quantity": 1})
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_quantidade_maior_que_estoque_e_invalida(self):
        product = ProductFactory(stock=2)
        serializer = OrderSerializer(data={"product": product.id, "quantity": 3})
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_pedido_valido_debita_estoque(self):
        product = ProductFactory(stock=10)
        serializer = OrderSerializer(data={"product": product.id, "quantity": 3})
        assert serializer.is_valid(), serializer.errors

        order = serializer.save()

        product.refresh_from_db()
        assert product.stock == 7
        assert order.quantity == 3
        assert order.product_id == product.id
