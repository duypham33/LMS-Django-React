from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
from .serializers import ChatSerializer
from rest_framework.generics import (
    ListAPIView
)
# Create your views here.

# @login_required
# def index(request):
#     return render(request, 'chatapp/index.html')

# @login_required
# def room(request, room_name):
#     return render(request, "chatapp/room.html", {"room_name": room_name})


class ChatListView(ListAPIView):
    serializer_class = ChatSerializer
    