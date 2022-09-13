
from django.urls import path
from . import views

app_name="teacher"

urlpatterns = [
    path("", views.home, name='teaHome'),
    path("session/new/", views.add_session, name='add_session'),
    path("subject/new/", views.add_subject, name='add_subject'),
    path("course/new/", views.add_course, name='add_course'),
    path("course/view/", views.view_courses, name='view_courses'),
    path("course/edit/", views.edit_course, name='edit_course'),
    path("course/edit/<int:pk>", views.update_course, name='update_course'),
    path("course/delete/<int:pk>", views.delete_course, name='delete_course'),

    path("student/new/", views.add_student, name='add_student'),
    path("student/view/", views.view_students, name='view_students'),
    path("student/edit/", views.edit_student, name='edit_student'),
    path("student/edit/<int:pk>", views.edit_a_student, name='update_student'),
    path("student/delete/<int:pk>", views.delete_student, name='delete_student'),
]