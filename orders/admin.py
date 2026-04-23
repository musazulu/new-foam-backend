from django.contrib import admin
from .models import Order, OrderItem, DeliveryZone, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'sku', 'unit_price', 'total_price',
                       'product_size', 'product_material']
    fields = ['product', 'product_name', 'quantity', 'unit_price', 'total_price']


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['old_status', 'new_status', 'notes', 'changed_by', 'changed_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'customer_email', 'status',
                    'total_amount', 'payment_method', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    list_per_page = 25
    ordering = ['-created_at']

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Customer', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Delivery', {
            'fields': ('delivery_address', 'city', 'town', 'postal_code',
                       'delivery_instructions', 'estimated_delivery_date',
                       'actual_delivery_date', 'tracking_number', 'delivery_partner')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'delivery_fee', 'tax_amount', 'total_amount', 'currency')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'payment_reference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'province', 'delivery_fee',
                    'estimated_days_min', 'estimated_days_max', 'is_active']
    list_filter = ['province', 'is_active']
    search_fields = ['name', 'city']
    list_editable = ['delivery_fee', 'is_active']
