from rest_framework import serializers
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta
from products.models import Product
from orders.models import Order
from accounts.models import User
from payments.models import Payment

class DashboardStatsSerializer(serializers.Serializer):
    # Today's stats
    today_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    today_orders = serializers.IntegerField()
    today_new_customers = serializers.IntegerField()
    
    # Weekly stats
    weekly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    weekly_orders = serializers.IntegerField()
    weekly_aov = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    # Monthly stats
    monthly_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    monthly_orders = serializers.IntegerField()
    monthly_aov = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    # Overview
    total_products = serializers.IntegerField()
    out_of_stock_products = serializers.IntegerField()
    low_stock_products = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    
    # Recent orders
    recent_orders = serializers.ListField()
    
    # Top products
    top_products = serializers.ListField()
    
    # Payment methods distribution
    payment_methods = serializers.DictField()

class SalesTrendSerializer(serializers.Serializer):
    period = serializers.CharField()
    labels = serializers.ListField()
    revenue = serializers.ListField()
    orders = serializers.ListField()
    customers = serializers.ListField()

class TopProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    product_name = serializers.CharField()
    total_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    stock_quantity = serializers.IntegerField()

class RecentOrderSerializer(serializers.Serializer):
    order_number = serializers.CharField()
    customer_name = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()