from django.contrib import admin
from .models import EmailLog, EmailAttachment


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient_email', 'subject', 'sent_by', 'permit', 'sent_at']
    list_filter = ['sent_at']
    search_fields = ['recipient_email', 'subject']
    readonly_fields = ['sent_at']

