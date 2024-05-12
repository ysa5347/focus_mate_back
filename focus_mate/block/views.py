from rest_framework import status
from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from account.permissions import OwnerOnly
from .serializers import blockSerializer
from account.models import CustomUser
from datetime import date

class blockCreateViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOnly]

    def post(self, request):
        serializer = blockSerializer(data=request.data)
        serializer.data['userID'] = request.user
        serializer.data['start'] = date.today().strftime()
 
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
    
class userTotalBlockViewAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOnly]

    def get(self, request):
        user = request.user
        blocks = user.timeBlocks.all().filter()
        serializer = blockSerializer(blocks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    