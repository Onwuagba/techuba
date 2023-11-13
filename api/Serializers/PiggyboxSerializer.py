from ..models import Piggybox
from rest_framework import serializers

class PiggyboxSerializer(serializers.ModelSerializer):

    interest =  serializers.ReadOnlyField()

    class Meta:
        model = Piggybox
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = instance.username.email
        return representation