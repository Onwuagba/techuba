from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from ..Serializers import UserSerializer 
from ..Models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.

class ViewAllUsers(generics.ListAPIView):
    permission_classes =  [IsAdminUser]

    queryset = User.User.objects.all()
    serializer_class = UserSerializer.UserSerializer

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@login_required
def my_view(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        return HttpResponse(f"You are logged in {request.user}.")
    else:
        # Redirect to the login page if not logged in
        return redirect('api-auth/login/') 


