from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin-dashboard')

    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin-dashboard')
        else:
            error = "Invalid credentials or not an admin user"

    return render(request, "admin/login.html", {"error": error})


@login_required(login_url='admin-login')
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")


def admin_logout(request):
    logout(request)
    return redirect('admin-login')
