from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    path('sales-trend/', views.SalesTrendView.as_view(), name='sales-trend'),
    path('product-analytics/', views.ProductAnalyticsView.as_view(), name='product-analytics'),
]
