from rest_framework import serializers
from ..models import User, Address
from .AddressSerializer import AddressSerializer

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','firstname', 'lastname', 'password', 'email', 'is_superuser', 'is_active', 'phone_code', 'phone', 'address']

    address = AddressSerializer()
    phone_code = serializers.ChoiceField(choices=User.PHONE_CODES, initial='NG')
    
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)

        user = User(
            email=validated_data.get('email'),
            firstname=validated_data.get('firstname'),
            lastname=validated_data.get('lastname'),
            phone_code=validated_data.get('phone_code'),
            phone=validated_data.get('phone'),
        )

        password = validated_data.get('password')
        user.set_password(password)

        user.address = address
        user.save()

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

        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.email= validated_data.get('email', instance.email)
        instance.phone= validated_data.get('phone', instance.phone)
        instance.phone_code= validated_data.get('phone_code', instance.phone_code)

        instance.save()
        return instance