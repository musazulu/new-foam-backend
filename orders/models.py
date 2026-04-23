from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

User = get_user_model()

class Order(models.Model):
    """Customer order model"""
    ORDER_STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('ecocash', 'EcoCash'),
        ('onemoney', 'OneMoney'),
        ('zipit', 'ZIPIT'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Visa/MasterCard'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Order status
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending_payment')
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Delivery information (Zimbabwe specific)
    delivery_address = models.TextField()
    city = models.CharField(max_length=100)
    town = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    delivery_instructions = models.TextField(blank=True)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    currency = models.CharField(max_length=3, default='USD')
    
    # Payment information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Delivery tracking
    estimated_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    delivery_partner = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXXX
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__contains=date_str).count()
            self.order_number = f"ORD-{date_str}-{last_order + 1:05d}"
        
        # Calculate totals if not set
        if not self.total_amount and self.subtotal:
            self.total_amount = self.subtotal + self.delivery_fee + self.tax_amount
        
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='order_items')
    product_name = models.CharField(max_length=200)  # Store product name at time of purchase
    sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Store product details at time of purchase
    product_image = models.CharField(max_length=500, blank=True)
    product_size = models.CharField(max_length=50, blank=True)
    product_material = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
    
    def save(self, *args, **kwargs):
        # Calculate total price
        if not self.total_price:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class DeliveryZone(models.Model):
    """Delivery zones for Zimbabwe"""
    PROVINCE_CHOICES = [
        ('harare', 'Harare'),
        ('bulawayo', 'Bulawayo'),
        ('manicaland', 'Manicaland'),
        ('mashonaland_central', 'Mashonaland Central'),
        ('mashonaland_east', 'Mashonaland East'),
        ('mashonaland_west', 'Mashonaland West'),
        ('masvingo', 'Masvingo'),
        ('matabeleland_north', 'Matabeleland North'),
        ('matabeleland_south', 'Matabeleland South'),
        ('midlands', 'Midlands'),
    ]
    
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=100)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_days_min = models.PositiveIntegerField(default=1)
    estimated_days_max = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['city', 'province']
    
    def __str__(self):
        return f"{self.city}, {self.get_province_display()}"

class OrderStatusHistory(models.Model):
    """Track order status changes"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.order.order_number}: {self.old_status} → {self.new_status}"