
from django.urls import path
from . import views

app_name="staff"

urlpatterns = [
    path("", views.home, name='staHome'),
    path("professors", views.view_professors, name='view_professors'),
    path("courses", views.view_courses, name='view_courses'),
    path("professor/<int:pk>/courses", views.view_teacherCourses, name='teacher_courses'),
]