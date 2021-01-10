import uuid
from django.db.models import Q,Count

from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from api.permissions import CustomPermission
from product.models import Product, Category, SubCategory, ShippingOptions, \
    PopularCategory, ProductComment, FeatureGroup, Feature, FilterFeature, AllFeature
from product.serializers import CategorySerializer, SubCategorySerializer, \
    ShippingOptionSerializer, PopularCategorySerializer, ProductDetailSerializer, \
        ProductTemplateSerializer, ProductCommentSerializer


def prepared_filters(products):
    filters = []
    feature_group_ids = products.values_list('product_features', flat=True)
    if feature_group_ids:
        features = list(
            set(
                FeatureGroup.objects.filter(
                    id__in=feature_group_ids
                ).values_list('features__name', flat=True)
            )
        )

        available_filters = list(
            set(
                FilterFeature.objects.filter(
                    is_filter=True
                ).values_list(
                    'feature__key', flat=True
                )
            )
        )
        for feature in features:
            if feature in available_filters:
                values = Feature.objects.filter(name__icontains=feature).values_list('value', flat=True)
                if values:
                    option = {
                        "has_data": True,
                        'feature': str(feature).title(),
                        'values': list(set(values))
                    }
                    filters.append(option)
    return filters


class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductTemplateSerializer

    def get_object(self, request, id):
        try:
            product = self.queryset.get(id=id)
            return product
        except Exception as e:
            return None

    def retrieve(self, request, pk=None):
        product = self.get_object(request, pk)
        if product is not None:
            serialized = ProductDetailSerializer(product)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Try Again", status=status.HTTP_204_NO_CONTENT)

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
        cat =  request.GET.get('category','')
        sub_category =  request.GET.get('sub_category','')
        seller = request.GET.get('seller','')
        filters = {}

        if cat:
            filters.update({
                'category__name__iexact': cat
            })
        
        if sub_category:
            filters.update({
                'sub_category__name__iexact': sub_category
            })
        if seller:
            filters.update({
                'seller__identifier__iexact': seller
            })
        products = self.queryset.filter(**filters)
        if products:

            # Preparing Features
            filters= prepared_filters(products)
            serialize = self.serializer_class(products, many=True)
            return Response(
                data={
                    'products': serialize.data,
                    'filters': filters
                }, status=status.HTTP_200_OK)
        return Response(data={'detail': 'no data'}, status=status.HTTP_204_NO_CONTENT)


class ProductCommentView(APIView):
    permission_classes =[AllowAny, ]
    serializer_class = ProductCommentSerializer
    queryset = ProductComment.objects.all()

    def get(self, request):
        comments = self.queryset
        if comments.exists():
            serialized = self.serializer_class(comments, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Try Again", status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        detail = request.data
        try:
            data = detail.get('detail')
            data.update({
                'product_id': int(detail.get('product_id'))
            })
            review = ProductComment.objects.create(**data)
            return Response(data={'detail': "Saved"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

        shiping_options = ShippingOptions.objects.filter(product_id=product_id).values('shipping_option')
        serialize = self.serializer_class(shiping_options, many=True)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


class SearchView(APIView):
    permission_classes =[AllowAny, ]
    serializer_class = ProductTemplateSerializer

    def get(self, request):
        search_term = str(request.GET.get('values', '')).strip()
        if search_term:
            products = Product.objects.filter(title__icontains=search_term)
            if products:
                filters= prepared_filters(products)
                serialize = self.serializer_class(products, many=True)
                return Response(
                    data={
                        'products': serialize.data,
                        'filters': filters
                    }, status=status.HTTP_200_OK)
            return Response(data={"detail":'No Data'}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"detail":'Query Should Not Blank'}, status=status.HTTP_400_BAD_REQUEST)


class MultiSearchView(APIView):
    permission_classes =[AllowAny, ]
    serializer_class = ProductTemplateSerializer

    def get(self, request):
        products = request.GET.get('values', '')
        products = list(map(lambda x: str(x).strip(), products.split(',')))
        product_ids = []
        for product in products:
            if product:
                ids = Product.objects.filter(title__icontains=product).values_list('id', flat=True)
                product_ids.extend(ids)
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
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
