from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=500)
    new_password = serializers.CharField(max_length=500)
    re_password = serializers.CharField(max_length=500)

    def validate_new_password(self, value):
        if value != self.initial_data['re_password']:
            raise serializers.ValidationError("Please enter matching passwords")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=500)
    password = serializers.CharField(max_length=500)