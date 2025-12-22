from django.shortcuts import redirect
from django.urls import path
from .views import admin_login, admin_dashboard, admin_logout
from django.contrib.auth.decorators import login_required

def control_root(request):
    return redirect('admin-dashboard')

urlpatterns = [
    path('', login_required(control_root, login_url='admin-login')),
    path('login/', admin_login, name='admin-login'),
    path('dashboard/', login_required(admin_dashboard, login_url='admin-login'), name='admin-dashboard'),
    path('logout/', login_required(admin_logout, login_url='admin-login'), name='admin-logout'),
]
