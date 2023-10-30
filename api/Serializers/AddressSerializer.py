from rest_framework import serializers
from ..Models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address.Address
        fields = '__all__'


