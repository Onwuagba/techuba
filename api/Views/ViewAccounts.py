from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..Serializers.AccountSerializer import  AccountSerializer
from ..models import Account
# Create your views here.

class ViewAccounts(generics.ListAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()