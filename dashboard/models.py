from django.db import models
from django.conf import settings


class EmailLog(models.Model):
    """Log of emails sent to customers."""
    
    permit = models.ForeignKey(
        'permits.PermitRequest',
        on_delete=models.CASCADE,
        related_name='email_logs',
        null=True,
        blank=True
    )
    sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField()
    attachments = models.JSONField(default=list)  # List of attachment filenames
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"Email to {self.recipient_email}: {self.subject}"


class EmailAttachment(models.Model):
    """Attachments for emails."""
    
    email_log = models.ForeignKey(
        EmailLog,
        on_delete=models.CASCADE,
        related_name='attachment_files'
    )
    file = models.FileField(upload_to='email_attachments/')
    filename = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

