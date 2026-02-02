from django.db import models
from company.models import Company


class Driver(models.Model):
    """Driver information."""
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='drivers'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    license_state = models.CharField(max_length=2, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(models.Model):
    """Base model for vehicles (trucks and trailers)."""
    
    class VehicleType(models.TextChoices):
        TRUCK = 'truck', 'Truck'
        TRAILER = 'trailer', 'Trailer'
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    vehicle_type = models.CharField(
        max_length=10,
        choices=VehicleType.choices
    )
    unit_number = models.CharField(max_length=50)
    year = models.PositiveIntegerField(null=True, blank=True)
    make = models.CharField(max_length=100, blank=True)
    plate = models.CharField(max_length=20, blank=True)
    plate_state = models.CharField(max_length=2, blank=True)
    vin = models.CharField(max_length=50, blank=True, verbose_name="VIN")
    
    # Dimensions
    length_ft = models.PositiveIntegerField(default=0, verbose_name="Length (ft)")
    length_in = models.PositiveIntegerField(default=0, verbose_name="Length (in)")
    
    # Registration document
    registration_pdf = models.FileField(
        upload_to='registrations/',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['unit_number']
        unique_together = ['company', 'unit_number', 'vehicle_type']
    
    def __str__(self):
        return f"{self.unit_number} - {self.year} {self.make}" if self.year else self.unit_number
    
    @property
    def total_length_inches(self):
        return (self.length_ft * 12) + self.length_in
    
    @property
    def length_display(self):
        return f"{self.length_ft}' {self.length_in}\""


class AxleConfiguration(models.Model):
    """Axle configuration for a vehicle."""
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='axle_configurations'
    )
    configuration_number = models.PositiveIntegerField(default=1)  # 1, 2, or 3
    num_axles = models.PositiveIntegerField(default=0, verbose_name="Number of Axles")
    
    class Meta:
        ordering = ['configuration_number']
        unique_together = ['vehicle', 'configuration_number']
    
    def __str__(self):
        return f"Config {self.configuration_number}: {self.num_axles} axles"


class AxleSpacing(models.Model):
    """Individual axle spacing within a configuration."""
    
    configuration = models.ForeignKey(
        AxleConfiguration,
        on_delete=models.CASCADE,
        related_name='spacings'
    )
    axle_number = models.PositiveIntegerField()
    spacing_ft = models.PositiveIntegerField(default=0)
    spacing_in = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['axle_number']
    
    @property
    def total_inches(self):
        return (self.spacing_ft * 12) + self.spacing_in


class AxleWeight(models.Model):
    """Weight per axle in a configuration."""
    
    configuration = models.ForeignKey(
        AxleConfiguration,
        on_delete=models.CASCADE,
        related_name='weights'
    )
    axle_number = models.PositiveIntegerField()
    weight_lbs = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['axle_number']

class EquipmentCombination(models.Model):
    """Saved combination of driver, truck, and trailer for quick selection."""
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='equipment_combinations'
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
    )
    truck = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='truck_combinations',
        null=True,
        blank=True,
        limit_choices_to={'vehicle_type': Vehicle.VehicleType.TRUCK}
    )
    trailer = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='trailer_combinations',
        null=True,
        blank=True,
        limit_choices_to={'vehicle_type': Vehicle.VehicleType.TRAILER}
    )
    is_default = models.BooleanField(default=False, help_text="Use this as default for new permits")

    
    # Axle spacings (saved for quick auto-fill)
    num_axles = models.PositiveIntegerField(default=5, blank=True)
    # Axle spacings in feet and inches
    spacing_1_2_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_1_2_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_2_3_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_2_3_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_3_4_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_3_4_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_4_5_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_4_5_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_5_6_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_5_6_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_6_7_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_6_7_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_7_8_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_7_8_in = models.PositiveIntegerField(default=0, blank=True)
    spacing_8_9_ft = models.PositiveIntegerField(default=0, blank=True)
    spacing_8_9_in = models.PositiveIntegerField(default=0, blank=True)

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', 'driver__last_name']
        unique_together = ['company', 'driver', 'truck', 'trailer']  # Changed from name
    
    def __str__(self):
        return f"{self.driver.full_name} - {self.truck.unit_number if self.truck else 'No Truck'} / {self.trailer.unit_number if self.trailer else 'No Trailer'}"
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults for this company
        if self.is_default:
            EquipmentCombination.objects.filter(
                company=self.company,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)