from django.db import models


class Company(models.Model):
    """Company/Carrier information model."""
    
    name = models.CharField(max_length=200, verbose_name="Carrier Name")
    email = models.EmailField(verbose_name="Company Email")
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    usdot_number = models.CharField(max_length=50, verbose_name="USDOT Number")
    fein = models.CharField(max_length=50, blank=True, verbose_name="FEIN")
    ifta_number = models.CharField(max_length=50, blank=True, verbose_name="IFTA Number")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Companies"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}"


class PaymentMethod(models.Model):
    """Payment method for a company."""
    
    class PaymentType(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'Credit Card'
        DEBIT_CARD = 'debit_card', 'Debit Card'
        ACH = 'ach', 'ACH Bank Transfer'
        INVOICE = 'invoice', 'Invoice'
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.CREDIT_CARD
    )
    # Card info (masked for display)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=20, blank=True)  # Visa, Mastercard, etc.
    expiry_month = models.PositiveIntegerField(null=True, blank=True)
    expiry_year = models.PositiveIntegerField(null=True, blank=True)
    
    # For ACH
    bank_name = models.CharField(max_length=100, blank=True)
    account_last_four = models.CharField(max_length=4, blank=True)
    
    is_default = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        if self.payment_type == self.PaymentType.CREDIT_CARD:
            return f"{self.card_brand} ****{self.card_last_four}"
        elif self.payment_type == self.PaymentType.ACH:
            return f"{self.bank_name} ****{self.account_last_four}"
        return self.get_payment_type_display()
    
    def save(self, *args, **kwargs):
        # If this is set as default, unset other defaults
        if self.is_default:
            PaymentMethod.objects.filter(
                company=self.company,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

