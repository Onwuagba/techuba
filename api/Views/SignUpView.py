from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..Serializers import UserSerializer 
from ..Models import User
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# @authentication_classes(['rest_framework.authentication.TokenAuthentication'])
