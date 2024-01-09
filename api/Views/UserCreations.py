from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse        
from ..serializers import SavingsGroupSerializer, UserSerializer, PiggyboxSerializer, AccountSerializer
from ..Models.SavingsGroup import SavingsGroup
from rest_framework import status, permissions
from rest_framework import generics
from ..Models.User import User
from ..Models.Piggybox import Piggybox
from ..Models.Account import Account
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            refresh_token = request.data.get('refresh_token')

            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                    return Response({'detail': 'Logout successful.'}, status=200)
                except Exception as e:
                    return Response({'detail': 'Invalid token or token has already been used.'}, status=400)

            return Response({'detail': 'No refresh token provided.'}, status=400)
        return Response('Log in before you log out')

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Customize the success and failure responses
        success_response = Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        failure_response = Response({"message": "Failed to create user"}, status=status.HTTP_400_BAD_REQUEST)

        # Return the appropriate response based on the success of user creation
        return success_response if serializer.data.get('email') else failure_response
    

class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=200)
        else:
            return Response(serializer.errors, status=400)
        

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.get(user=request.user).delete()
        return Response({"detail": "logged out."}, status=status.HTTP_200_OK)
    

class PiggyboxCreation(generics.CreateAPIView):
    queryset = Piggybox.objects.all()
    serializer_class = PiggyboxSerializer
    permission_classes = [permissions.IsAuthenticated]  # Use IsAuthenticated permission

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)
        return Response('Piggybox created successfully')

class AccountCreation(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(username=self.request.user, pin=self.request.data.get('pin'))
        elif self.request.user.is_anonymous:
            return Response("Please log in to continue")

    def create(self, request, *args, **kwargs):
        # Call the super create method to perform the creation
        response = super().create(request, *args, **kwargs)
        return Response(f"Account created successfully: {response.data['account_number']}")


class SavingsGroupCreation(generics.CreateAPIView):
    queryset = SavingsGroup.objects.all()
    serializer_class = SavingsGroupSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(creator = self.request.user)
            return Response("Savings group created successfully")
        elif self.request.user.is_anonymous:
            return Response("Please log in to continue")
        else:
            return Response("Authentication required")