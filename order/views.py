from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from api.permissions import CustomPermission
from order.models import Order, OrderDetail
from order.serializers import OrderSerializer
from product.models import ProductComment


class OrderPlaceView(APIView):
    permission_classes =[CustomPermission, ]
    # serializer_class = ProductSearchSerializer

    def post(self, request):
        user = request.user
        data = request.data

        price = {
            "mrp": data.get('mrp'),
            "discount": data.get('discount', 0),
            "discount_type": data.get('discount_type',''),
            "tax": data.get('tax',0),
            "shipping_price": data.get('shipping_price',0),
            "paid_amount": data.get('payable_amount')
        }

        billing_address = {
            "full_name": data.get('full_name', ''),
            "mobile": data.get('mobile', ''),
            "pincode": data.get('pincode', ''),
            "locality": data.get('locality', ''),
            "address": data.get('address', ''),
            "landmark": data.get('landmark', ''),
            "alternate_mobile": data.get('alternate_mobile', ''),
            "add_type": data.get('add_type',1)
        }

        is_billing_same = data.get('is_billing-same', True)

        shipping_address = None
        if not is_billing_same:
            shipping_address = {
                "full_name": data.get('full_name', ''),
                "mobile": data.get('mobile', ''),
                "pincode": data.get('pincode', ''),
                "locality": data.get('locality', ''),
                "address": data.get('address', ''),
                "landmark": data.get('landmark', ''),
                "alternate_mobile": data.get('alternate_mobile', ''),
                "add_type": data.get('add_type',1)
        }

        track_dates = {
            "order_date": data.get('order_date', ''),
            "est_delivery_date": data.get('est_delivery_date', ''),
            "shipping_date": data.get('shipping_date', ''),
            "delivery_date": data.get('delivery_date', '')
        }

        return_policy = {
            "max_return_date": '',
            "return_condition": '',
            "is_return": data.get('is_return', False)
        }       

        payment_option = {
            "card_name": data.get('card_name',''), 
            "card_number": data.get('card_number',''),
            "card_valid_year": data.get('card_valid_year',''),
            "card_valid_month": data.get('card_valid_month','')
        }

        od = OrderDetail.objects.create(
            price=price,
            features={},
            shipping_address=shipping_address,
            is_billing_same=is_billing_same,
            billing_address=billing_address,
            track_dates=track_dates,
            return_policy=return_policy,
            payment_option=payment_option
        )

        if od:

            order_dict = dict({
                'buyer':user,
                'product_id':data.get('product_id'),
                'order_detail':od,
                "ordered_date": data.get('ordered_date',''),
                "is_return_available": data.get('is_return_available',''),
                "is_cancel_available": data.get('is_cancel_available',''),
                "track_status": data.get('track_status',''),
                "comment": data.get('comment',''),
                "rating": data.get('rating',''),
                "quantity": data.get('quantity',''),
                "measurement_parameter": data.get('measurement_parameter','')
            })

            o = Order.objects.create(**order_dict)

            return Response(data={'detail': "Order Successfull Placed"}, status=200)
        return Response(data={'detail': "Please Try Again"}, status=400)


class OrderViewSet(ViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_object(self, request, id):
        order = self.queryset.filter(id=id)
        return order

    # list order history
    def list(self, request):
        orders = self.queryset.filter(buyer=request.user)
        try:
            serialize = self.serializer_class(orders, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # retrieve order
    def retrieve(self, request, pk=None):
        order = self.get_object(request, pk)
        if order.exists():
            serialized = self.serializer_class(order.last())
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Please Check id", status=status.HTTP_404_NOT_FOUND)

    # add order review and product review
    @action(detail=True, methods=['POST'])
    def add_order_review(self, request, id):
        order = self.get_object(request, id)
        if order.exists():
            order.update(
                comments = request.data.get('comment',''),
                rating = request.data.get('rating',1)
            )

            product = order.last().product
            user=request.user
            pro, _ = ProductComment.objects.get_or_create(product=product, user=user)
            pro.comment = request.data.get('comment','')
            pro.rating = request.data.get('rating',1)
            pro.save()
            return Response(data={'detail': "saved"}, status=status.HTTP_200_OK)
        return Response(data={'error':"No Order Found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




