from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Address, OTPVerification


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ['avatar', 'date_of_birth', 'gender',
              'receive_email_notifications', 'receive_sms_notifications',
              'default_delivery_address', 'default_delivery_city']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ['email', 'username', 'first_name', 'last_name',
                    'is_verified', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_verified', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Zimbabwe Info', {
            'fields': ('phone_number', 'is_verified', 'city', 'province',
                       'currency_preference', 'marketing_opt_in')
        }),
        ('Stats', {
            'fields': ('total_orders', 'total_spent'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'province', 'is_default', 'address_type']
    list_filter = ['province', 'address_type', 'is_default']
    search_fields = ['user__email', 'name', 'city']
