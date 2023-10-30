from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..Serializers import UserSerializer 
from ..Models import User
# Create your views here.

class ViewAllUsers(generics.ListAPIView):
    queryset = User.User.objects.all()
    serializer_class = UserSerializer.UserSerializer

