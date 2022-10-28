
from django.urls import path
from . import views

app_name="chatapp_api"

urlpatterns = [
    path("chats/", views.GetChats.as_view(), name='current_user'),
    path("friends_search/", views.FriendSearch.as_view()),
    path("send_first_time/", views.FirstSend.as_view()),
]