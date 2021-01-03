from rest_framework import serializers
from order.models import Order, OrderDetail, OrderReview


class OrderReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    review = OrderReviewSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'orderId', 'ordered_date', 'total_amount',
            'is_return_available', 'is_cancel_available',
            'review', 'current_status'
        ]

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

