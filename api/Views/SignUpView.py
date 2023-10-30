from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..Serializers import UserSerializer 
from ..Models import User
# Create your views here.

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer.UserSerializer
    queryset = User.User.objects.all()
