import uuid

from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from api.models import Role, User
from seller.models import Seller, SellerDetail, Pincode, City


# Create your views here.
class SellerRegisterView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Create Student.
        """
        data = request.data.get('formData')
        # 1. Detail Create
        bankCity = City.objects.filter(
            city_name__iexact=str(data.get('bank_city', ''))
        )
        if not bankCity.exists():
            bankCity = None
        else:
            bankCity = bankCity.last()

        pincode = Pincode.objects.filter(
            pincode=data.get('zip_code')
        )
        if not pincode.exists():
            pincode = None
        else:
            pincode = pincode.last()

        spd = dict(
            address=data.get('address',''),
            zip_code=pincode,
            gst=data.get('gst',''),
            pancard=data.get('pancard',None),
            adharcard=data.get('adharcard',None),
            logo=data.get('logo',None),
            board=data.get('board',None),
            role=data.get('role',1),
            minimum_order=data.get('minimum_order',''),
            category=data.get('category',1),
            ifsc=data.get('ifsc',''),
            bank_city=bankCity,
            branch=data.get('branch',''),
            account_holder=data.get('account_holder',''),
            account_number=data.get('account_number',''),
            bank=data.get('bank',''),
            proof=data.get('proof','')
        )

        try:
            detail = SellerDetail.objects.create(**spd)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # 2. User Create
        try:
            user = User.objects.create(
                email=data.get('userid'),
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
