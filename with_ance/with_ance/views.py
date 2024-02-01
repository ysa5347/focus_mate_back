from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class helloView(APIView):
    def get(self):
        return Response("hello World!", status=status.HTTP_200_OK)