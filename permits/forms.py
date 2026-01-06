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
        'load_description', 'load_make_model', 'load_serial',
        'load_length', 'load_width', 'load_height', 'load_weight',
        'load_detailed_description',
        'origin_address', 'destination_address',
        'driver', 'truck', 'trailer', 
        'overall_length_ft', 'overall_length_in',
        'overall_width_ft', 'overall_width_in',
        'overall_height_ft', 'overall_height_in',
        'gross_weight', 'front_overhang_ft', 'front_overhang_in',
        'rear_overhang_ft', 'rear_overhang_in',
        'left_overhang_ft', 'left_overhang_in',
        'right_overhang_ft', 'right_overhang_in',
        'num_axles', 'is_legal_weight',
        'axle_weight_1', 'axle_weight_2', 'axle_weight_3',
        'axle_weight_4', 'axle_weight_5', 'axle_weight_6',
        'axle_weight_7', 'axle_weight_8', 'axle_weight_9',
        'tires_per_axle_1', 'tires_per_axle_2', 'tires_per_axle_3',
        'tires_per_axle_4', 'tires_per_axle_5', 'tires_per_axle_6',
        'tires_per_axle_7', 'tires_per_axle_8', 'tires_per_axle_9',
        'spacing_1_2', 'spacing_2_3', 'spacing_3_4', 'spacing_4_5',
        'spacing_5_6', 'spacing_6_7', 'spacing_7_8', 'spacing_8_9',
        'customer_comments',
    ]
        widgets = {
            'load_description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Object'}),
            'load_make_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Make/Model'}),
            'load_serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial#'}),
            'load_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length', 'step': '0.1'}),
            'load_width': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Width', 'step': '0.1'}),
            'load_height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height', 'step': '0.1'}),
            'load_weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (lbs)'}),
            'load_detailed_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Detailed load description'}),
            'origin_address': forms.TextInput(attrs={'class': 'form-control'}),
            'destination_address': forms.TextInput(attrs={'class': 'form-control'}),
            'driver': forms.Select(attrs={'class': 'form-select'}),
            'truck': forms.Select(attrs={'class': 'form-select'}),
            'trailer': forms.Select(attrs={'class': 'form-select'}),
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
            'num_axles': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_legal_weight': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'axle_weight_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-1'}),
            'axle_weight_2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-2'}),
            'axle_weight_3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-3'}),
            'axle_weight_4': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-4'}),
            'axle_weight_5': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-5'}),
            'axle_weight_6': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-6'}),
            'axle_weight_7': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-7'}),
            'axle_weight_8': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-8'}),
            'axle_weight_9': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-9'}),
            # Tires per axle
            'tires_per_axle_1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-1'}),
            'tires_per_axle_2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-2'}),
            'tires_per_axle_3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-3'}),
            'tires_per_axle_4': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-4'}),
            'tires_per_axle_5': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-5'}),
            'tires_per_axle_6': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-6'}),
            'tires_per_axle_7': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-7'}),
            'tires_per_axle_8': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-8'}),
            'tires_per_axle_9': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ax-9'}),

            # Spacings
            'spacing_1_2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-2', 'step': '0.1'}),
            'spacing_2_3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2-3', 'step': '0.1'}),
            'spacing_3_4': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '3-4', 'step': '0.1'}),
            'spacing_4_5': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '4-5', 'step': '0.1'}),
            'spacing_5_6': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5-6', 'step': '0.1'}),
            'spacing_6_7': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '6-7', 'step': '0.1'}),
            'spacing_7_8': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '7-8', 'step': '0.1'}),
            'spacing_8_9': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '8-9', 'step': '0.1'}),
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
            #self.fields['payment_method'].queryset = company.payment_methods.all()


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

