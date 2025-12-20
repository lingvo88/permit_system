from django.urls import path
from . import views

app_name = 'fleet'

urlpatterns = [
    # Vehicles
    path('', views.fleet_list, name='list'),
    path('vehicle/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicle/<int:vehicle_id>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicle/<int:vehicle_id>/delete/', views.vehicle_delete, name='vehicle_delete'),
    path('vehicle/<int:vehicle_id>/pdf/', views.vehicle_pdf, name='vehicle_pdf'),
    
    # Drivers
    path('drivers/', views.driver_list, name='driver_list'),
    path('driver/add/', views.driver_add, name='driver_add'),
    path('driver/<int:driver_id>/edit/', views.driver_edit, name='driver_edit'),
    path('driver/<int:driver_id>/delete/', views.driver_delete, name='driver_delete'),
    
    # API
    path('api/vehicles/', views.api_vehicles, name='api_vehicles'),
    path('api/drivers/', views.api_drivers, name='api_drivers'),
]

