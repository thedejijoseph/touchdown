
from rest_framework import serializers

from .models import CustomUser

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()

class AuthenticateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    auth_code = serializers.CharField()
