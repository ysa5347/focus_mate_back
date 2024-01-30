from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from account.models import CustomUser, FollowUserStat
from group.models import groupSession, groupUserTable
from group.views import groupAPIView
from kafka import KafkaProducer

class matchSubmit(groupAPIView):

    def post(self, request):
        super().isUserInGroup(request, request.GET['pk'])
        group = super().get_group(request.GET['pk'])

        producer = KafkaProducer(
            acks=0
        )

class matchStatus(groupAPIView):
    
    def get(self, request):
        super().isUserInGroup(request, request.GET['pk'])
        group = super().get_group(request.GET['pk'])


