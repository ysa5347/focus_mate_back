from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import groupSession
from account.models import CustomUser, FollowUserStat
from account.serializers import userAbstractSerializer


class groupCreateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = groupSession
        fields = ['user', 'userCap']

class groupDetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = groupSession
        fields = '__all__'

class groupListViewSerializer(serializers.ModelSerializer):
    users = serializers.StringRelatedField(many=True)
    class Meta:
        model = groupSession
        fields = ['pk', 'name', 'gender', 'userCap', 'pubTime', 'users']