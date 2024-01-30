from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, FollowUserStat

User = get_user_model()

class userCreateSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            userID = validated_data['userID'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])

        user.save()
        return user
        
class userListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userID', 'college', 'major', 'semaster']

class userFollowViewSerializer(serializers.ModelSerializer):
    class Meta:
        models = FollowUserStat
        fields = '__all__'

# userID가 팔로우당한 사람
class userFollowersViewSerializer(serializers.ModelSerializer):
    class Meta:
        models = CustomUser
        fields = ['followee_user']

# userID가 팔로우하는 사람
class userFolloweesViewSerializer(serializers.ModelSerializer):
    class Meta:
        models = CustomUser
        fields = ['follower_user']

class userDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class userAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userID', 'email', 'college', 'major', 'semaster', 'comment']

class userLoginSerializer(serializers.Serializer):
    userID = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class userFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUserStat
        exclude = ['pk']