from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'user_type', 'company', 'is_active']
    list_filter = ['user_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'company')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'company')}),
    )
    
    def delete_model(self, request, obj):
        """Prevent users from deleting themselves."""
        if obj == request.user:
            messages.error(request, "You cannot delete your own account!")
            return
        super().delete_model(request, obj)
    
    def delete_queryset(self, request, queryset):
        """Prevent users from deleting themselves in bulk actions."""
        if request.user in queryset:
            messages.error(request, "You cannot delete your own account!")
            # Remove current user from queryset
            queryset = queryset.exclude(pk=request.user.pk)
        if queryset.exists():
            super().delete_queryset(request, queryset)
    
    def has_delete_permission(self, request, obj=None):
        """Check if user can delete this object."""
        if obj and obj == request.user:
            return False
        return super().has_delete_permission(request, obj)
