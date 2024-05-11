from django.shortcuts import redirect, render
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly, OwnerOnly
from .serializers import *
from .models import CustomUser

# class userListViewAPI:

# class userDetailViewAPI(APIView):       #permition 필요
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def get_object(self, userID):
#         user = get_object_or_404(CustomUser, userID=userID)
#         return user
    
#     def get(self, request, userID):
#         user = self.get_object(userID)
#         if request.user == user:
#             serializer = userDetailSerializer(user)
#         else:
#             serializer = userAbstractSerializer(user)
#         return Response(serializer.data)
    
#     def patch(self, request, userID):
#         user = self.get_object(userID)
#         serializer = userDetailSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# #     def delete(self, request, userID):
#         user = self.get_object(userID)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class userCreateViewAPI(APIView):

    def post(self, request):
        serializer = userCreateSerializer(data=request.data)
 
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if CustomUser.objects.filter(userID=serializer.validated_data['userID']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate user"}, status=status.HTTP_409_CONFLICT)

class loginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        userID = request.data.get('userID')
        password = request.data.get('password')

        if userID is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = auth.authenticate(userID=userID, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        auth.login(request, user)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

class logoutAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        auth.logout(request)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

class userConfigViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOnly]

    def get(self, request):
        user = CustomUser.objects.get(userID=request.user)
        serializer = userConfigSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = CustomUser.objects.get(userID=request.user)
        serializer = userConfigSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class userCategoryViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOnly]

    def get(self, request):
        user = CustomUser.objects.get(userID=request.user)
        serializer = userCategorySerializer(user)
        return Response(serializer.data)

    def post(self, request):
        user = CustomUser.objects.get(userID=request.user)
        serializer = userCategorySerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class userSearchViewAPI(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
    
#     def get(self, request):
#         serializer = userListSerializer(CustomUser.objects.all(), many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         filter = request.POST.items()
#         for key, value in filter:
#             key = key + "__contains"

#         Users = CustomUser.objects.all()
#         if filter is not None:
#             Users = Users.filter(**filter)
#         serializer = userListSerializer(Users, many=True)
#         return Response(serializer.data)

# userID를 팔로우하고 있는 사람
# class userFollowersViewAPI(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, userID):
#         user = CustomUser.objects.get(userID=userID)
#         serializer = userFollowersViewSerializer(user)
#         return Response(serializer.data)     


# # userID가 팔로우하고 있는 사람
# class userFolloweesViewAPI(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, userID):
#         user = CustomUser.objects.get(userID=userID)
#         serializer = userFolloweesViewSerializer(user)
#         return Response(serializer.data)

# class userFollowAPI(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly, OwnerOnly]

#     # userID는 팔로우 당하는 사람임.
#     def get(self, request, userID):
#         follower = get_object_or_404(CustomUser, userID=request.user)
#         followee = get_object_or_404(CustomUser, userId=userID)
#         stat = FollowUserStat.objects.create(follower = follower, followee = followee)
        
#         serializer = userFollowViewSerializer(stat)
#         return Response(serializer.data)

# class userInviteStatViewAPI(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         # groups = groupUserTable.objects.filter(user=user, acceptStat=0, acceptType=0)
#         print(request.user)
#         user = CustomUser.objects.get(userID=request.user)
#         print(user)
#         groups = groupSession.objects.filter(groupUserTable__user=request.user, groupUserTable__acceptStat=0, groupUserTable__acceptType=0)

#         serializer = groupListViewSerializer(groups)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        



    




        
        