from rest_framework import serializers
from django.contrib.auth import get_user_model
from account.models import CustomUser, FollowUserStat

# 추후 위치정보도 넣어야함
class userMatchializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userID','college', 'major', 'semaster', 'profileImg']