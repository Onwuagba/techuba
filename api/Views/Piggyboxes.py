from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..models import Piggybox, SavingsGroup
from ..serializers import PiggyboxSerializer, SavingsGroupSerializer
from rest_framework.permissions import IsAdminUser

class ViewPiggyboxes(generics.ListAPIView):
    queryset = Piggybox.objects.all()
    serializer_class = PiggyboxSerializer


class ViewSavingsGroups(generics.ListAPIView):
    permission_classes = [IsAdminUser]

    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer