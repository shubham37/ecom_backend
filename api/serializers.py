from rest_framework import  serializers
from api.models import State, City, Pincode        


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
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
