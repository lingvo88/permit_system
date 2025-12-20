from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from company.models import Company

User = get_user_model()


class CustomerRegistrationForm(UserCreationForm):
    """Registration form for new customers."""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=True)
    
    # Company fields
    company_name = forms.CharField(max_length=200, required=True, label="Carrier Name")
    company_email = forms.EmailField(required=True, label="Company Email")
    address = forms.CharField(max_length=300, required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=2, required=True)
    zipcode = forms.CharField(max_length=10, required=True)
    company_phone = forms.CharField(max_length=20, required=True)
    usdot_number = forms.CharField(max_length=50, required=True, label="USDOT Number")
    fein = forms.CharField(max_length=50, required=False, label="FEIN")
    ifta_number = forms.CharField(max_length=50, required=False, label="IFTA Number")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data['phone']
        user.user_type = User.UserType.CUSTOMER
        
        if commit:
            # Create company first
            company = Company.objects.create(
                name=self.cleaned_data['company_name'],
                email=self.cleaned_data['company_email'],
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                zipcode=self.cleaned_data['zipcode'],
                phone=self.cleaned_data['company_phone'],
                usdot_number=self.cleaned_data['usdot_number'],
                fein=self.cleaned_data.get('fein', ''),
                ifta_number=self.cleaned_data.get('ifta_number', ''),
            )
            user.company = company
            user.save()
        
        return user


class LoginForm(AuthenticationForm):
    """Custom login form with better styling."""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username or Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EmployeeCreationForm(UserCreationForm):
    """Form for creating employee accounts (admin only)."""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=False)
    user_type = forms.ChoiceField(
        choices=[
            (User.UserType.EMPLOYEE, 'Employee'),
            (User.UserType.ADMIN, 'Admin'),
        ],
        initial=User.UserType.EMPLOYEE
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'user_type', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        user.user_type = self.cleaned_data['user_type']
        
        if commit:
            user.save()
        
        return user

