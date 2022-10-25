
from django.urls import path
from . import views

app_name="chatapp_api"

urlpatterns = [
    path("currentuser/", views.get_current_user, name='current_user'),
    path("chats/", views.GetChats.as_view(), name='current_user'),
]