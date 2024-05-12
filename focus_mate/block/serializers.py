from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import CustomUser
from .models import timeBlock

class blockSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
    category = serializers.CharField(required=True)
    date = serializers.DateField()

    def create(self, validated_data):
        block = timeBlock.objects.create(
            userID = validated_data['userID'],
            start = validated_data['start'],
            end = validated_data['end'],
            category = validated_data['category'],
            date = validated_data['date']
        )
        block.save()
        return block
