from django.contrib import admin
from .models import User, Design, Message, Review, Transaction

admin.site.register(User)
admin.site.register(Design)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(Transaction)