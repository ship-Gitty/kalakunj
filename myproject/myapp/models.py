from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('artist', 'Artist'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    
    # Manually add a default value for username
    username = models.CharField(max_length=150, unique=True, default='')

    def __str__(self):
        return self.username

class Design(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    artist = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'artist'})
    file_url = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=[('read', 'Read'), ('unread', 'Unread')], default='unread')

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username}'

class Review(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    rating = models.IntegerField()
    review_text = models.TextField()

    def __str__(self):
        return f'Review by {self.customer.username} for {self.design.title}'

class Transaction(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=[('esewa', 'Esewa'), ('khalti', 'Khalti')])
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])

    def __str__(self):
        return f'Transaction for {self.design.title} by {self.customer.username}'
