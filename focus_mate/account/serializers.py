from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class userCreateSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            userID = validated_data['userID'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user

class userLoginSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class userConfigSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    outScreen = serializers.IntegerField(required=True)
    