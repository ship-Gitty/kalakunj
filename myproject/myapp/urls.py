# core/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('marketplace/', views.marketplace, name='marketplace'),
    path('design/<int:design_id>/', views.design_detail, name='design_detail'),
    path('upload/', views.upload_design, name='upload_design'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL using custom view
    path('login/', views.login_view, name='login'),  # Login URL using custom view
    path('register/', views.register_view, name='register'),  # Registration URL using custom view
]
