from rest_framework import generics
from ..models import SavingsGroup, User
from ..serializers import SavingsGroupSerializer
import pdb
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated  # <-- Here


class Landing(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.firstname and user.lastname:
                return Response(f"Welcome {user.firstname}{user.lastname}")
            return Response(f"Welcome {user.email}!")
        else:
            return Response(f"Welcome, register and create an account today!")
