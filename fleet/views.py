from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.db.models import Q

from .models import Vehicle, Driver, AxleConfiguration
from .forms import VehicleForm, DriverForm


@login_required
def fleet_list(request):
    """List all vehicles in the fleet."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    company = request.user.company
    
    # Search/filter
    search = request.GET.get('search', '')
    vehicle_type = request.GET.get('type', '')
    
    trucks = company.vehicles.filter(vehicle_type=Vehicle.VehicleType.TRUCK)
    trailers = company.vehicles.filter(vehicle_type=Vehicle.VehicleType.TRAILER)
    
    if search:
        trucks = trucks.filter(
            Q(unit_number__icontains=search) |
            Q(make__icontains=search) |
            Q(plate__icontains=search) |
            Q(vin__icontains=search)
        )
        trailers = trailers.filter(
            Q(unit_number__icontains=search) |
            Q(make__icontains=search) |
            Q(plate__icontains=search) |
            Q(vin__icontains=search)
        )
    
    return render(request, 'fleet/list.html', {
        'trucks': trucks,
        'trailers': trailers,
        'search': search,
    })


@login_required
def vehicle_add(request):
    """Add a new vehicle."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    vehicle_type = request.GET.get('type', 'truck')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.company = request.user.company
            vehicle.save()
            form.save()  # Save axle configs
            messages.success(request, f'{vehicle.get_vehicle_type_display()} added successfully.')
            return redirect('fleet:list')
    else:
        form = VehicleForm(initial={'vehicle_type': vehicle_type})
    
    return render(request, 'fleet/vehicle_form.html', {
        'form': form,
        'title': 'Add New Vehicle',
    })


@login_required
def vehicle_edit(request, vehicle_id):
    """Edit a vehicle."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
        company=request.user.company
    )
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully.')
            return redirect('fleet:list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'fleet/vehicle_form.html', {
        'form': form,
        'vehicle': vehicle,
        'title': f'Edit {vehicle.unit_number}',
    })


@login_required
def vehicle_delete(request, vehicle_id):
    """Delete a vehicle."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    vehicle = get_object_or_404(
        Vehicle,
        pk=vehicle_id,
        company=request.user.company
    )
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted.')
        return redirect('fleet:list')
    
    return render(request, 'fleet/vehicle_confirm_delete.html', {
        'vehicle': vehicle,
    })


@login_required
def vehicle_pdf(request, vehicle_id):
    """View vehicle registration PDF."""
    
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    
    # Check access
    if request.user.is_customer and request.user.company != vehicle.company:
        messages.error(request, 'Access denied.')
        return redirect('fleet:list')
    
    if not vehicle.registration_pdf:
        messages.error(request, 'No registration PDF available.')
        return redirect('fleet:list')
    
    return FileResponse(
        vehicle.registration_pdf.open('rb'),
        content_type='application/pdf'
    )


# Driver views
@login_required
def driver_list(request):
    """List all drivers."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    drivers = request.user.company.drivers.all()
    search = request.GET.get('search', '')
    
    if search:
        drivers = drivers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    return render(request, 'fleet/driver_list.html', {
        'drivers': drivers,
        'search': search,
    })


@login_required
def driver_add(request):
    """Add a new driver."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.company = request.user.company
            driver.save()
            messages.success(request, 'Driver added successfully.')
            return redirect('fleet:driver_list')
    else:
        form = DriverForm()
    
    return render(request, 'fleet/driver_form.html', {
        'form': form,
        'title': 'Add New Driver',
    })


@login_required
def driver_edit(request, driver_id):
    """Edit a driver."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    driver = get_object_or_404(
        Driver,
        pk=driver_id,
        company=request.user.company
    )
    
    if request.method == 'POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver updated successfully.')
            return redirect('fleet:driver_list')
    else:
        form = DriverForm(instance=driver)
    
    return render(request, 'fleet/driver_form.html', {
        'form': form,
        'driver': driver,
        'title': f'Edit {driver.full_name}',
    })


@login_required
def driver_delete(request, driver_id):
    """Delete a driver."""
    
    if not request.user.is_customer or not request.user.company:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    driver = get_object_or_404(
        Driver,
        pk=driver_id,
        company=request.user.company
    )
    
    if request.method == 'POST':
        driver.delete()
        messages.success(request, 'Driver deleted.')
        return redirect('fleet:driver_list')
    
    return render(request, 'fleet/driver_confirm_delete.html', {
        'driver': driver,
    })


# API endpoints for AJAX
@login_required
def api_vehicles(request):
    """API endpoint to get vehicles for dropdowns."""
    
    if not request.user.company:
        return JsonResponse({'error': 'No company'}, status=400)
    
    vehicle_type = request.GET.get('type', '')
    search = request.GET.get('q', '')
    
    vehicles = request.user.company.vehicles.filter(is_active=True)
    
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    
    if search:
        vehicles = vehicles.filter(
            Q(unit_number__icontains=search) |
            Q(make__icontains=search)
        )
    
    data = [{
        'id': v.id,
        'unit_number': v.unit_number,
        'display': str(v),
        'type': v.vehicle_type,
    } for v in vehicles[:50]]
    
    return JsonResponse({'vehicles': data})


@login_required
def api_drivers(request):
    """API endpoint to get drivers for dropdowns."""
    
    if not request.user.company:
        return JsonResponse({'error': 'No company'}, status=400)
    
    search = request.GET.get('q', '')
    
    drivers = request.user.company.drivers.filter(is_active=True)
    
    if search:
        drivers = drivers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    data = [{
        'id': d.id,
        'name': d.full_name,
        'email': d.email,
    } for d in drivers[:50]]
    
    return JsonResponse({'drivers': data})

