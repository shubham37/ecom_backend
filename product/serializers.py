from rest_framework import  serializers
from product.models import Category, SubCategory, Product, \
    ShippingOptions, PopularCategory, ProductComment, ProductImages

from api.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = '__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
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

class ProductDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    order_count = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    attribute_options = serializers.SerializerMethodField()
    is_linked_product = serializers.SerializerMethodField()
    related_seller = serializers.SerializerMethodField()
    discount_str = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'images', 'view_count', 'mrp',
            'rating', 'review_count', 'final_price', 'shop_name', 'is_available',
            'attribute_options', 'is_linked_product', 'related_seller', 'reviews',
            'discount_str', 'order_count'
        ]

    def get_rating(self, obj):
        return 1
    
    def get_review_count(self, obj):
        reviews = ProductComment.objects.filter(product_id=obj.id).count()
        return reviews

    def get_order_count(self, obj):
        return 1

    def get_images(self, obj):        
        return ProductImagesSerializer(obj.images, many=True).data

    def get_reviews(self, obj):
        reviews = ProductComment.objects.filter(product_id=obj.id)
        if reviews:
            return ProductCommentSerializer(reviews, many=True).data
        return []

    def get_final_price(self, obj):
        return 1

    def get_shop_name(self, obj):
        return "Shop"

    def get_is_available(self, obj):
        return "In Stack"

    def get_attribute_options(self, obj):
        return {}

    def get_is_linked_product(self, obj):
        return False

    def get_related_seller(self, obj):
        return []

    def get_discount_str(self, obj):
        return "15 %"


class ProductTemplateSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    shop_name = serializers.SerializerMethodField()
    discount_str = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'image', 'view_count', 'mrp', 'category',
            'rating', 'final_price', 'shop_name', 'discount_str'
        ]

    def get_category(self, obj):
        return str(obj.category.name)
    
    def get_rating(self, obj):
        return 1

    def get_image(self, obj):
        return obj.thumbnail.image.name

    def get_final_price(self, obj):
        return 12
    
    def get_shop_name(self, obj):
        return "Shop Name"
    
    def get_discount_str(self, obj):
        return "15 %"


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
