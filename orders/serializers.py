from django.db import transaction
from rest_framework import serializers
from orders.models import Order
from product.models import Product


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "product", "quantity", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade precisa ser maior que zero.")
        return value

    def validate(self, data):
        product = data["product"]
        if not product.is_active:
            raise serializers.ValidationError("Este produto não está disponível para venda.")
        if data["quantity"] > product.stock:
            raise serializers.ValidationError(
                f"Estoque insuficiente. Disponível: {product.stock}, pedido: {data['quantity']}."
            )
        return data

    def create(self, validated_data):
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        with transaction.atomic():
            product = Product.objects.select_for_update().get(pk=product.pk)
            if quantity > product.stock:
                raise serializers.ValidationError("Estoque mudou durante a operação, tenta de novo.")

            product.stock -= quantity
            product.save(update_fields=["stock"])
            order = Order.objects.create(product=product, quantity=quantity)

        return order
