import random
import uuid
import datetime

from django.shortcuts import render
from django.core.mail import EmailMessage

from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

from api.models import User, Role, Subscriber, Contact, State, City, Pincode
from api.serializers import CitySerializer, StateSerializer, PincodeSerializer


# Call from OTP send on Buyer Registration and Login
class LoginOTPView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        email = request.data.get('email','')
        if email:
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                return Response(data={'detail': "Email is not registered"}, status=status.HTTP_403_FORBIDDEN)
            otp = random.randint(1000,9999)
            subject = "OTP To Register"
            body = "Hi,\n Here is your required otp: \n  {} \n\nThanks & Regards\n Army".format((otp))
            Email = EmailMessage(subject=subject, body=body, to=(email,))
            token, _ = Token.objects.get_or_create(user=user)
            try:
                Email.send()
                return Response(data={'detail':"OTP has been sent to email.Please check.", "OTP":otp, 'token': str(token.key)}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data={'detail':"Please check Email."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterOTPView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        data = request.data.get('registerData')
        email = data.get('email','')

        if email:
            otp = random.randint(1000,9999)
            subject = "OTP To Register"
            body = "Hi,\n Here is your required otp: \n  {} \n\nThanks & Regards\n Army".format((otp))
            Email = EmailMessage(subject=subject, body=body, to=(email,))
            try:
                Email.send()
                user = User.objects.create(
                    email=email,
                    role=Role.BUYER,
                    password=data.get('password'),
                    number=data.get('mobile')
                )
                # buyer = Buyer.objects.create(user=user)
                token, _ = Token.objects.get_or_create(user=user)
                # return Response(data={'token':str(token.key)}, status=status.HTTP_201_CREATED)
                return Response(data={'token':str(token.key), 'detail':"OTP has been sent to email.Please check.", "OTP":otp}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'detail':"Please check Email."}, status=status.HTTP_400_BAD_REQUEST)


# call after login otp
class Login(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        """
            Api for Sent Reset Password Link To User Email.
        """
        data = request.data.get('emailData')
        email = data.get('login_input','')
        password = data.get('password_input', '')
        if email and password:
            try:
                user = User.objects.get(email=email, password=password)
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    return Response(data={'token':str(token.key)}, status=status.HTTP_201_CREATED)
                else:
                    return Response(data={'detail':'Email or Password is not matched'}, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'detail':'Email or Password should not be blanked.'}, status=status.HTTP_400_BAD_REQUEST)


# Call from suscription button
class SubscribeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        email = request.data.get('email','')
        if email:
            subject = "Subscription Mail"
            body = "Hi,\n You are subscribed us \n  \nThanks & Regards\n Ecom"
            Email = EmailMessage(subject=subject, body=body, to=(email,))
            try:
                reponse = Email.send()
                customer = Subscriber.objects.create(email=email)
                return Response(data={'detail': 'Successfully Subscribed'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'detail':'Please Try again'}, status=status.HTTP_400_BAD_REQUEST)


# Call On Customer Query
class CustomerQueryView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
            Api for Sent Reset Password Link To User Email.
        """
        email = request.data.get('contactData').get('email','')
        if email:
            name = request.data.get('contactData').get('name','')
            subject = request.data.get('contactData').get('subject','')
            comment = request.data.get('contactData').get('comment','')


            body = "Hi,\n Our teM WILL contact you soon \n   \nThanks & Regards\n Ecom"

            Email = EmailMessage(subject=subject, body=body, to=(email,))
            try:
                reponse = Email.send()
                query = Contact.objects.create(email=email, name=name, subject=subject, comment=comment)
                return Response(data={'detail': 'Successfully Query Saved'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'detail':'Please Try again'}, status=status.HTTP_400_BAD_REQUEST)


class StateViewSet(ViewSet):
    queryset = State.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StateSerializer

    def get_object(self, request, id):
        state = State.objects.filter(id=id)
        return state

    # list of state
    def list(self, request):
        context = {
            "is_success": False,
            "states": None
        }
        if self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            context.update({
                "is_success": True,
                "states": serialize.data
            })

        return Response(context, status=status.HTTP_200_OK)

    # State with id
    def retrieve(self, request, pk=None):
        state = self.get_object(request, pk)
        if state.exists():
            serialized = self.serializer_class(state.last())
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(" No State", status=status.HTTP_404_NOT_FOUND)


class CityViewSet(ViewSet):
    queryset = City.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

    def get_object(self, request, id):
        city = City.objects.filter(id=id)
        return city

    # list of cities
    def list(self, request):
        context = {
            "is_success": False,
            "cities": None
        }
        if self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            context.update({
                "is_success": True,
                "cities": serialize.data
            })

        return Response(context, status=status.HTTP_200_OK)

    # City with id
    def retrieve(self, request, pk=None):
        city = self.get_object(request, pk)
        if city.exists():
            serialized = self.serializer_class(city.last())
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(" No city", status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['GET'])
    def get_cities_by_state(self, request, pk=None):
        cities = self.queryset.filter(state_id=pk)
        if cities.exists():
            serialized = PincodeSerializer(cities, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("State Has No City.", status=status.HTTP_404_NOT_FOUND)


class PincodeViewSet(ViewSet):
    queryset = Pincode.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PincodeSerializer

    def get_object(self, request, id):
        pincode = Pincode.objects.filter(id=id)
        return pincode

    # list of cities
    def list(self, request):
        context = {
            "is_success": False,
            "pincodes": None
        }
        if self.queryset.exists():
            serialize = self.serializer_class(self.queryset, many=True)
            context.update({
                "is_success": serialize.data,
                "pincodes": True
            })

        return Response(context, status=status.HTTP_200_OK)

    # Pincode with id
    def retrieve(self, request, pk=None):
        pincode = self.get_object(request, pk)
        if pincode.exists():
            serialized = self.serializer_class(pincode.last())
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(" No pincode", status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['POST'])
    def get_location_by_pincode(self, request):
        pincodes = self.queryset.filter(pincode=request.data.get('pincode'))
        if pincodes.exists():
            serialized = PincodeSerializer(pincodes, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("City Has No Pincode.", status=status.HTTP_404_NOT_FOUND)

