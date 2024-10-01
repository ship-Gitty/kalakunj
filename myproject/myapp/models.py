from django.contrib.auth.models import AbstractUser
from django.db import models
import os


# Custom User model extending AbstractUser
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('artist', 'Artist'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.username


# Design model to hold uploaded design details
class Design(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='designs/', null=True, blank=True)
    file_type = models.CharField(max_length=10, blank=True)  # Store file type (extension)
    file_size = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        # Automatically set file type based on uploaded file's extension
        if self.file:
            self.file_type = os.path.splitext(self.file.name)[1].lower().replace('.', '')  # Get extension without the dot
            self.file_size = self.file.size  # Set file size
        super().save(*args, **kwargs)  # Save the model

    def __str__(self):
        return self.title


# Message model for communication between users
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=[('read', 'Read'), ('unread', 'Unread')], default='unread')

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'


# Review model for customers to review designs
class Review(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    rating = models.IntegerField()  # Rating should ideally be limited (e.g., 1-5 stars)
    review_text = models.TextField()

    def __str__(self):
        return f'Review by {self.customer.username} for {self.design.title}'


# Transaction model to track customer purchases
class Transaction(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('esewa', 'Esewa'), ('khalti', 'Khalti')])
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])

    def __str__(self):
        return f'Transaction for {self.design.title} by {self.customer.username}'
