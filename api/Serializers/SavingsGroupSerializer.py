from rest_framework import serializers
from ..models import SavingsGroup
from ..models import User
class SavingsGroupSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.email')
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta:
        model = SavingsGroup
        fields = ['creator', 'group_name', 'date_created', 'date_fulfilled', 'target_amount', 'current_amount', 'interest', 'is_private', 'group_members']

    

from rest_framework import serializers
from ..Models.SavingsGroup import SGDeposit

class SGDepositSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(source='user.email', read_only=True)
    sg = serializers.PrimaryKeyRelatedField(source='sg.group_name', queryset=SavingsGroup.objects.all(), required=False)


    class Meta:
        model = SGDeposit
        fields = ['id', 'user', 'amount', 'sg']

    