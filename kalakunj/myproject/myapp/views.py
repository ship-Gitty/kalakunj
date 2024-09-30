from django.shortcuts import render, redirect, get_object_or_404
from .models import Design
from django.contrib.auth.decorators import login_required
from .forms import DesignForm, ReviewForm, MessageForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login, authenticate, logout
from .models import Design, Review, Message



# View to list approved designs in the marketplace
def marketplace(request):
    designs = Design.objects.filter(status='approved')
    return render(request, 'marketplace.html', {'designs': designs})

# View to display details of a specific design
def design_detail(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    return render(request, 'design_detail.html', {'design': design})

# View to upload designs (only accessible by artists)
@login_required
def upload_design(request):
    if request.user.role != 'artist':  # Check if the logged-in user is an artist
        return redirect('marketplace')  # Redirect to marketplace if not an artist

    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            design = form.save(commit=False)
            design.artist = request.user  # Assign the logged-in user (artist) to the design
            design.save()
            return redirect('marketplace')  # Redirect to the marketplace after successful upload
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

User = get_user_model()

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('marketplace')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('marketplace')  # Redirect to marketplace after successful login
        else:
            # Handle invalid form data
            print(form.errors)  # Print form errors to console for debugging
    else:
        form = AuthenticationForm()  # Show empty login form
    return render(request, 'login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('marketplace')

@login_required
def upload_design(request):
    if request.user.role != 'artist':
        return redirect('marketplace')  # Only artists can upload
    if request.method == 'POST':
        form = DesignForm(request.POST)
        if form.is_valid():
            design = form.save(commit=False)
            design.artist = request.user
            design.save()
            return redirect('marketplace')
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