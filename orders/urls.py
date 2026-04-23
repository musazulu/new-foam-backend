from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'delivery-zones', views.DeliveryZoneViewSet, basename='delivery-zone')
router.register(r'', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/calculate/', views.CartView.as_view(), name='cart-calculate'),
    path('delivery-fee/', views.DeliveryZoneViewSet.as_view({'post': 'calculate_fee'}), name='delivery-fee'),
    path('stats/', views.OrderStatsView.as_view(), name='order-stats'),
]
