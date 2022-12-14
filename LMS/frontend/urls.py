
from django.urls import path
from . import views

app_name="chatapp_frontend"

urlpatterns = [
    path("", views.index, name = 'index'),
    path("<str:chatID>/", views.chat_room, name = 'chat_room'),
]