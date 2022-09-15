
from django.urls import path
from . import views

app_name="teacher"

urlpatterns = [
    path("", views.home, name='teaHome'),
    path("session/new/", views.add_session, name='add_session'),
    path("session/view/", views.view_sessions, name='view_sessions'),
    path("session/edit/<int:pk>", views.update_session, name='update_session'),


    path("subject/new/", views.add_subject, name='add_subject'),
    path("subject/view/", views.view_subjects, name='view_subjects'),
    path("subject/edit/<int:pk>", views.update_subject, name='update_subject'),

    path("course/new/", views.add_course, name='add_course'),
    path("course/view/", views.view_courses, name='view_courses'),
    path("course/edit/", views.edit_course, name='edit_course'),
    path("course/edit/<int:pk>", views.update_course, name='update_course'),
    path("course/delete/<int:pk>", views.delete_course, name='delete_course'),
    path("course/<int:pk>/roster", views.view_roster, name='view_roster'),
    path("course/<int:pk>/staffs", views.view_staffOf_course, name='view_staffOf_course'),

    path("student/new/", views.add_student, name='add_student'),
    path("student/view/", views.view_students, name='view_students'),
    path("student/edit/", views.edit_student, name='edit_student'),
    path("student/edit/<int:pk>", views.edit_a_student, name='update_student'),
    path("student/delete/<int:pk>", views.delete_student, name='delete_student'),
    path("student/<int:pk>/courses", views.view_coursesOf_student, name='coursesOfStud'),

    path('staff/new/', views.add_staff, name='add_staff'),
    path("staff/view/", views.view_staffs, name='view_staffs'),
    path("staff/edit/", views.edit_staff, name='edit_staff'),
    path("staff/edit/<int:pk>", views.edit_a_staff, name='update_staff'),
    path("staff/delete/<int:pk>", views.delete_staff, name='delete_staff'),
    path("staff/<int:pk>/courses", views.view_coursesOf_staff, name='coursesOfStaff'),
]