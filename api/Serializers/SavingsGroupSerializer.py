from rest_framework import serializers
from ..models import SavingsGroup

class SavingsGroupSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator_id')

    class Meta:
        model = SavingsGroup
        fields = '__all__'
        # depth = 1

    