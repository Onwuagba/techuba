from rest_framework import serializers
from ..models import User, Address
from .AddressSerializer import AddressSerializer

class UserSerializer(serializers.ModelSerializer):
    
    address = AddressSerializer()

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        address = validated_data.pop('address')
        validated_data['address'] = Address.objects.create(**address)
        user = User.objects.create(**validated_data)
        return user