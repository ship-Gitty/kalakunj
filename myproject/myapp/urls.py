# myapp/urls.py

# myapp/urls.py
from django.urls import path
from . import views
from .views import (
    marketplace,
    design_detail,
    upload_design,
    admin_dashboard,
    register_view,
    CustomLoginView,
    logout_view,
    profile_view,
    update_design,
    delete_design
)
from .views import esewa_payment, khalti_payment, payment_success, payment_failed

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', marketplace, name='marketplace'),
    path('design/<int:design_id>/', design_detail, name='design_detail'),
    path('upload/', upload_design, name='upload_design'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),  # Add this line
    path('profile/', profile_view, name='profile'),
    path('update_design/<int:design_id>/', update_design, name='update_design'),
    path('delete_design/<int:design_id>/', delete_design, name='delete_design'),
    path('design/<int:design_id>/', views.design_detail, name='design_detail'),
    path('checkout/<int:design_id>/', views.checkout, name='checkout'),  # Add this line
    path('esewa-payment/<int:design_id>/', views.esewa_payment, name='esewa_payment'),
    path('khalti-payment/<int:design_id>/', views.khalti_payment, name='khalti_payment'),
    path('payment-success/<int:design_id>/<str:payment_method>/', views.payment_success, name='payment_success'),
    path('payment-failure/<int:design_id>/<str:payment_method>/', views.payment_failed, name='payment_failed'),

]


