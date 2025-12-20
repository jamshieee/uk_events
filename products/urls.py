from django.urls import path
from .views import ProductListAPIView
from .views import (
    admin_product_list,
    admin_product_create,
    admin_product_delete,
)

urlpatterns = [
    # PUBLIC API (for frontend)
    path("products/", ProductListAPIView.as_view(), name="product-list"),

    # ADMIN HTML VIEWS
    path("control/products/", admin_product_list, name="admin-products"),
    path("control/products/add/", admin_product_create, name="admin-product-add"),
    path("control/products/delete/<int:pk>/", admin_product_delete, name="admin-product-delete"),
]
