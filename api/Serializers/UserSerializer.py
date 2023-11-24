from rest_framework import serializers
from ..models import User, Address
from .AddressSerializer import AddressSerializer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','firstname', 'lastname', 'password', 'email', 'is_superuser', 'is_active', 'phone_code', 'phone', 'transaction_pin', 'address']

    address = AddressSerializer()
    phone_code = serializers.ChoiceField(choices=User.PHONE_CODES, initial='NG')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        validated_data['address'] = Address.objects.create(**address_data)
        user = User.objects.create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address

        if address_data:
            address.number = address_data.get('number', address.number)
            address.street = address_data.get('street', address.street)
            address.city = address_data.get('city', address.city)
            address.state = address_data.get('state', address.state)
            address.country = address_data.get('country', address.country)
            address.save()

        # Update fields of the Person
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email= validated_data.get('email', instance.email)
        instance.phone= validated_data.get('phone', instance.phone)
        instance.phone_code= validated_data.get('phone_code', instance.phone_code)
        # Update other fields as needed

        instance.save()
        return instance