import uuid

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions

from api.permissions import CustomPermission
from api.models import User, Role, Pincode
from buyer.models import Buyer, UserAddress, Card, BuyerWishlist
from buyer.serializers import UserAddressSerializer, CardSerializer, \
    BuyerSerializer, BuyerWishlistSerializer
from product.models import Product


# call after buyer entered otp
class BuyerSignup(APIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        user = request.user
        if user:
            try:
                buyer = Buyer.objects.create(user=user)
                return Response(data={'detail':' Account Created Successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={'detail':'Please Try again'}, status=status.HTTP_401_UNAUTHORIZED)


class BuyerViewSet(ViewSet):
    queryset = Buyer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BuyerSerializer

    def get_object(self, request, id):
        availability = self.queryset.filter(id=id)
        return availability


    # fetch userdetail
    @action(detail=False, methods=['GET'])
    def fetch_detail(self, request):
        user = request.user
        try:
            buyer = Buyer.objects.get(user=user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_403_FORBIDDEN)

        serialize = self.serializer_class(buyer)
        return Response(data=serialize.data, status=status.HTTP_200_OK)


    # update personal Info
    @action(detail=False, methods=['POST'])
    def update_pd(self, request):
        user = request.user
        try:
            buyer = Buyer.objects.get(user=user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        buyer.first_name = data.get('first_name','')
        buyer.last_name = data.get('last_name','')
        buyer.gender = data.get('gender',1)
        buyer.save()
        return Response(data={'detail':'updates'}, status=status.HTTP_202_ACCEPTED)

    # update email
    @action(detail=False, methods=['POST'])
    def update_email(self, request):
        user = request.user
        email = request.data.get('email', '')
        if email:
            user.email = email
            user.save()
            return Response(data={'detail':'updates'}, status=status.HTTP_202_ACCEPTED)
        return Response(data={'detail':'No Email'}, status=status.HTTP_204_NO_CONTENT)

    # update mobile
    @action(detail=False, methods=['POST'])
    def update_mobile(self, request):
        user = request.user
        data = request.data
        user.mobile = data.get('mobile','')
        try:
            user.save()
            return Response(data={'detail':'updates'}, status=status.HTTP_202_ACCEPTED)
        except  Exception as e:
            return Response(data={'error':e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BuyerAddressViewSet(ViewSet):
    queryset = UserAddress.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAddressSerializer

    def get_object(self, request, id):
        address = self.queryset.filter(id=id)
        return address

    # list address
    def list(self, request):
        addresses = self.queryset.filter(buyer__user=request.user)
        if addresses.exists():
            serialize = self.serializer_class(addresses, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail':"No Data"}, status=status.HTTP_204_NO_CONTENT)

    # Retreive aaddress
    def retrieve(self, request, pk=None):
        address = self.get_object(request, pk)
        if address.exists():
            serialized = self.serializer_class(address.last())
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Please Check uuid", status=status.HTTP_404_NOT_FOUND)


    # add address
    def create(self, request):
        user = request.user
        try:
            buyer = Buyer.objects.get(user=user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.get('address')
        try:
            pincode = Pincode.objects.get(pincode=data.get('pincode'))
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            data.update({'pincode':pincode})
            address = UserAddress.objects.create(**data)
            if address:
                buyer.addresses.add(address)
                buyer.save()
                return Response(data={"detail": "created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # update address
    def update(self, request, *args, **kwargs):
        data = request.data.get('address')
        instance = self.get_object(request, kwargs.get('pk', ''))
        if instance.exists():
            try:
                pincode = Pincode.objects.get(pincode=data.get('pincode'))
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            data.update({'pincode':pincode})
            data.update({'add_type': int(data.get('add_type', 1))})
            serializer = self.serializer_class(instance.first(), data=data)
            try:
                if serializer.is_valid(raise_exception=False):
                    serializer.update(instance.first(), serializer.validated_data)
                    return Response("Update Successfull", status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response("This Address is not yours", status=status.HTTP_404_NOT_FOUND)

    
    # delete address
    def destroy(self, request, *args, **kwargs):
        address = self.get_object(request, kwargs.get('pk', ''))
        if address.exists():
            address.delete()
            return Response("Delete Successfully", status=status.HTTP_204_NO_CONTENT)
        return Response("This address is not yours", status=status.HTTP_404_NOT_FOUND)


class PaymentOptionViewSet(ViewSet):
    queryset = Card.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CardSerializer

    def get_object(self, request, id):
        card = self.queryset.filter(id=id)
        return card

    # list card
    def list(self, request):
        cards = self.queryset.filter(buyer__user=request.user)
        if cards.exists():
            serialize = self.serializer_class(cards, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail':"No Data"}, status=status.HTTP_204_NO_CONTENT)

    # Retreive acard
    def retrieve(self, request, pk=None):
        card = self.get_object(request, pk)
        if card.exists():
            serialized = self.serializer_class(card, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Please Check uuid", status=status.HTTP_404_NOT_FOUND)


    # add card
    def create(self, request):

        user = request.user
        try:
            buyer = Buyer.objects.get(user=user)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.get('card')
        try:
            # data.update({'pincode':pincode})
            card = Card.objects.create(**data)
            if card:
                buyer.cards.add(card)
                buyer.save()
                return Response(data={"detail": "created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # update card
    def update(self, request, id):
        data = request.data
        instance = self.get_object(request, id)
        if instance.exists():
            serializer = self.serializer_class(instance.last(), data=data)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.update(instance, serializer.validated_data)
                    return Response("Update Successfull", status=status.HTTP_202_ACCEPTED)
            except Exception as e:
                return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
        return Response("This Card is not yours", status=status.HTTP_404_NOT_FOUND)

    
    # delete card
    def destroy(self, request, *args, **kwargs):
        card = self.get_object(request, kwargs.get('pk', ''))
        if card.exists():
            card.delete()
            return Response("Delete Successfully", status=status.HTTP_204_NO_CONTENT)
        return Response("This card is not yours", status=status.HTTP_404_NOT_FOUND)


class BuyerWishlistViewset(ViewSet):
    queryset = BuyerWishlist.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BuyerWishlistSerializer

    def get_object(self, request, id):
        availability = self.queryset.filter(id=id)
        return availability


    # wishlist 
    def list(self, request):
        user = request.user
        wishlists = self.queryset.filter(user=user)
        if wishlists.exists():
            serialize = self.serializer_class(wishlists.last())
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail':"No Data"}, status=status.HTTP_204_NO_CONTENT)


    # add into wishlist
    @action(detail=False, methods=['POST'])
    def add(self, request):
        user = request.user
        product = Product.objects.get(id = int(request.data.get('product_id')))
        user_wish = BuyerWishlist.objects.filter(user=user)
        if user_wish:
            wish = user_wish.last()
            is_exists = wish.products.filter(id=product.id)
            if is_exists.exists():
                return Response(data={'detail': 'Already in wishlist'}, status=status.HTTP_200_OK)
        else:
            wish = BuyerWishlist.objects.create(
                user=user
            )
        wish.products.add(product)
        wish.save()
        return Response(data={'detail': 'Added to wishlist.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def isYour(self, request, pk=None):
        wishlist = self.queryset.get(user=request.user)
        if wishlist:
            products = list(wishlist.products.values_list('id', flat=True))
            if int(pk) in products:
                return Response(data={'exist':True}, status=status.HTTP_200_OK)
            else:
                return Response(data={'exist':False}, status=status.HTTP_200_OK)
        return Response(data={'detail':"This wishlist is not yours"}, status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, *args, **kwargs):
        wishlist = self.queryset.get(user=request.user)
        if wishlist:
            p = Product.objects.get(id=kwargs.get('pk', ''))
            wishlist.products.remove(p)
            return Response(data={'details':"Delete Successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={'detail':"This wishlist is not yours"}, status=status.HTTP_404_NOT_FOUND)
