# products/serializers.py
from rest_framework import serializers
from django.conf import settings
from .models import Category, Product, ProductImage, ProductReview, ProductLike

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'alt_text', 'is_primary', 'order']
    
    def get_image_url(self, obj):
        # Use direct URL field if available
        if obj.image_url:
            return obj.image_url
        # Fall back to uploaded file
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return f"{settings.MEDIA_URL}{obj.image}"
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description',
            'category', 'category_name', 'category_slug',
            'price_usd', 'price_zwl', 'discount_percentage',
            'discounted_price_usd', 'discounted_price_zwl',
            'average_rating', 'total_ratings', 'total_likes',
            'total_sold', 'primary_image', 'is_featured',
            'is_sponsored', 'is_in_stock', 'size', 'material',
            'color', 'dimensions', 'weight', 'stock_quantity',
            'low_stock_threshold', 'created_at', 'updated_at'
        ]
        read_only_fields = ['discounted_price_usd', 'discounted_price_zwl']
    
    def get_primary_image(self, obj):
        try:
            primary_image = obj.images.filter(is_primary=True).first()
            if not primary_image:
                primary_image = obj.images.first()
            
            if primary_image and primary_image.image:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(primary_image.image.url)
                return f"{settings.MEDIA_URL}{primary_image.image}"
        except Exception as e:
            print(f"Error getting primary image: {e}")
        
        return None

class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    description = serializers.CharField()
    
    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            'description', 'sku', 'published_at', 'images'
        ]

class ProductReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    comment = serializers.CharField(allow_blank=True, required=False, default='')

    class Meta:
        model = ProductReview
        fields = [
            'id', 'user', 'user_name', 'user_email', 'rating', 'title',
            'comment', 'helpful_votes', 'is_approved', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'is_approved', 'helpful_votes']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ['id', 'user', 'product', 'created_at']

class ProductSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2)
    rating = serializers.DecimalField(required=False, max_digits=3, decimal_places=1)
    size = serializers.CharField(required=False, allow_blank=True)
    material = serializers.CharField(required=False, allow_blank=True)
    sort_by = serializers.CharField(required=False, default='relevance')
    page = serializers.IntegerField(required=False, default=1, min_value=1)
    page_size = serializers.IntegerField(required=False, default=20, min_value=1, max_value=100)