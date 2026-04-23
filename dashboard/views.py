from rest_framework import generics, permissions
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from accounts.models import User
from products.models import Product

class DashboardStatsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Simple stats
        stats = {
            'today_orders': Order.objects.filter(created_at__date=today).count(),
            'weekly_orders': Order.objects.filter(created_at__date__gte=week_ago).count(),
            'monthly_orders': Order.objects.filter(created_at__date__gte=month_ago).count(),
            'total_products': Product.objects.count(),
            'total_customers': User.objects.count(),
            'out_of_stock': Product.objects.filter(stock_quantity=0).count(),
        }
        
        return Response(stats)

class SalesTrendView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Simple implementation for now
        return Response({'message': 'Sales trend endpoint - to be implemented'})

class ProductAnalyticsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        # Simple implementation for now
        return Response({'message': 'Product analytics endpoint - to be implemented'})
