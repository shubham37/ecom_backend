import datetime
import random
import string
import hashlib
import hmac
import base64
from dateutil.relativedelta import relativedelta
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from api.permissions import CustomPermission
from buyer.models import  UserAddress
from order.models import Order, OrderDetail, OrderReview
from product.models import ProductComment

from order.serializers import OrderSerializer, OrderDetailSerializer, \
    OrderReviewSerializer
from buyer.serializers import UserAddressSerializer


class OrderPlaceView(APIView):
    permission_classes =[IsAuthenticated, ]
    # serializer_class = ProductSearchSerializer

    def post(self, request):
        user = request.user
        data = request.data.get('orderDetail')

        price_detail = data.get('prices')
        products = list(data.get("products"))

        billing_address_id = int(data['billing_address']) if data['billing_address'] else -1
        try:
            address = UserAddress.objects.get(id=billing_address_id)
        except Exception as e:
            return Response(data={"error": e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        billing_address = UserAddressSerializer(address).data

        is_billing_same = data.get('is_shipping_same') == 'true'

        shipping_address = None
        if not is_billing_same:
            shipping_address_id = int(data['shipping_address']) if data['shipping_address'] else -1
            try:
                address = UserAddress.objects.get(id=shipping_address_id)
            except Exception as e:
                return Response(data={"error": e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            shipping_address = UserAddressSerializer(address).data

        track_dates = {
            "order_date": str(datetime.datetime.now()),
            "est_delivery_date": str(datetime.date.today() + relativedelta(days=2)),
            "shipping_date": str(datetime.date.today() + relativedelta(days=1)),
            "delivery_date": None
        }

        return_policy = {
            "max_return_date": '',
            "return_condition": '',
            "is_return": data.get('is_return', False)
        }

        payment_details = {
            "is_cod": data.get('is_cod') == 'true',
            "Is_online": data.get('is_online') == 'true',
            "transaction_id": "osd435fgogj43"
        }

        try:
            od = OrderDetail.objects.create(
                price_detail=price_detail,
                products=products,
                features={},
                shipping_address=shipping_address,
                is_billing_same=is_billing_same,
                billing_address=billing_address,
                track_dates=track_dates,
                return_policy=return_policy,
                payment_details=payment_details
            )
        except Exception as e:
            return Response(data={"error": e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        orderId = "OID" +''.join([random.choice(string.ascii_letters 
        + string.digits) for n in range(7)])
        order_dict = dict({
            'buyer':user,
            "orderId": orderId,
            'order_detail':od,
            "ordered_date": datetime.date.today(),
            "total_amount": price_detail['final'],
            "is_return_available": True,
            "is_cancel_available": False
        })

        try:
            order = Order.objects.create(**order_dict)
            return Response(data={'detail': "Order Placed", "orderId": order.orderId}, status=status.HTTP_201_CREATED)
        except Exception as e:
            od.delete()
            return Response(data={"error": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderViewSet(ViewSet):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_object(self, request, id):
        try:
            order = self.queryset.get(orderId=id)
            return order
        except Exception as e:
            return None

    # list order history
    def list(self, request):
        orders = self.queryset.filter(buyer=request.user)
        try:
            serialize = self.serializer_class(orders, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # retrieve order
    @action(detail=True, methods=['GET'])
    def order_detail(self, request, pk=None):
        order = self.get_object(request, pk)
        if order is not None:
            serialized = OrderDetailSerializer(order)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Please Check id", status=status.HTTP_404_NOT_FOUND)

    # add order review and product review
    @action(detail=False, methods=['POST'])
    def add_order_review(self, request):
        data = request.data

        try:
            order_review = OrderReview.objects.create(
                comment = data.get('comment',''),
                rating = int(data.get('rating',1))
            )
            order = self.get_object(request, data.get('orderId'))
            if order is not None:
                OrderReview.objects.filter(id=order.review_id).delete()
                order.review = order_review
                order.save()
                return Response(data={'detail': "Saved"}, status=status.HTTP_200_OK)
            else:
                order_review.delete()
                return Response(data={'detail': "Try Again"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentBack(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        print(request.data)

    def get(self, request):
        appId = settings.PAYMENT_APP_ID
        secretKey = settings.PAYMENT_SECRET_KEY
        customerEmail = request.user.email
        customerPhone = request.user.number
        orderId = "OID" +''.join([random.choice(string.ascii_letters 
        + string.digits) for n in range(7)])

        orderAmount = request.GET['orderAmount']

        data = "appId=" + appId + "&orderId=" + orderId + "&orderAmount=" + orderAmount + "&customerEmail=" + customerEmail + "&customerPhone=" + customerPhone + "&orderCurrency=INR";
        message = bytes(data).encode('utf-8')
        secret = bytes(secretKey).encode('utf-8')
        paymentToken = base64.b64encode(hmac.new(secret, message,digestmod=hashlib.sha256).digest())

        data = {}
        data.appId = appId
        data.secretKey = secretKey
        data.customerEmail = customerEmail
        data.customerPhone = customerPhone
        data.orderId = orderId
        data.notifyurl = 'https://localhost:8000/orders/payment/'
        data.returnurl = 'https://localhost:8000/orders/payment/'
        data.orderNote = 'Note'

        data.paymentOption = "card";
        data.card = {};
        # data.card.number = document.getElementById("card-num").value; 
        # data.card.expiryMonth = document.getElementById("card-mm").value;
        # data.card.expiryYear = document.getElementById("card-yyyy").value;
        # data.card.holder = document.getElementById("card-name").value;
        # data.card.cvv = document.getElementById("card-cvv").value;
        # CashFree.paySeamless(data);

        return paymentToken


