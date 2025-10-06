from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        # Updated to match Flutter expectations - only username and email

class UserProfileUpdateRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    bio = serializers.CharField(max_length=500, required=False, allow_blank=True)
    display_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    location = serializers.CharField(max_length=100, required=False, allow_blank=True)
