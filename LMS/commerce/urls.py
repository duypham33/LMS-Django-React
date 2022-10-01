
from django.urls import path
from . import views

app_name="commerce"

urlpatterns = [
    path("", views.index, name='index'),
]