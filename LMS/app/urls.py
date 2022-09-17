
from django.urls import path
from . import views, auth_views

app_name="app"

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", auth_views.login_user, name='login'),
    path("logout/", auth_views.logout_user, name='logout'),

    path("profile/", views.profile, name='profile'),
    path("courses/notification/", views.select_course_send_notice, name='select_course_send_notice'),
    path("course/<int:pk>/send_notice/", views.send_notice, name='send_notice'),
    path("inbox/", views.view_inbox, name='view_inbox'),
    path("inbox/<int:pk>/", views.inbox, name='inbox'),
]