from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..models import User
from ..serializers import UserSerializer
# Create your views here.

class EditUserInformation(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
