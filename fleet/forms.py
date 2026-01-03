from django import forms
from .models import Vehicle, Driver, AxleConfiguration


class VehicleForm(forms.ModelForm):
    """Form for adding/editing vehicles."""
    
    # Number of axles field
    num_axles = forms.IntegerField(
        required=False, 
        min_value=0, 
        max_value=20,
        label="Number of Axles",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '# of Axles'})
    )
    
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_type', 'unit_number', 'year', 'make', 
            'plate', 'plate_state', 'vin', 'length_ft', 
            'length_in', 'registration_pdf'
        ]
        widgets = {
            'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
            'unit_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year'}),
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Make'}),
            'plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plate'}),
            'plate_state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2', 'placeholder': 'State'}),
            'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VIN'}),
            'length_ft': forms.NumberInput(attrs={'class': 'form-control length-ft', 'placeholder': 'ft'}),
            'length_in': forms.NumberInput(attrs={'class': 'form-control length-in', 'placeholder': 'in'}),
            'registration_pdf': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load existing axle count if editing
        if self.instance and self.instance.pk:
            config = self.instance.axle_configurations.first()
            if config:
                self.fields['num_axles'].initial = config.num_axles
    
    def save(self, commit=True):
        vehicle = super().save(commit=commit)
        
        if commit:
            # Save single axle configuration
            num_axles = self.cleaned_data.get('num_axles', 0) or 0
            
            # Delete all existing configurations
            vehicle.axle_configurations.all().delete()
            
            # Create new configuration if axles > 0
            if num_axles > 0:
                AxleConfiguration.objects.create(
                    vehicle=vehicle,
                    configuration_number=1,
                    num_axles=num_axles
                )
        
        return vehicle


class DriverForm(forms.ModelForm):
    """Form for adding/editing drivers."""
    
    class Meta:
        model = Driver
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'license_number', 'license_state', 'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'license_state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }