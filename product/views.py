import uuid
from django.db.models import Q,Count

from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from api.permissions import CustomPermission
from product.models import Product, Category, SubCategory, ProductOptions, ShippingOptions, \
    PriceRangeOptions, BrandsOptions, PopularCategory
from product.serializers import CategorySerializer, SubCategorySerializer, \
    ProductSearchSerializer, ProductSerializer, ShippingOptionSerializer, \
        PopularCategorySerializer


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer

    def get_object(self, request, id):
        availability = self.queryset.filter(id=id)
        return availability

    # product by id
    def retrieve(self, request, pk=None):
        product = self.get_object(request, pk)
        if product.exists():
            serialized = self.serializer_class(product.last())
            # We should add other available options
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Please Check uuid", status=status.HTTP_204_NO_CONTENT)

    # popular & most viewed
    @action(detail=False, methods=['GET'])
    def popular_viewed(self, request):
        viewed_products = self.queryset.order_by('-view_count')
        # popular_products = self.queryset.annotate(popular=Count('comments')).order_by('-popular_count')
        popular_products =[]
        response = {
            'viewed' : [],
            'popular': []
        }

        if viewed_products:
            serialized_viewed = self.serializer_class(viewed_products, many=True)
            response.update({'viewed': serialized_viewed.data})
            response.update({'popular': serialized_viewed.data})

        # if popular_products:
        #     serialized_popular = self.serializer_class(popular_products, many=True)
        #     response.update({'popular': serialized_popular.data})

        return Response(data=response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def byCategory(self, request):
        cat =  request.GET.get('name')
        category = set(Category.objects.filter(name__iexact=cat).values_list('id'))
        products = self.queryset.filter(category_id__in=category)
        if products:
            serialize = self.serializer_class(products, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': 'no data'}, status=status.HTTP_204_NO_CONTENT)



class ShippingOptionViewSet(ViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ShippingOptionSerializer

    def get_object(self, request, id):
        availability = self.queryset.filter(id=id)
        return availability
    
    def retrieve(self, request, id):
        product_id = id
        user = request.user

        shiping_options = ProductOptions.objects.filter(product_id=product_id).values('shipping_option')
        serialize = self.serializer_class(shiping_options, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class SearchView(APIView):
    permission_classes =[AllowAny, ]
    serializer_class = ProductSearchSerializer

    def get(self, request):
        print(request.GET)
        category = request.GET.get('category', 0)
        sub_category = request.GET.get('subcategory', 0)

        search_term = request.GET.get('query', '') # This will compare against title, tag

        price_range = request.GET.get('price_range', '')
        brand = request.GET.get('brand', '')
        quality = request.GET.get('quantity', '')
        discounts = request.GET.get('discount', '')
        feature_name = request.GET.get('feature_name', '')
        feature_value = request.GET.get('feature_value', '')


        value_filter = {
         'category_id': category,
         'sub_category_id': sub_category
        }


        # query = (
        #     Q(category_id=category) |
        #     Q(sub_category_id=sub_category) |
        #     Q(title__iexact__contain=search_term) |
        #     Q(tags__title__iexact=search_term)
        # )

        products = Product.objects.filter(**value_filter)
        if products:
            serialize = self.serializer_class(products, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={"detail":'No Data'}, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ViewSet):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

    def get_object(self, request, id):
        category = Category.objects.filter(id=id)
        return category

    # list of Category
    def list(self, request):
        context = {
            "is_success": False,
            "categories": []
        }
        if self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            context.update({
                "is_success": True,
                "categories": serialize.data
            })

        return Response(context, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def byName(self, request):
        cat = request.GET.get('name')
        category = self.queryset.filter(name__iexact=cat)
        if category:
            serialize = self.serializer_class(category.last())
            return Response(serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Data Exist"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['GET'])
    def top(self, request):
        context = {
            "top_categories": []
        }
        cats = self.queryset.filter(is_top_category=True)
        if cats.exists():
            serialize = self.serializer_class(cats, many=True)
            context.update({
                "top_categories": serialize.data
            })
        return Response(context, status=status.HTTP_200_OK)

class PopularCategoryViewSet(ViewSet):
    queryset = PopularCategory.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PopularCategorySerializer

    def get_object(self, request, id):
        category = Category.objects.filter(id=id)
        return category

    # list of Category
    def list(self, request):
        context = {
            "popular_categories": []
        }
        if self.queryset.exists():
            serialize = self.serializer_class(self.queryset[:4], many=True)
            context.update({
                "popular_categories": serialize.data
            })

        return Response(context, status=status.HTTP_200_OK)


class SubCategoryViewSet(ViewSet):
    queryset = SubCategory.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SubCategorySerializer

    def get_object(self, request, id):
        subCategory = SubCategory.objects.filter(id=id)
        return subCategory

    # list of cities
    def list(self, request):
        context = {
            "is_success": False,
            "sub_categories": []
        }
        if self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            context.update({
                "is_success": True,
                "sub_categories": serialize.data
            })

        return Response(context, status=status.HTTP_200_OK)

    # SubCategory with id
    def retrieve(self, request, pk=None):
        subCategory = self.get_object(request, pk)
        if subCategory.exists():
            serialized = self.serializer_class(subCategory.last())
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(" No SubCategory", status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def byCategory(self, request):
        cat =  request.GET.get('name')
        category = set(Category.objects.filter(name__iexact=cat).values_list('id'))
        products = self.queryset.filter(cat_id__in=category)
        if products:
            serialize = self.serializer_class(products, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': 'no data'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'])
    def get_subcategory_by_category(self, request, pk=None):
        sub_categories = self.queryset.filter(cat_id=pk)
        if sub_categories.exists():
            serialized = self.serializer_class(sub_categories, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("StateCategory Has No SubCategory.", status=status.HTTP_404_NOT_FOUND)
