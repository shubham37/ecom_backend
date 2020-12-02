from rest_framework import  serializers
from product.models import Category, SubCategory, Product, ShippingOptions, PopularCategory
# , PriceRangeOptions, BrangeOptions


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PopularCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PopularCategory
        fields = '__all__'
        depth = 1

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
        depth = 1


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 3

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 2

class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOptions
        fields = '__all__'
        depth = 1
