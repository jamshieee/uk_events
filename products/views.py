from rest_framework.generics import ListAPIView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.db.models import Q
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
import cloudinary.uploader


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


@login_required(login_url='admin-login')
def admin_product_list(request):
    query = request.GET.get("q", "").strip()

    products = Product.objects.all().order_by('-id')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'admin/product_list.html', {
        'products': products,
        'query': query,   # IMPORTANT for keeping search text
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

    if product.image:
        cloudinary.uploader.destroy(product.image.public_id)

    product.delete()
    return redirect('admin-products')

@login_required(login_url='admin-login')
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.category = request.POST.get('category')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')

        if request.FILES.get('image'):
            # delete old image from Cloudinary
            if product.image:
                cloudinary.uploader.destroy(product.image.public_id)

            product.image = request.FILES.get('image')

        product.save()
        return redirect('admin-products')

    return render(request, 'admin/product_form.html', {
        'product': product
    })
