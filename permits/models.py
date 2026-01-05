from django.db import models
from django.conf import settings
from company.models import Company, PaymentMethod
from fleet.models import Vehicle, Driver


class PermitRequest(models.Model):
    """Permit request submitted by customers."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Review'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        INVOICED = 'invoiced', 'Invoiced'
        CANCELLED = 'cancelled', 'Cancelled'
    
    # Auto-generated permit number
    permit_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Who submitted this
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='permit_requests'
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='submitted_permits'
    )
    
    # Assigned employee
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_permits'
    )
    
    # Load info
    load_description = models.CharField(max_length=200, verbose_name="Object/Load Description")
    load_make_model = models.CharField(max_length=200, blank=True, verbose_name="Make/Model")
    load_serial = models.CharField(max_length=200, blank=True, verbose_name="Serial#")
    origin_address = models.CharField(max_length=300)
    destination_address = models.CharField(max_length=300)
    
    # Equipment
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    truck = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permits_as_truck'
    )
    trailer = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='permits_as_trailer'
    )
    
    # Dimensions (overall)
    overall_length_ft = models.PositiveIntegerField(default=0)
    overall_length_in = models.PositiveIntegerField(default=0)
    overall_width_ft = models.PositiveIntegerField(default=0)
    overall_width_in = models.PositiveIntegerField(default=0)
    overall_height_ft = models.PositiveIntegerField(default=0)
    overall_height_in = models.PositiveIntegerField(default=0)
    gross_weight = models.PositiveIntegerField(default=0, help_text="Gross weight in lbs")
    
    # Load dimensions (overhang)
    front_overhang_ft = models.PositiveIntegerField(default=0)
    front_overhang_in = models.PositiveIntegerField(default=0)
    rear_overhang_ft = models.PositiveIntegerField(default=0)
    rear_overhang_in = models.PositiveIntegerField(default=0)
    left_overhang_ft = models.PositiveIntegerField(default=0)
    left_overhang_in = models.PositiveIntegerField(default=0)
    right_overhang_ft = models.PositiveIntegerField(default=0)
    right_overhang_in = models.PositiveIntegerField(default=0)
    
    # Axle configuration for this permit
    axle_configuration = models.PositiveIntegerField(default=1)  # Which config to use
    num_axles = models.PositiveIntegerField(default=0)
    is_legal_weight = models.BooleanField(default=False)
    
    # Payment
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Comments
    customer_comments = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True, help_text="Internal notes (not visible to customer)")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"#{self.permit_number} - {self.load_description}"
    
    def save(self, *args, **kwargs):
        if not self.permit_number:
            # Generate permit number
            last_permit = PermitRequest.objects.order_by('-id').first()
            if last_permit:
                try:
                    last_num = int(last_permit.permit_number.replace('#', ''))
                    self.permit_number = f"{last_num + 1}"
                except ValueError:
                    self.permit_number = "2100"
            else:
                self.permit_number = "2100"
        super().save(*args, **kwargs)
    
    @property
    def states_list(self):
        return list(self.states.values_list('state', flat=True))
    
    @property
    def states_display(self):
        return ", ".join(self.states_list)


class PermitState(models.Model):
    """States included in a permit request."""
    
    US_STATES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]
    
    permit = models.ForeignKey(
        PermitRequest,
        on_delete=models.CASCADE,
        related_name='states'
    )
    state = models.CharField(max_length=2, choices=US_STATES)
    travel_date = models.DateField(null=True, blank=True)
    route = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['state']
        unique_together = ['permit', 'state']
    
    def __str__(self):
        return f"{self.state} - {self.permit.permit_number}"


class PermitAxleDetail(models.Model):
    """Detailed axle information for a permit."""
    
    permit = models.ForeignKey(
        PermitRequest,
        on_delete=models.CASCADE,
        related_name='axle_details'
    )
    axle_number = models.PositiveIntegerField()
    spacing_ft = models.PositiveIntegerField(default=0)
    spacing_in = models.PositiveIntegerField(default=0)
    weight_lbs = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['axle_number']
        unique_together = ['permit', 'axle_number']


class PermitDocument(models.Model):
    """Documents attached to permit requests (permits, invoices, etc.)."""
    
    class DocumentType(models.TextChoices):
        PERMIT = 'permit', 'Permit'
        INVOICE = 'invoice', 'Invoice'
        OTHER = 'other', 'Other'
    
    permit = models.ForeignKey(
        PermitRequest,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER
    )
    file = models.FileField(upload_to='permit_documents/')
    filename = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename


class PermitComment(models.Model):
    """Comments/messages on permit requests."""
    
    permit = models.ForeignKey(
        PermitRequest,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    message = models.TextField()
    is_internal = models.BooleanField(default=False, help_text="Internal comments not visible to customer")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user} on #{self.permit.permit_number}"

