from ..models import Piggybox
from rest_framework import serializers
from ..models import User

class PiggyboxSerializer(serializers.ModelSerializer):

    interest =  serializers.ReadOnlyField()

    username = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Piggybox
        fields = ['id', 'username', 'name_of_box', 'date_created', 'date_break', 'date_fulfilled', 'target_amount', 'current_amount', 'interest']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.username.email
        return representation