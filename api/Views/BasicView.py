from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
# Create your views here.

class BasicView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Hello World'})

