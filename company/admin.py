from django.contrib import admin
from .models import Company, PaymentMethod


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'city', 'state', 'usdot_number', 'created_at']
    list_filter = ['state', 'created_at']
    search_fields = ['name', 'email', 'usdot_number']


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['company', 'payment_type', 'card_brand', 'card_last_four', 'is_default']
    list_filter = ['payment_type', 'is_default']
    search_fields = ['company__name']

