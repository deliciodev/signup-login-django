from rest_framework import status, generics, permissions, serializers
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
        identifier = serializer.validated_data["identifier"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=identifier, password=password)
        if user is None or not user.is_active:
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
            return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
    
class CustomerProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user
    
class JWTTokenRefreshView(TokenRefreshView):
    permission_classes = (permissions.AllowAny,)

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.pk == request.user.pk
    
class CustomerCreateListView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Customer.objects.all().order_by('created_at')

    def get_permissions(self):
        if self.request.method  in ("GET", "POST"):
            return [permissions.IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        reg = CustomerRegistrationSerializer(data=request.data)
        reg.is_valid(raise_exception=True)
        user = reg.save()
        return Response(CustomerSerializer(user).data, status=status.HTTP_201_CREATED)
    

class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticated, IsSelfOrAdmin)
    queryset = Customer.objects.all()