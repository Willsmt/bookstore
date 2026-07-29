from rest_framework import viewsets
from orders.models import Order
from orders.serializers import OrderSerializer
from core.pagination import OrderPagination


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
