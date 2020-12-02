from rest_framework import  serializers
from buyer.models import UserAddress, Card, Buyer, BuyerWishlist


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
        depth = 3


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'
        depth = 1


class BuyerWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerWishlist
        fields = '__all__'
        depth = 2