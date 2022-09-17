
from django.urls import path
from . import views

app_name="student"

urlpatterns = [
    path("", views.home, name="stuHome"),
    path("courses/", views.view_courses, name="view_courses"),
]