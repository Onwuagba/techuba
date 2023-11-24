from rest_framework import serializers
from ..models import Account

class AccountSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(source= 'username.email', read_only=True)

    class Meta:
        model= Account 
        fields = ['username', 'account_number', 'account_balance', 'pin']