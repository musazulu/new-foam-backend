from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid

class User(AbstractUser):
    """Custom user model with additional fields for Zimbabwe"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True, region='ZW')
    is_verified = models.BooleanField(default=False)
    
    # Zimbabwe-specific address fields
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Preferences
    currency_preference = models.CharField(max_length=3, default='USD')
    marketing_opt_in = models.BooleanField(default=False)
    
    # Stats
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Timestamps
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email or self.username

class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    
    # Communication preferences
    receive_email_notifications = models.BooleanField(default=True)
    receive_sms_notifications = models.BooleanField(default=True)
    receive_order_updates = models.BooleanField(default=True)
    
    # Default delivery address
    default_delivery_name = models.CharField(max_length=200, blank=True)
    default_delivery_phone = models.CharField(max_length=20, blank=True)
    default_delivery_address = models.TextField(blank=True)
    default_delivery_city = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"

class Address(models.Model):
    """User addresses for delivery"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    
    # Address fields
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Type
    is_default = models.BooleanField(default=False)
    address_type = models.CharField(max_length=20, choices=[
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ], default='home')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.city}"

class OTPVerification(models.Model):
    """OTP storage for phone/email verification"""
    OTP_TYPE_CHOICES = [
        ('email_verification', 'Email Verification'),
        ('phone_verification', 'Phone Verification'),
        ('password_reset', 'Password Reset'),
        ('login', 'Login'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_type = models.CharField(max_length=20, choices=OTP_TYPE_CHOICES)
    otp_code = models.CharField(max_length=6)
    recipient = models.CharField(max_length=255)  # Email or phone number
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'otp_type', 'is_used']),
        ]
    
    def __str__(self):
        return f"OTP for {self.recipient} - {self.otp_type}"