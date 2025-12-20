from django import forms
from .models import Company, PaymentMethod


class CompanyForm(forms.ModelForm):
    """Form for editing company information."""
    
    class Meta:
        model = Company
        fields = [
            'name', 'email', 'address', 'city', 'state', 
            'zipcode', 'phone', 'usdot_number', 'fein', 'ifta_number'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'usdot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'fein': forms.TextInput(attrs={'class': 'form-control'}),
            'ifta_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PaymentMethodForm(forms.ModelForm):
    """Form for adding payment methods."""
    
    # Card fields
    card_number = forms.CharField(max_length=19, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '1234 5678 9012 3456'
    }))
    cvv = forms.CharField(max_length=4, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'CVV'
    }))
    
    class Meta:
        model = PaymentMethod
        fields = ['payment_type', 'expiry_month', 'expiry_year', 'nickname', 'is_default']
        widgets = {
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
            'expiry_month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'expiry_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 2024, 'max': 2040}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Business Card'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Process card number
        card_number = self.cleaned_data.get('card_number', '').replace(' ', '')
        if card_number:
            instance.card_last_four = card_number[-4:]
            # Detect card brand
            if card_number.startswith('4'):
                instance.card_brand = 'Visa'
            elif card_number.startswith(('51', '52', '53', '54', '55')):
                instance.card_brand = 'Mastercard'
            elif card_number.startswith(('34', '37')):
                instance.card_brand = 'Amex'
            elif card_number.startswith('6011'):
                instance.card_brand = 'Discover'
            else:
                instance.card_brand = 'Card'
        
        if commit:
            instance.save()
        
        return instance

