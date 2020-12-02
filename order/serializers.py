from rest_framework import serializers
from order.models import Order, OrderDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__'
        depth =1

