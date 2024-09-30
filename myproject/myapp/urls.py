# myapp/urls.py

# myapp/urls.py
from django.urls import path
from .views import (
    marketplace,
    design_detail,
    upload_design,
    admin_dashboard,
    register_view,
    CustomLoginView,
    logout_view,
    profile_view,
)
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
]


