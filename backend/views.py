from django.shortcuts import render

def frontend_home(request):
    return render(request, 'frontend/index.html')

def product_detail(request, id):
    return render(request, "frontend/product_details.html", {
        "product_id": id
    })
