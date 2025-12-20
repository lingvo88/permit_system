from django.contrib import admin
from .models import Vehicle, Driver, AxleConfiguration, AxleSpacing, AxleWeight


class AxleConfigurationInline(admin.TabularInline):
    model = AxleConfiguration
    extra = 0


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['unit_number', 'company', 'vehicle_type', 'year', 'make', 'plate', 'is_active']
    list_filter = ['vehicle_type', 'is_active', 'company']
    search_fields = ['unit_number', 'make', 'plate', 'vin']
    inlines = [AxleConfigurationInline]


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'company', 'email', 'phone', 'is_active']
    list_filter = ['is_active', 'company']
    search_fields = ['first_name', 'last_name', 'email']

