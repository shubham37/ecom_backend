import uuid

from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from api.models import Role, User
from seller.models import Seller, SellerPersonalDetail, SellerBankDetail, \
    SellerBusinessDetail, Pincode, City


# Create your views here.
class SellerRegisterView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Create Student.
        """
        try:
            info_data =  request.data.get('info')
            business_data =  request.data.get('business')
            bank_data =  request.data.get('bank')

            # 1. User Create
            token = uuid.uuid4()
            user = User.objects.create(
                email=info_data.get('userid'),
                role=Role.SELLER
            )

            # 2. Address Create
            spd = dict(
                user_id=user.id,
                password=info_data.get('password'),
                address=info_data.get('address'),
                city=City.objects.get(
                    id=int(info_data.get('city'))
                ),
                zip_code=Pincode.objects.get(
                    id=int(info_data.get('pincode'))
                )
            )

            spd = SellerPersonalDetail.objects.create(**spd)

            # 3. Bank Details
            sbd = dict(
                ifsc=bank_data.get('ifsc'),
                branch=bank_data.get('branch'),
                acc_holder=bank_data.get('account_holder'),
                acc_number=bank_data.get('account_number'),
                bank_name=bank_data.get('bank'),
                bank_proof=bank_data.get('proof')
            )

            sbd = SellerBankDetail.objects.create(**sbd)


            # 4. busines Details
            sbsd = dict(
                gst=business_data.get('gst'),
                role=business_data.get('role'),
                minimum_home_delivery=business_data.get('minimum_order'),
                shop_board=business_data.get('board'),
                shop_category=business_data.get('category'),
                pancard=business_data.get('pancard'),
                adharCard=business_data.get('adharCard')
            )

            sbsd = SellerBusinessDetail.objects.create(**sbsd)

            # 5. Token Create
            seller = Seller.objects.create(
                bank_detail_id=sbd.id,
                business_detail_id=sbsd.id,
                personal_detail_id=spd.id
            )
            token, _ = Token.objects.get_or_create(user=user)
            response = {
                "token": str(token.key)
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
