
from django.urls import path
from . import views

app_name="course"

urlpatterns = [
    path("<int:pk>", views.home, name="home"),
    path("<int:pk>/syllabus/edit", views.edit_syllabus, name="edit_syllabus"),
    path("<int:pk>/people", views.people, name="people"),

    path("<int:pk>/modules", views.module, name="module"),
    path("<int:pk>/module/new", views.add_module, name="add_module"),
    path("module/<int:pk>/edit", views.edit_module, name="edit_module"),
    path("module/<int:pk>/delete", views.delete_module, name="delete_module"),

    path("module/<int:pk>/page/new", views.add_page, name="add_page"),
    path("page/<int:pk>/", views.page, name="page"),
    path("page/<int:pk>/edit", views.edit_page, name="edit_page"),
    path("page/<int:pk>/delete", views.delete_page, name="delete_page"),
]
