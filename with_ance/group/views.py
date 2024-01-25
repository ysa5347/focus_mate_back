from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from account.models import CustomUser, FollowUserStat
from .permissions import *
from .serializers import *
from .models import groupSession

class groupCreateViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request):
        data = request.data
        reqUser = CustomUser.objects.get(userID=request.user)
        serializer = groupCreateViewSerializer(data=data)

        print(f"groupCreateViewAPI; reqUser: {request.user}")

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        
        group = groupSession.objects.create(
            name=data["name"],
            gender=reqUser.gender,
            leader=reqUser,
            userCap=data["userCap"]
            )
        group.users.add(reqUser)
        
        return Response(serializer.data)

class groupListViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        groups = groupSession.objects.all()# filter(pubStat=True)
        if not groups:
            raise exceptions.NotFound()
        print(groups[0].name)
        serializer = groupListViewSerializer(groups, many=True)
        return Response(serializer.data)
    

class groupDetailViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        group = get_object_or_404(groupSession, pk=pk)
        return group

    def insafe_methods_secure(self, request, pk):
        group = self.get_object(pk)

        for user in group.users:
            if request.user == user.userID:
                return
        raise exceptions.PermissionDenied()

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = groupDetailViewSerializer(group)
        
        return Response(serializer.data)

    def patch(self, request, pk):
        self.insafe_methods_secure(request, pk)
        group = self.get_object(pk)
        serializer = groupDetailViewSerializer(data=request.dat, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.insafe_methods_secure(request, pk)
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
