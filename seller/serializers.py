from rest_framework import serializers
from seller.models import SellerDetail
from product.models import Product
from product.serializers import ProductTemplateSerializer


class SellerDetailListSerializer(serializers.ModelSerializer):
    identifier = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()

    class Meta:
        model = SellerDetail
        fields = ['shop_name', 'address', 'category', 'role', 'identifier', 'logo', 'minimum_order']

    def get_identifier(self, obj):
        return obj.seller_set.last().identifier

    def get_logo(self, obj):
        return obj.logo.name



class SellerStoreSerializer(serializers.ModelSerializer):
    identifier = serializers.SerializerMethodField()
    # specialized_category = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    board = serializers.SerializerMethodField()

    class Meta:
        model = SellerDetail
        fields = ['shop_name', 'address',  'identifier', 'logo', 'board', 'products']

    def get_identifier(self, obj):
        return obj.seller_set.last().identifier

    # def get_specialized_category(self, obj):
    #     return []
    def get_logo(self, obj):
        if obj.logo:
            return obj.logo.name
        return ''

    def get_board(self, obj):
        if obj.board:
            return obj.board.name
        return ''

    def get_products(self, obj):
        products = Product.objects.filter(seller__detail=obj)
        if products:
            serialized = ProductTemplateSerializer(products, many=True)
            return serialized.data
        return []


