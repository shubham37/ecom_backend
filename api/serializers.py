from rest_framework import  serializers
from api.models import State, City, Pincode, User


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields ='__all__'
        depth = 1


class PincodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pincode
        fields ='__all__'
        depth = 2
