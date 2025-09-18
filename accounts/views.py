from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """Custom login view with Bootstrap styling"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().first_name}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = reverse_lazy('tourism:home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    """User registration view"""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('tourism:home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.success(self.request, f'Account created successfully! Welcome to Smart Tourism India, {user.first_name}!')
        return response


@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'title': 'My Profile',
        'profile': profile,
        'user': request.user,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'title': 'Edit Profile',
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)
