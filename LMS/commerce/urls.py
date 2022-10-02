
from django.urls import path
from . import views

app_name="commerce"

urlpatterns = [
    path("", views.index, name='index'),
    path("course/list", views.course_list, name='course_list'),
    path("course/<int:pk>", views.course_detail, name='course_detail'),
]