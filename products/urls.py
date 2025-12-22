from django.urls import path
from .views import (
    admin_product_list,
    admin_product_create,
    admin_product_delete,
    admin_product_edit
)

urlpatterns = [
    path('', admin_product_list, name='admin-products'),
    path('add/', admin_product_create, name='admin-product-add'),
    path('edit/<int:pk>/', admin_product_edit, name='admin-product-edit'),
    path('delete/<int:pk>/', admin_product_delete, name='admin-product-delete'),
]
