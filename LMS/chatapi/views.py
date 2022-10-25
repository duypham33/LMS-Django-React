
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import ChatSerializer
from .models import Chat
from app.models import User
# Create your views here.

def get_current_user(request):
    user = request.user
    data = {
        "id": user.pk,
        "name": user.get_name(),
        "avatar": '../' + user.avatar.name
    }

    return JsonResponse(data = data, status = status.HTTP_200_OK)


class GetChats(APIView):
    serializer_class = ChatSerializer
    
    def get(self, request):
        user = request.user
        userid = user.pk
        user_info = {
                    "name": user.get_name(),
                    "avatar": user.avatar.name
                }
        
        chats = ChatSerializer(user.chats.all(), many = True, context = {'userid': userid}).data
        return Response({'user_info': user_info, 'chats': chats}, status=status.HTTP_200_OK)
        
