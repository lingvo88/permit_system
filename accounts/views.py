from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CustomerRegistrationForm, LoginForm, UserProfileForm


class CustomerLoginView(LoginView):
    """Login view for customers and employees."""
    
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class CustomerLogoutView(LogoutView):
    """Logout view."""
    
    next_page = 'accounts:login'


class CustomerRegisterView(CreateView):
    """Registration view for new customers."""
    
    form_class = CustomerRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:index')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully! Welcome to the Permit System.')
        return redirect(self.success_url)


@login_required
def profile_view(request):
    """User profile view."""
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})

