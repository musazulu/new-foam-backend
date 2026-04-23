from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardStats(models.Model):
    """Store aggregated dashboard statistics for quick access"""
    date = models.DateField(unique=True)
    
    # Sales stats
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Customer stats
    new_customers = models.PositiveIntegerField(default=0)
    returning_customers = models.PositiveIntegerField(default=0)
    
    # Product stats
    top_selling_product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    low_stock_products = models.PositiveIntegerField(default=0)
    
    # Payment stats
    successful_payments = models.PositiveIntegerField(default=0)
    failed_payments = models.PositiveIntegerField(default=0)
    
    # Delivery stats
    orders_delivered = models.PositiveIntegerField(default=0)
    average_delivery_time = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    calculated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Dashboard Statistics"
    
    def __str__(self):
        return f"Stats for {self.date}"