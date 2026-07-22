from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books.views import BookViewSet
from orders.views import OrderViewSet
from product.views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
