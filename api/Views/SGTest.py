from rest_framework import generics
from ..models import SavingsGroup
from ..serializers import SavingsGroupSerializer
import pdb

class SGTest(generics.ListAPIView):
    serializer_class = SavingsGroupSerializer
    queryset = SavingsGroup.objects.all().values()

