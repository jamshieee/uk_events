from rest_framework.generics import ListAPIView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .serializers import ProductSerializer
import cloudinary.uploader


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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

    # 🔥 delete image from Cloudinary
    if product.image:
        cloudinary.uploader.destroy(product.image.public_id)

    product.delete()
    return redirect('admin-products')
