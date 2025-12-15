from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

@login_required(login_url='admin-login')
def admin_product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'admin/product_list.html', {
        'products': products
    })

@login_required(login_url='admin-login')
def admin_product_create(request):
    if request.method == "POST":
        Product.objects.create(
            name=request.POST.get('name'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            image=request.FILES.get('image')
        )
        return redirect('admin-products')

    return render(request, 'admin/product_form.html')

@login_required(login_url='admin-login')
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('admin-products')
