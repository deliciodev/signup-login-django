from rest_framework import serializers
from .models import Customer

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'name']
        ref_name = "CustomerRegistration"

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return Customer.objects.create_user(**validated_data)
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'created_at', 'updated_at', 'username']
        ref_name = "Customer"
class CustomerLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Email or Username")
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        ref_name = "CustomerLogin"