
from rest_framework import serializers

from .models import CustomUser

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
