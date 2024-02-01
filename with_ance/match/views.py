from kafka import KafkaProducer
from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from datetime import datetime

from account.models import CustomUser, FollowUserStat
from group.models import groupSession, groupUserTable
from group.views import groupAPIView

from .serializers import *

class matchSubmit(groupAPIView):

    def post(self, request):
        super().isUserInGroup(request, request.GET['pk'])
        group = super().get_group(request.GET['pk'])
        users = CustomUser.objects.filter(group=group)
        serializer = userMatchializer(users)

        producer = KafkaProducer(
            acks=0
        )

class matchStatus(groupAPIView):
    
    def get(self, request):
        super().isUserInGroup(request, request.GET['pk'])
        group = super().get_group(request.GET['pk'])

# match가 성사되면, n개의 group를 1개의 group으로 묶어서 새로 생성.
def matchSuccess(userCap, *groups):
    """
    groups는 [pk]로 구성.
    다음엔 유사도, 매칭 적합률 등 여러 지표를 parameter로 받는 것도 고려해보도록.
    """

    newGroup = groupSession.objects.create(
        userCap=userCap,
        gender=None,
        userPresent=userCap,
        matchStat=True,
        matchTime=datetime.now()
    )

    for group in groups:
        group = groupSession.objects.get(pk=group)
        table = groupUserTable.objects.filter(group=group)
        for user in table:
            user = user.user
            groupUserTable.objects.create(user=user, group=newGroup, lastGroup=group)
    
