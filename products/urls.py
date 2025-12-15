from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from django.urls import path
from django.urls import path
from .views import (
    admin_product_list,
    admin_product_create,
    admin_product_delete,
)


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = router.urls

urlpatterns += [
    path('control/products/', admin_product_list, name='admin-products'),
    path('control/products/add/', admin_product_create, name='admin-product-add'),
    path('control/products/delete/<int:pk>/', admin_product_delete, name='admin-product-delete'),
]