from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.conf import settings

from permits.models import PermitRequest, PermitDocument, PermitComment
from permits.forms import PermitStatusForm, EmailForm, PermitDocumentForm
from company.models import Company
from .models import EmailLog, EmailAttachment


@login_required
def index(request):
    """Main dashboard - redirects based on user type."""
    
    if request.user.is_employee:
        return redirect('dashboard:employee_dashboard')
    else:
        return redirect('dashboard:customer_dashboard')


@login_required
def customer_dashboard(request):
    """Customer dashboard showing their permits."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Please complete your company registration.')
        return redirect('accounts:profile')
    
    company = request.user.company
    
    # Get permit statistics
    total_permits = PermitRequest.objects.filter(company=company).count()
    pending_permits = PermitRequest.objects.filter(company=company, status=PermitRequest.Status.PENDING).count()
    in_progress = PermitRequest.objects.filter(company=company, status=PermitRequest.Status.IN_PROGRESS).count()
    completed = PermitRequest.objects.filter(company=company, status=PermitRequest.Status.COMPLETED).count()
    
    # Recent permits
    recent_permits = PermitRequest.objects.filter(company=company)[:10]
    
    return render(request, 'dashboard/customer_dashboard.html', {
        'company': company,
        'total_permits': total_permits,
        'pending_permits': pending_permits,
        'in_progress': in_progress,
        'completed': completed,
        'recent_permits': recent_permits,
    })


@login_required
def employee_dashboard(request):
    """Employee dashboard showing all permits to review."""
    
    if not request.user.is_employee:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    # Get all permits with filters
    permits = PermitRequest.objects.all()
    
    # Filters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    company_id = request.GET.get('company', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if search:
        permits = permits.filter(
            Q(permit_number__icontains=search) |
            Q(load_description__icontains=search) |
            Q(company__name__icontains=search) |
            Q(origin_address__icontains=search) |
            Q(destination_address__icontains=search) |
            Q(driver__first_name__icontains=search) |
            Q(driver__last_name__icontains=search)
        )
    
    if status:
        permits = permits.filter(status=status)
    
    if company_id:
        permits = permits.filter(company_id=company_id)
    
    if date_from:
        permits = permits.filter(created_at__date__gte=date_from)
    
    if date_to:
        permits = permits.filter(created_at__date__lte=date_to)
    
    # Statistics
    stats = {
        'total': PermitRequest.objects.count(),
        'pending': PermitRequest.objects.filter(status=PermitRequest.Status.PENDING).count(),
        'in_progress': PermitRequest.objects.filter(status=PermitRequest.Status.IN_PROGRESS).count(),
        'completed': PermitRequest.objects.filter(status=PermitRequest.Status.COMPLETED).count(),
    }
    
    # Pagination
    paginator = Paginator(permits, 20)
    page = request.GET.get('page', 1)
    permits = paginator.get_page(page)
    
    # Companies for filter dropdown
    companies = Company.objects.all()
    
    return render(request, 'dashboard/employee_dashboard.html', {
        'permits': permits,
        'stats': stats,
        'companies': companies,
        'search': search,
        'status_filter': status,
        'company_filter': company_id,
        'date_from': date_from,
        'date_to': date_to,
        'status_choices': PermitRequest.Status.choices,
    })


@login_required
def employee_permit_detail(request, permit_id):
    """Employee view of permit details with management options."""
    
    if not request.user.is_employee:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    permit = get_object_or_404(PermitRequest, pk=permit_id)
    
    if request.method == 'POST':
        form = PermitStatusForm(request.POST, instance=permit)
        if form.is_valid():
            updated_permit = form.save(commit=False)
            
            # Update completion time if completed
            if updated_permit.status == PermitRequest.Status.COMPLETED and not permit.completed_at:
                updated_permit.completed_at = timezone.now()
            
            updated_permit.save()
            messages.success(request, 'Permit updated successfully.')
            return redirect('dashboard:employee_permit_detail', permit_id=permit.id)
    else:
        form = PermitStatusForm(instance=permit)
    
    # Get employees for assignment dropdown
    from accounts.models import User
    employees = User.objects.filter(user_type__in=[User.UserType.EMPLOYEE, User.UserType.ADMIN])
    form.fields['assigned_to'].queryset = employees
    
    comments = permit.comments.all()
    email_logs = permit.email_logs.all()[:10]
    
    return render(request, 'dashboard/employee_permit_detail.html', {
        'permit': permit,
        'form': form,
        'comments': comments,
        'email_logs': email_logs,
    })


@login_required
def send_email(request, permit_id):
    """Send email to customer with attachments."""
    
    if not request.user.is_employee:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    permit = get_object_or_404(PermitRequest, pk=permit_id)
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message_body = request.POST.get('message', '')
        recipient = request.POST.get('recipient', permit.company.email)
        
        if not subject:
            messages.error(request, 'Subject.')
            return redirect('dashboard:employee_permit_detail', permit_id=permit.id)
        
        # Create email

        signature = """

---
Best regards,

PermitPro Team
Big Rig Permits
Email: bigrigpermitsinc@gmail.com
Phone: (773) 992-0771
Website: https://bigrigpermits.org

This is an automated message. Please do not reply directly to this email.
        """
        email = EmailMessage(
            subject=subject,
            body=message_body + signature,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[request.user.email] if request.user.email else None,
        )
        
        # Handle attachments
        attachment_filenames = []
        files = request.FILES.getlist('attachments')
        
        for f in files:
            email.attach(f.name, f.read(), f.content_type)
            attachment_filenames.append(f.name)

        
        try:
            email.send()
            
            # Log the email
            email_log = EmailLog.objects.create(
                permit=permit,
                sent_by=request.user,
                recipient_email=recipient,
                subject=subject,
                body=message_body,
                attachments=attachment_filenames,
            )
            
            # Save uploaded attachments
            for f in request.FILES.getlist('attachments'):
                f.seek(0)  # Reset file pointer
                EmailAttachment.objects.create(
                    email_log=email_log,
                    file=f,
                    filename=f.name,
                )
                # Automatically change status to completed when email is sent
            if permit.status != PermitRequest.Status.COMPLETED:
                permit.status = PermitRequest.Status.COMPLETED
                permit.completed_at = timezone.now()
                permit.save()
                messages.success(request, f'Email sent to {recipient}. Permit status changed to Completed.')
            else:
                messages.success(request, f'Email sent to {recipient}')
                
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
            
            messages.success(request, f'Email sent to {recipient}')
        except Exception as e:
            messages.error(request, f'Failed to send email: {str(e)}')
        
        return redirect('dashboard:employee_permit_detail', permit_id=permit.id)
    
    return redirect('dashboard:employee_permit_detail', permit_id=permit.id)


@login_required
def add_comment(request, permit_id):
    """Add a comment to a permit."""
    
    permit = get_object_or_404(PermitRequest, pk=permit_id)
    
    # Check access
    if request.user.is_customer and request.user.company != permit.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        is_internal = request.POST.get('is_internal') == 'on' and request.user.is_employee
        
        if message:
            PermitComment.objects.create(
                permit=permit,
                user=request.user,
                message=message,
                is_internal=is_internal,
            )
            messages.success(request, 'Comment added.')
    
    # Redirect back to appropriate detail page
    if request.user.is_employee:
        return redirect('dashboard:employee_permit_detail', permit_id=permit.id)
    else:
        return redirect('permits:detail', permit_id=permit.id)


@login_required
def company_list(request):
    """List all companies (employee view)."""
    
    if not request.user.is_employee:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    companies = Company.objects.annotate(
        permit_count=Count('permit_requests')
    ).order_by('name')
    
    search = request.GET.get('search', '')
    if search:
        companies = companies.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(usdot_number__icontains=search)
        )
    
    return render(request, 'dashboard/company_list.html', {
        'companies': companies,
        'search': search,
    })


@login_required
def company_detail_employee(request, company_id):
    """View company details (employee view)."""
    
    if not request.user.is_employee:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    company = get_object_or_404(Company, pk=company_id)
    permits = company.permit_requests.all()[:20]
    vehicles = company.vehicles.all()
    drivers = company.drivers.all()
    
    return render(request, 'dashboard/company_detail_employee.html', {
        'company': company,
        'permits': permits,
        'vehicles': vehicles,
        'drivers': drivers,
    })

