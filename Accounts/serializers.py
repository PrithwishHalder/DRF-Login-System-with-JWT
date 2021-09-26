from rest_framework import serializers
from django.contrib.auth import get_user_model
from Accounts.models import OTP

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'password', 'email']


class ResetSerializer(serializers.Serializer):

  model = User

  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)


class OTPSerializer(serializers.ModelSerializer):
  class Meta:
    model = OTP
    fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email']
