from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import Account
import pdb
from ..Serializers.TransactionSerializer import TransactionSerializer
from ..Models.Transaction import Transaction

class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()