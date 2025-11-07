from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate, get_user_model

from .serializers import CustomerRegistrationSerializer, CustomerSerializer, CustomerLoginSerializer

Customer = get_user_model()

class CustomerSignupView(generics.CreateAPIView):
    serializer_class = CustomerRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": CustomerSerializer(user).data,
            "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)},
            "message": "Customer registered successfully."
        }, status=status.HTTP_201_CREATED)
    
class CustomerLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomerLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data['identifier']
        password = serializer.validated_data['password']

        user = authenticate(request, username=identifier, password=password)
        if user is not None or not user.is_active:
            return Response({"error": "Invalid credentials or inactive account."}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": CustomerSerializer(user).data,
            "tokens": {"refresh": str(refresh), "access": str(refresh.access_token)},
            "message": "Customer logged in successfully."
        }, status=status.HTTP_200_OK)
    
class CustomerLogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        
class CustomerProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
    
class JWTTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

    