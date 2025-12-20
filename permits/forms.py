from django import forms
from django.forms import inlineformset_factory
from .models import PermitRequest, PermitState, PermitAxleDetail, PermitDocument


class MultipleFileInput(forms.FileInput):
    """Custom file input widget that allows multiple file selection."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Custom file field that handles multiple files."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class PermitRequestForm(forms.ModelForm):
    """Form for creating/editing permit requests."""
    
    class Meta:
        model = PermitRequest
        fields = [
            'load_description', 'origin_address', 'destination_address',
            'driver', 'truck', 'trailer', 'payment_method',
            'overall_length_ft', 'overall_length_in',
            'overall_width_ft', 'overall_width_in',
            'overall_height_ft', 'overall_height_in',
            'gross_weight', 'front_overhang_ft', 'front_overhang_in',
            'rear_overhang_ft', 'rear_overhang_in',
            'left_overhang_ft', 'left_overhang_in',
            'right_overhang_ft', 'right_overhang_in',
            'axle_configuration', 'num_axles', 'is_legal_weight',
            'customer_comments',
        ]
        widgets = {
            'load_description': forms.TextInput(attrs={'class': 'form-control'}),
            'origin_address': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'truck': forms.Select(attrs={'class': 'form-select'}),
            'trailer': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'overall_length_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'overall_length_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'overall_width_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'overall_width_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'overall_height_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'overall_height_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'gross_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'lbs'}),
            'front_overhang_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'front_overhang_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'rear_overhang_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'rear_overhang_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'left_overhang_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'left_overhang_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'right_overhang_ft': forms.NumberInput(attrs={'class': 'form-control dim-ft', 'placeholder': 'ft'}),
            'right_overhang_in': forms.NumberInput(attrs={'class': 'form-control dim-in', 'placeholder': 'in'}),
            'axle_configuration': forms.Select(attrs={'class': 'form-select'}, choices=[(1, '1'), (2, '2'), (3, '3')]),
            'num_axles': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_legal_weight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'customer_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if company:
            # Filter queryset to company's resources
            from fleet.models import Vehicle, Driver
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
            self.fields['payment_method'].queryset = company.payment_methods.all()


class PermitStateForm(forms.ModelForm):
    """Form for permit states."""
    
    class Meta:
        model = PermitState
        fields = ['state', 'travel_date', 'route', 'comments']
        widgets = {
            'state': forms.Select(attrs={'class': 'form-select state-select'}),
            'travel_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'route': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Route'}),
            'comments': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comments'}),
        }


PermitStateFormSet = inlineformset_factory(
    PermitRequest,
    PermitState,
    form=PermitStateForm,
    extra=1,
    can_delete=True
)


class PermitAxleDetailForm(forms.ModelForm):
    """Form for axle details."""
    
    class Meta:
        model = PermitAxleDetail
        fields = ['axle_number', 'spacing_ft', 'spacing_in', 'weight_lbs']
        widgets = {
            'axle_number': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'spacing_ft': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ft'}),
            'spacing_in': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'in'}),
            'weight_lbs': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'lbs'}),
        }


class PermitDocumentForm(forms.ModelForm):
    """Form for uploading documents."""
    
    class Meta:
        model = PermitDocument
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class PermitStatusForm(forms.ModelForm):
    """Form for updating permit status (employees)."""
    
    class Meta:
        model = PermitRequest
        fields = ['status', 'assigned_to', 'internal_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EmailForm(forms.Form):
    """Form for sending emails to customers."""
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
    )
    attachments = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'multiple': True
        })
    )

