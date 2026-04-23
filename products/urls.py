# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),

    # Review endpoints - product pk is uuid, review pk is int
    path('products/<uuid:pk>/reviews/', views.ProductReviewViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='product-reviews'),
    path('products/<uuid:product_pk>/reviews/<int:pk>/', views.ProductReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='product-review-detail'),
    path('reviews/<int:pk>/helpful/', views.ProductReviewViewSet.as_view({
        'post': 'helpful'
    }), name='review-helpful'),
]
