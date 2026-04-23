from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductReview, ProductLike


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'image_preview', 'alt_text', 'is_primary', 'order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px; border-radius:4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


class ProductReviewInline(admin.StackedInline):
    model = ProductReview
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', 'rating', 'title', 'comment', 'is_approved', 'helpful_votes']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'price_usd', 'stock_quantity',
                    'average_rating', 'is_featured', 'is_in_stock', 'created_at']
    list_filter = ['category', 'is_featured', 'is_in_stock', 'is_sponsored', 'created_at']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['average_rating', 'total_ratings', 'total_likes', 'total_sold', 'created_at', 'updated_at']
    inlines = [ProductImageInline, ProductReviewInline]
    list_editable = ['is_featured', 'is_in_stock']
    list_per_page = 25

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'category')
        }),
        ('Pricing', {
            'fields': ('price_usd', 'price_zwl', 'discount_percentage')
        }),
        ('Inventory', {
            'fields': ('sku', 'stock_quantity', 'low_stock_threshold', 'is_in_stock')
        }),
        ('Specifications', {
            'fields': ('size', 'material', 'color', 'dimensions', 'weight')
        }),
        ('Marketing', {
            'fields': ('is_featured', 'is_sponsored', 'published_at')
        }),
        ('Statistics (read-only)', {
            'fields': ('average_rating', 'total_ratings', 'total_likes', 'total_sold'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'category')
        }),
        ('Pricing', {
            'fields': ('price_usd', 'price_zwl', 'discount_percentage')
        }),
        ('Inventory', {
            'fields': ('sku', 'stock_quantity', 'low_stock_threshold', 'is_in_stock')
        }),
        ('Specifications', {
            'fields': ('size', 'material', 'color', 'dimensions', 'weight')
        }),
        ('Marketing', {
            'fields': ('is_featured', 'is_sponsored')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return []


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__email', 'title', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'product__name']
