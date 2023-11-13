from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..models import Piggybox
from ..serializers import PiggyboxSerializer

class ViewPiggyboxes(generics.ListAPIView):
    queryset = Piggybox.objects.all()
    serializer_class = PiggyboxSerializer