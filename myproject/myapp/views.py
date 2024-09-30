from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DesignForm, ReviewForm, MessageForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login, authenticate, logout
from .models import Design, Review, Message, User
from django.contrib import messages



User = get_user_model()

# Marketplace view
def marketplace(request):
    designs = Design.objects.all()  # Fetch all designs
    return render(request, 'marketplace.html', {'designs': designs})


# View to display details of a specific design
def design_detail(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    return render(request, 'design_detail.html', {'design': design})

# View to upload designs (only accessible by artists)

@login_required  # Ensure only logged-in users can upload designs
def upload_design(request):
    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            design = form.save(commit=False)
            design.artist = request.user  # Assign the logged-in user as the artist
            design.save()
            return redirect('profile')  # Redirect to profile after successful upload
    else:
        form = DesignForm()

    return render(request, 'upload_design.html', {'form': form})


# View for the admin dashboard (only accessible by admins)
@login_required
def admin_dashboard(request): 
    if request.user.role != 'admin':  # Check if the logged-in user is an admin
        return redirect('marketplace')  # Redirect to marketplace if not admin
    
    # Here, you can add logic to manage users, designs, etc.
    return render(request, 'admin_dashboard.html')


# view for the user registration
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('profile')  # Redirect to profile after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Use a custom template for login
    redirect_authenticated_user = True  # Redirect to profile if the user is already logged in

    def get_success_url(self):
        return '/profile/'  # Redirect to profile page after successful login

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('marketplace')



@login_required
def profile_view(request):
    user = request.user
    designs = Design.objects.filter(artist=user)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=user)  # Allow updating the profile picture
        if form.is_valid():
            form.save()
            return redirect('profile')  # Refresh the page after updating
    else:
        form = CustomUserCreationForm(instance=user)

    return render(request, 'profile.html', {'user': user, 'designs': designs, 'form': form})


  

@login_required
def upload_design(request):
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            design = form.save(commit=False)
            design.artist = request.user
            design.file_size = design.file.size  # Calculate file size in bytes
            design.save()
            return redirect('marketplace')  # Redirect to marketplace after uploading
    else:
        form = DesignForm()

    return render(request, 'upload_design.html', {'form': form})



@login_required
def review_design(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.design = design
            review.customer = request.user
            review.save()
            return redirect('design_detail', design_id=design.id)
    else:
        form = ReviewForm()
    return render(request, 'review_design.html', {'form': form, 'design': design})

@login_required
def send_message(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('design_detail', design_id=design.id)
    else:
        form = MessageForm()
    return render(request, 'send_message.html', {'form': form, 'design': design})