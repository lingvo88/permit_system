from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Company, PaymentMethod
from .forms import CompanyForm, PaymentMethodForm
from accounts.forms import UserProfileForm


@login_required
def company_detail(request):
    """View company details."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'You do not have a company associated with your account.')
        return redirect('dashboard:index')
    
    company = request.user.company
    users = company.users.all()
    payment_methods = company.payment_methods.all()
    
    return render(request, 'company/detail.html', {
        'company': company,
        'users': users,
        'payment_methods': payment_methods,
    })


@login_required
def company_edit(request):
    """Edit company information."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'You do not have a company associated with your account.')
        return redirect('dashboard:index')
    
    company = request.user.company
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company information updated successfully.')
            return redirect('company:detail')
    else:
        form = CompanyForm(instance=company)
    
    return render(request, 'company/edit.html', {
        'form': form,
        'company': company,
    })


@login_required
def user_edit(request, user_id):
    """Edit a company user."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    user = get_object_or_404(request.user.company.users, pk=user_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('company:detail')
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'company/user_edit.html', {
        'form': form,
        'edit_user': user,
    })


@login_required
def user_delete(request, user_id):
    """Delete a company user."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.user.id == user_id:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('company:detail')
    
    user = get_object_or_404(request.user.company.users, pk=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('company:detail')


@login_required
def payment_method_add(request):
    """Add a new payment method."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.company = request.user.company
            payment.save()
            messages.success(request, 'Payment method added successfully.')
            return redirect('company:detail')
    else:
        form = PaymentMethodForm()
    
    return render(request, 'company/payment_add.html', {
        'form': form,
    })


@login_required
def payment_method_delete(request, payment_id):
    """Delete a payment method."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    payment = get_object_or_404(
        PaymentMethod,
        pk=payment_id,
        company=request.user.company
    )
    payment.delete()
    messages.success(request, 'Payment method deleted.')
    return redirect('company:detail')

