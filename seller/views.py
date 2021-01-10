import uuid
import pandas as pd
from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from api.models import Role, User
from seller.models import Seller, SellerDetail, Pincode, City
from seller.serializers import SellerDetailListSerializer, SellerStoreSerializer

# Create your views here.
class SellerRegisterView(APIView):

    permission_classes = (AllowAny,)
    parser_class = (FileUploadParser,)

    def prepare_pincodes(self, user_pincodes):
        pincodes = ''
        if user_pincodes:
            for pincode in user_pincodes.split(','):
                if str(pincode).strip():
                    pincodes= pincodes + ',' + str(pincode).strip()        
        return pincodes


    def post(self, request, format=None):
        data = request.data

        pincodes = self.prepare_pincodes(str(data.get('pincode_file')) + ',' + str(data.get('pincodes')))

        detail = dict(
            shop_name=data.get('shop_name'),
            address=data.get('address'),
            zip_code=data.get('zip_code', ''),
            city=data.get('city'),
            state=data.get('state'),

            gst=data.get('gst'),
            pancard=data.get('pancard'),
            adharcard=data.get('adharcard'),
            logo=data.get('logo'),
            board=data.get('board'),
            role=int(data.get('role',1)),
            minimum_order=data.get('minimum_order',0),
            category=int(data.get('category',1)),
            pincodes=pincodes,
            ifsc=data.get('ifsc'),
            bank_city=data.get('bank_city'),
            branch=data.get('branch'),
            account_holder=data.get('account_holder'),
            account_number=data.get('account_number'),
            bank=data.get('bank'),
            proof=data.get('proof')
        )

        try:
            detail = SellerDetail.objects.create(**detail)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # 2. User Create
        try:
            user = User.objects.create(
                email=data.get('email'),
                role=Role.SELLER,
                password=data.get('password',''),
                number=data.get('phone','')
            )
        except Exception as e:
            if detail:
                detail.delete()
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 3. Seller Create
        try:
            seller = Seller.objects.create(
                user=user,
                detail=detail
            )
        except Exception as e:
            if detail:
                detail.delete()
            if user:
                user.delete()
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. Token Generate
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "token": str(token.key)
        }
        return Response(data=response, status=status.HTTP_201_CREATED)


class SellerByPincodeView(APIView):
    permission_classes =[ AllowAny,]
    serializer_class = SellerDetailListSerializer


    def post(self, request):
        pincode = request.data['pincode']
        details = SellerDetail.objects.filter(
            zip_code=pincode
        )
        if details:
            serialized = self.serializer_class(details, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"detail": "No Seller For This"}, status=status.HTTP_204_NO_CONTENT)


class SellerStoreView(APIView):

    permission_classes = [ AllowAny, ]
    serializer_class = SellerStoreSerializer

    def post(self, request):
        identifier = request.data['identifier']
        try:
            store = SellerDetail.objects.get(
                seller__identifier__iexact=identifier
            )
        except Exception as e:
            return Response(data={'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serialized = self.serializer_class(store)
        return Response(data=serialized.data, status=status.HTTP_200_OK)


class IsDeliveryPossibleView(APIView):

    permission_classes = [AllowAny,]

    def post(self, request):
        delivery_pincode = request.data['delivery_pincode']
        seller = request.data['seller']
        response = {
            'is_deliverable': False,
            'charge': 0
        }
        sd = SellerDetail.objects.filter(seller__identifier=seller)
        if sd and delivery_pincode:
            servicable_pincodes = sd.last().pincodes
            if servicable_pincodes and delivery_pincode.get('pincode')['pincode'] in servicable_pincodes:
                response = {
                    'is_deliverable': True,
                    'charge': 100
                }
        return Response(data=response, status=status.HTTP_200_OK)

