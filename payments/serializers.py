from rest_framework import serializers
from .models import Payment, PaymentWebhook, Refund

class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_number', 'user', 'user_email',
                 'amount', 'currency', 'payment_method', 'payment_method_display',
                 'status', 'status_display', 'payment_reference', 'transaction_id',
                 'phone_number', 'payment_date', 'card_last_four', 'card_brand',
                 'description', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = fields
    
    def get_order_number(self, obj):
        return obj.order.order_number if obj.order else None
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user else None

class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    payment_method = serializers.ChoiceField(choices=[
        ('ecocash', 'EcoCash'),
        ('onemoney', 'OneMoney'),
        ('zipit', 'ZIPIT'),
        ('bank_transfer', 'Bank Transfer'),
        ('card', 'Visa/MasterCard'),
    ])
    
    # For mobile money
    phone_number = serializers.CharField(required=False, allow_blank=True)
    
    # For card payments
    card_token = serializers.CharField(required=False, allow_blank=True)
    save_card = serializers.BooleanField(default=False)

class EcoCashPaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

class OneMoneyPaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)

class BankTransferPaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    reference_number = serializers.CharField(required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    bank_name = serializers.CharField(required=True)
    transaction_date = serializers.DateTimeField(required=True)

class CardPaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(required=True)
    token = serializers.CharField(required=True)
    save_card = serializers.BooleanField(default=False)

class PaymentWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentWebhook
        fields = ['id', 'payment_gateway', 'event_type', 'payload', 
                 'is_processed', 'processing_error', 'received_at']
        read_only_fields = fields

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'amount', 'currency', 'reason',
                 'status', 'refund_reference', 'processed_by',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']