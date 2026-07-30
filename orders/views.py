from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from orders.models import Order
from orders.serializers import OrderSerializer
from core.pagination import OrderPagination


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]