
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DesignForm, ReviewForm, MessageForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, login, authenticate, logout
from .models import Design, Review, Message, User, Transaction
from django.contrib import messages
from django.conf import settings



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
def update_design(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    if request.user != design.artist:
        return redirect('profile')  # Redirect if the user is not the owner

    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile after successful update
    else:
        form = DesignForm(instance=design)
    return render(request, 'update_design.html', {'form': form, 'design': design})

@login_required
def delete_design(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    if request.user == design.artist:
        design.delete()
    return redirect('profile')  # Redirect to profile after successful deletion

@login_required
def checkout(request, design_id):
    design = get_object_or_404(Design, id=design_id)
    if request.method == "POST":
        # Here you would integrate payment gateways (eSewa, Khalti)
        payment_method = request.POST.get('payment_method')
        if payment_method == "esewa":
            return redirect('esewa_payment', design_id=design_id)
        elif payment_method == "khalti":
            return redirect('khalti_payment', design_id=design_id)
    return render(request, 'checkout.html', {'design': design})

# eSewa Payment View
@login_required
def esewa_payment(request, design_id):
    design = get_object_or_404(Design, id=design_id)

    # eSewa API setup and payment URL
    esewa_payment_url = "https://esewa.com.np/#/home"  # replace with eSewa API URL
    esewa_success_url = request.build_absolute_uri(f'/esewa-payment-success/{design_id}')
    esewa_failure_url = request.build_absolute_uri(f'/esewa-payment-failure/{design_id}')

    # Redirect user to eSewa's checkout page
    return redirect(esewa_payment_url)

# Khalti Payment View
@login_required
def khalti_payment(request, design_id):
    design = get_object_or_404(Design, id=design_id)

    # Khalti API setup and payment URL
    khalti_payment_url = "https://khalti.com/#/home"  # replace with Khalti API URL
    khalti_success_url = request.build_absolute_uri(f'/khalti-payment-success/{design_id}')
    khalti_failure_url = request.build_absolute_uri(f'/khalti-payment-failure/{design_id}')

    # Redirect user to Khalti's checkout page
    return redirect(khalti_payment_url)

# Handle payment success
@login_required
def payment_success(request, design_id, payment_method):
    design = get_object_or_404(Design, id=design_id)
    # Record the successful transaction
    Transaction.objects.create(
        design=design,
        customer=request.user,
        amount=design.price,
        payment_method=payment_method,
        status='completed'
    )
    return render(request, 'payment_success.html', {'design': design, 'payment_method': payment_method})

# Handle payment failure
@login_required
def payment_failed(request, design_id, payment_method):
    design = get_object_or_404(Design, id=design_id)
    return render(request, 'payment_failed.html', {'design': design, 'payment_method': payment_method})



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