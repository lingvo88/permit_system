from django import forms
from .models import Vehicle, Driver, AxleConfiguration


class VehicleForm(forms.ModelForm):
    """Form for adding/editing vehicles."""
    
    # Axle configuration fields
    axle_config_1 = forms.IntegerField(
        required=False, 
        min_value=0, 
        max_value=15,
        label="Axle Configuration 1 - # of Axles",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '# of Axles'})
    )
    axle_config_2 = forms.IntegerField(
        required=False, 
        min_value=0, 
        max_value=15,
        label="Axle Configuration 2 - # of Axles",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '# of Axles'})
    )
    axle_config_3 = forms.IntegerField(
        required=False, 
        min_value=0, 
        max_value=15,
        label="Axle Configuration 3 - # of Axles",
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
        
        # Load existing axle configurations if editing
        if self.instance and self.instance.pk:
            for config in self.instance.axle_configurations.all():
                field_name = f'axle_config_{config.configuration_number}'
                if field_name in self.fields:
                    self.fields[field_name].initial = config.num_axles
    
    def save(self, commit=True):
        vehicle = super().save(commit=commit)
        
        if commit:
            # Save axle configurations
            for i in range(1, 4):
                num_axles = self.cleaned_data.get(f'axle_config_{i}', 0) or 0
                if num_axles > 0:
                    AxleConfiguration.objects.update_or_create(
                        vehicle=vehicle,
                        configuration_number=i,
                        defaults={'num_axles': num_axles}
                    )
                else:
                    # Remove configuration if set to 0
                    AxleConfiguration.objects.filter(
                        vehicle=vehicle,
                        configuration_number=i
                    ).delete()
        
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

