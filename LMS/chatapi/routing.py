
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chatID>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/notice/(?P<userID>\w+)/$", consumers.NoticeConsumer.as_asgi()),
]