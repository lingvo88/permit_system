from django import forms
from .models import Vehicle, Driver, AxleConfiguration, EquipmentCombination


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
        
        # Make fields required
        self.fields['unit_number'].required = True
        self.fields['num_axles'].required = True
        self.fields['year'].required = True
        self.fields['make'].required = True
        self.fields['plate'].required = True
        self.fields['plate_state'].required = True
        self.fields['vin'].required = True
        self.fields['length_ft'].required = True
        self.fields['length_in'].required = False  # inches not required
        
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

class EquipmentCombinationForm(forms.ModelForm):
    """Form for creating/editing equipment combinations."""

    class Meta:
        model = EquipmentCombination
        fields = ['driver', 'truck', 'trailer', 'is_default', 'num_axles', 
                  'spacing_1_2_ft', 'spacing_1_2_in', 
                  'spacing_2_3_ft', 'spacing_2_3_in',
                  'spacing_3_4_ft', 'spacing_3_4_in', 
                  'spacing_4_5_ft', 'spacing_4_5_in',
                  'spacing_5_6_ft', 'spacing_5_6_in', 
                  'spacing_6_7_ft', 'spacing_6_7_in',
                  'spacing_7_8_ft', 'spacing_7_8_in', 
                  'spacing_8_9_ft', 'spacing_8_9_in']
        widgets = {
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'truck': forms.Select(attrs={'class': 'form-select'}),
            'trailer': forms.Select(attrs={'class': 'form-select'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'num_axles': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
            'spacing_1_2_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_1_2_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_2_3_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_2_3_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_3_4_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_3_4_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_4_5_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_4_5_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_5_6_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_5_6_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_6_7_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_6_7_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_7_8_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_7_8_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_8_9_ft': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
            'spacing_8_9_in': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'}),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)

        if company:
            self.fields['driver'].queryset = Driver.objects.filter(company=company, is_active=True)
            self.fields['truck'].queryset = Vehicle.objects.filter(
                company=company,
                vehicle_type=Vehicle.VehicleType.TRUCK,
                is_active=True
            )
            self.fields['trailer'].queryset = Vehicle.objects.filter(
                company=company,
                vehicle_type=Vehicle.VehicleType.TRAILER,
                is_active=True
            )