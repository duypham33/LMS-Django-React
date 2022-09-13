
from django.urls import path
from . import views, auth_views

app_name="app"

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", auth_views.login_user, name='login'),
    path("logout/", auth_views.logout_user, name='logout'),

    path("profile/", views.profile, name='profile'),
]