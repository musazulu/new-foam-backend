from rest_framework import serializers
from .models import Order, OrderItem, DeliveryZone, OrderStatusHistory
from products.serializers import ProductListSerializer

class DeliveryZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryZone
        fields = ['id', 'name', 'province', 'city', 'delivery_fee', 
                 'estimated_days_min', 'estimated_days_max', 'is_active']

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'product_name', 'sku',
                 'quantity', 'unit_price', 'total_price', 'product_image',
                 'product_size', 'product_material']
        read_only_fields = fields
    
    def get_product_details(self, obj):
        if obj.product:
            return ProductListSerializer(obj.product, context=self.context).data
        return None

class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['old_status', 'new_status', 'notes', 'changed_by', 'changed_at']
        read_only_fields = fields

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    estimated_delivery = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'user', 'status', 'status_display', 'status_history',
                 'customer_name', 'customer_email', 'customer_phone',
                 'delivery_address', 'city', 'town', 'postal_code', 'delivery_instructions',
                 'subtotal', 'delivery_fee', 'tax_amount', 'total_amount', 'currency',
                 'payment_method', 'payment_method_display', 'payment_status', 'payment_reference',
                 'estimated_delivery_date', 'estimated_delivery', 'actual_delivery_date',
                 'tracking_number', 'delivery_partner',
                 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'user', 'created_at', 'updated_at']
    
    def get_estimated_delivery(self, obj):
        if obj.estimated_delivery_date:
            return obj.estimated_delivery_date.strftime('%B %d, %Y')
        return None

class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)

class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True, required=True)
    delivery_address = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    town = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    delivery_instructions = serializers.CharField(required=False, allow_blank=True)
    payment_method = serializers.ChoiceField(choices=[
        ('ecocash', 'EcoCash'),
        ('onemoney', 'OneMoney'),
        ('zipit', 'ZIPIT'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Visa/MasterCard'),
    ])
    
    customer_name = serializers.CharField(required=False)
    customer_email = serializers.EmailField(required=False)
    customer_phone = serializers.CharField(required=False)

class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('pending_payment', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ])
    notes = serializers.CharField(required=False, allow_blank=True)

class CartItemSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(min_value=1, required=True)

class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True, required=True)
    
    def validate(self, data):
        # Check if all products exist and are in stock
        from products.models import Product
        
        for item in data['items']:
            try:
                product = Product.objects.get(id=item['product_id'])
                if product.stock_quantity < item['quantity']:
                    raise serializers.ValidationError(
                        f"Product {product.name} has only {product.stock_quantity} items in stock"
                    )
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with ID {item['product_id']} does not exist")
        
        return data

class DeliveryFeeSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    province = serializers.CharField(required=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    
    def validate(self, data):
        try:
            zone = DeliveryZone.objects.get(city=data['city'], province=data['province'])
            data['delivery_fee'] = zone.delivery_fee
            data['estimated_days_min'] = zone.estimated_days_min
            data['estimated_days_max'] = zone.estimated_days_max
        except DeliveryZone.DoesNotExist:
            data['delivery_fee'] = 15.00  # Default fee
            data['estimated_days_min'] = 3
            data['estimated_days_max'] = 7
        
        return data