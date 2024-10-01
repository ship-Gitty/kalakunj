from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User, Design, Review, Message

User = get_user_model()

# Custom user creation form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_picture', 'password1', 'password2']

# Design form for uploading designs
class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['title', 'description', 'file_type', 'file', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
