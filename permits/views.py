from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.db.models import Q
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.paginator import Paginator

from .models import PermitRequest, PermitState, PermitDocument, PermitComment
from .forms import (
    PermitRequestForm, PermitStateFormSet, PermitDocumentForm,
    PermitStatusForm, EmailForm
)


@login_required
def permit_list(request):
    """List permits for customers."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    permits = PermitRequest.objects.filter(company=request.user.company)
    
    # Filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if search:
        permits = permits.filter(
            Q(permit_number__icontains=search) |
            Q(load_description__icontains=search) |
            Q(origin_address__icontains=search) |
            Q(destination_address__icontains=search) |
            Q(driver__first_name__icontains=search) |
            Q(driver__last_name__icontains=search)
        )
    
    if status:
        permits = permits.filter(status=status)
    
    if date_from:
        permits = permits.filter(created_at__date__gte=date_from)
    
    if date_to:
        permits = permits.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(permits, 10)
    page = request.GET.get('page', 1)
    permits = paginator.get_page(page)
    
    return render(request, 'permits/list.html', {
        'permits': permits,
        'search': search,
        'status_filter': status,
        'date_from': date_from,
        'date_to': date_to,
        'status_choices': PermitRequest.Status.choices,
    })


@login_required
def permit_create(request):
    """Create a new permit request."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    company = request.user.company
    
    # Get equipment combinations
    from fleet.models import EquipmentCombination
    combinations = EquipmentCombination.objects.filter(company=company)
    default_combination = combinations.filter(is_default=True).first()
    
    if request.method == 'POST':
        form = PermitRequestForm(request.POST, company=company)
        
        if form.is_valid():
            permit = form.save(commit=False)
            permit.company = company
            permit.customer = request.user
            
            # Set status based on which button was clicked
            if 'draft' in request.POST:
                permit.status = PermitRequest.Status.DRAFT
            else:
                permit.status = PermitRequest.Status.PENDING
                permit.submitted_at = timezone.now()
                # Send email notification
                try:
                    send_permit_notification(permit)
                except Exception as e:
                    messages.warning(request, f'Permit created but email notification failed: {str(e)}')
            
            permit.save()
            
            # Handle state selections
            selected_states = request.POST.getlist('selected_states[]')
            for state_code in selected_states:
                if state_code:
                    date_key = f'state_date_{state_code}'
                    route_key = f'state_route_{state_code}'
                    comments_key = f'state_comments_{state_code}'
                    
                    PermitState.objects.create(
                        permit=permit,
                        state=state_code,
                        travel_date=request.POST.get(date_key) or None,
                        route=request.POST.get(route_key, ''),
                        comments=request.POST.get(comments_key, '')
                    )
            
            if 'draft' in request.POST:
                messages.success(request, 'Permit saved as draft.')
            else:
                messages.success(request, 'Permit request submitted successfully!')
            
            return redirect('dashboard:customer_dashboard')
    else:
        # Pre-populate with default combination if it exists
        initial = {}
        if default_combination:
            initial = {
                'driver': default_combination.driver,
                'truck': default_combination.truck,
                'trailer': default_combination.trailer,
            }
        form = PermitRequestForm(company=company, initial=initial)
    
    state_choices = PermitState.US_STATES
    
    return render(request, 'permits/form.html', {
        'form': form,
        'company': company,
        'state_choices': state_choices,
        'title': 'New Permit Request',
        'combinations': combinations,
        'default_combination': default_combination,
    })


@login_required
def permit_edit(request, permit_id):
    """Edit a permit request."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    permit = get_object_or_404(
        PermitRequest,
        pk=permit_id,
        company=request.user.company
    )
    
    # Only allow editing drafts
    if permit.status not in [PermitRequest.Status.DRAFT, PermitRequest.Status.PENDING]:
        messages.error(request, 'This permit can no longer be edited.')
        return redirect('permits:detail', permit_id=permit.id)
    
    company = request.user.company
    
    if request.method == 'POST':
        form = PermitRequestForm(request.POST, instance=permit, company=company)
        
        if form.is_valid():
            permit = form.save(commit=False)
            
            if 'submit' in request.POST and permit.status == PermitRequest.Status.DRAFT:
                permit.status = PermitRequest.Status.PENDING
                permit.submitted_at = timezone.now()
            
            permit.save()
            
            # Update states
            permit.states.all().delete()
            states_data = request.POST.getlist('selected_states[]')
            for state_code in states_data:
                if state_code:
                    PermitState.objects.create(
                        permit=permit,
                        state=state_code,
                        travel_date=request.POST.get(f'state_date_{state_code}') or None,
                        route=request.POST.get(f'state_route_{state_code}', ''),
                        comments=request.POST.get(f'state_comments_{state_code}', ''),
                    )
            
            messages.success(request, 'Permit updated successfully.')
            return redirect('permits:detail', permit_id=permit.id)
    else:
        form = PermitRequestForm(instance=permit, company=company)
    
    return render(request, 'permits/form.html', {
        'form': form,
        'permit': permit,
        'company': company,
        'title': f'Edit Permit #{permit.permit_number}',
        'existing_states': list(permit.states.values('state', 'travel_date', 'route', 'comments')),
        'state_choices': PermitState.US_STATES,
    })


@login_required
def permit_detail(request, permit_id):
    """View permit details."""
    
    permit = get_object_or_404(PermitRequest, pk=permit_id)
    
    # Check access
    if request.user.is_customer:
        if request.user.company != permit.company:
            messages.error(request, 'Access denied.')
            return redirect('dashboard:index')
    
    documents = permit.documents.all()
    comments = permit.comments.filter(is_internal=False) if request.user.is_customer else permit.comments.all()
    
    return render(request, 'permits/detail.html', {
        'permit': permit,
        'documents': documents,
        'comments': comments,
    })


@login_required
def permit_copy(request, permit_id):
    """Copy an existing permit to create a new one."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    original = get_object_or_404(
        PermitRequest,
        pk=permit_id,
        company=request.user.company
    )
    
    # Create a copy
    new_permit = PermitRequest.objects.create(
        company=original.company,
        submitted_by=request.user,
        load_description=original.load_description,
        origin_address=original.origin_address,
        destination_address=original.destination_address,
        driver=original.driver,
        truck=original.truck,
        trailer=original.trailer,
        overall_length_ft=original.overall_length_ft,
        overall_length_in=original.overall_length_in,
        overall_width_ft=original.overall_width_ft,
        overall_width_in=original.overall_width_in,
        overall_height_ft=original.overall_height_ft,
        overall_height_in=original.overall_height_in,
        gross_weight=original.gross_weight,
        axle_configuration=original.axle_configuration,
        num_axles=original.num_axles,
        is_legal_weight=original.is_legal_weight,
        payment_method=original.payment_method,
        status=PermitRequest.Status.DRAFT,
    )
    
    # Copy states
    for state in original.states.all():
        PermitState.objects.create(
            permit=new_permit,
            state=state.state,
            route=state.route,
            comments=state.comments,
        )
    
    messages.success(request, f'Permit copied. New permit #{new_permit.permit_number} created as draft.')
    return redirect('permits:edit', permit_id=new_permit.id)


@login_required
def permit_delete(request, permit_id):
    """Delete a permit request."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    permit = get_object_or_404(
        PermitRequest,
        pk=permit_id,
        company=request.user.company
    )
    
    if permit.status not in [PermitRequest.Status.DRAFT]:
        messages.error(request, 'Only draft permits can be deleted.')
        return redirect('permits:detail', permit_id=permit.id)
    
    if request.method == 'POST':
        permit_number = permit.permit_number
        permit.delete()
        messages.success(request, f'Permit #{permit_number} deleted.')
        return redirect('permits:list')
    
    return render(request, 'permits/confirm_delete.html', {'permit': permit})


@login_required
def permit_document_download(request, document_id):
    """Download a permit document."""
    
    document = get_object_or_404(PermitDocument, pk=document_id)
    
    # Check access
    if request.user.is_customer and request.user.company != document.permit.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    return FileResponse(
        document.file.open('rb'),
        as_attachment=True,
        filename=document.filename
    )

