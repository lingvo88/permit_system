from django.contrib import admin
from .models import PermitRequest, PermitState, PermitDocument, PermitComment, PermitAxleDetail


class PermitStateInline(admin.TabularInline):
    model = PermitState
    extra = 0


class PermitDocumentInline(admin.TabularInline):
    model = PermitDocument
    extra = 0


@admin.register(PermitRequest)
class PermitRequestAdmin(admin.ModelAdmin):
    list_display = ['permit_number', 'company', 'load_description', 'status', 'submitted_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['permit_number', 'company__name', 'load_description']
    inlines = [PermitStateInline, PermitDocumentInline]
    readonly_fields = ['permit_number', 'created_at', 'updated_at']


@admin.register(PermitDocument)
class PermitDocumentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'permit', 'document_type', 'uploaded_by', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']

