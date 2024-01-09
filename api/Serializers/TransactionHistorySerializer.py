from rest_framework import serializers
from ..Models.Transaction import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = '__all__'


