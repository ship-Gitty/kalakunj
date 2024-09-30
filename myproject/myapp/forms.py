from django import forms
from .models import Design, Review, Message

class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['title', 'description', 'file_url', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
