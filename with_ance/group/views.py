from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from account.models import CustomUser, FollowUserStat
from .models import groupSession, groupUserTable
from .permissions import *
from .serializers import *

class groupAPIView(APIView):
    
    def get_group(self, pk):
        group = get_object_or_404(groupSession, pk=pk)
        return group

    def isUserInGroup(self, request, pk, **kwargs):
        group = self.get_group(pk)
        try:
            user = group.user.get(userID=request.user)
        except:
            raise exceptions.PermissionDenied("you are not the group member.")
        table = groupUserTable.objects.get(user=user, group=group)
        if not(kwargs.get("include") or table.acceptStat):
            raise exceptions.PermissionDenied("you are not the group member since you still not accepted invite.")

        

    def setUserPresent(self, group):
        pass

    def queryValidator(self, **kwargs):
        pass

class groupCreateViewAPI(groupAPIView):
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
            leader=reqUser,
            userCap=data["userCap"]
            )
        group.user.add(reqUser)
        table = groupUserTable.objects.get(user=reqUser, group=group)
        table.acceptStat = True
        table.save()
        
        return Response(serializer.data)

class groupListViewAPI(groupAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # query = super.queryValidator(request.GET)
        # groups = groupSession.objects.filter(pubStat=True, **query)
        groups = groupSession.objects.filter(pubStat=True)
        if not groups:
            raise exceptions.NotFound()
        serializer = groupListViewSerializer(groups, many=True)
        return Response(serializer.data)
    
class groupDetailViewAPI(groupAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        group = super(groupDetailViewAPI, self).get_group(pk)
        serializer = groupDetailViewSerializer(group)
        
        return Response(serializer.data)

    def patch(self, request, pk):
        super(groupDetailViewAPI, self).isUserInGroup(request, pk)
        group = super(groupDetailViewAPI, self).get_group(pk)
        serializer = groupDetailViewSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        super(groupDetailViewAPI, self).isUserInGroup(request, pk)
        group = super(groupDetailViewAPI, self).get_group(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class userReadyViewAPI(groupAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        pk = request.GET['pk']
        super(userReadyViewAPI, self).isUserInGroup(request, pk)

        group = super(userReadyViewAPI, self).get_group(pk)
        user = get_object_or_404(CustomUser, userID=request.user)
        toggle = request.GET.get('ready', True)

        table = group.userTable.get(user=user)
        table.userIsReady = toggle
        table.save()
        return Response(f"Successfully changed to ready={toggle}.", status=status.HTTP_200_OK)
        
class groupInviteViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        super(groupInviteViewAPI, self).isUserInGroup(request, request.GET['pk'])
        group = super(groupInviteViewAPI, self).get_group(request.GET['pk'])
        target = get_object_or_404(CustomUser, userID=request.GET['userID'])
        group.user.add(target)

        return Response("ok", status=status.HTTP_200_OK)

class groupInviteAcceptViewAPI(groupAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        pk = request.GET['pk']
        super(groupInviteAcceptViewAPI, self).isUserInGroup(request, pk, include=True)
        user, group = CustomUser.objects.get(userID=request.user), super(groupInviteAcceptViewAPI, self).get_group(pk)
        
        table = groupUserTable.objects.get(user=user, group=group)
        table.acceptStat = True
        table.save()
        return Response("ok", status=status.HTTP_200_OK)
        
class groupLeaveViewAPI(groupAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def delete(self, request):
        pk = request.GET['pk']
        super(groupLeaveViewAPI, self).isUserInGroup(request, pk, include=True)
        group = super(groupLeaveViewAPI, self).get_group(pk)
        target = get_object_or_404(CustomUser, userID=request.GET['userID'])

        group.user.remove(target)

        return Response("ok", status=status.HTTP_200_OK)


