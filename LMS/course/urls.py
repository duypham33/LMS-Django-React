
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

    path("module/<int:pk>/quiz/new", views.create_quiz, name="create_quiz"),
    path("quiz/<int:pk>/question/new", views.init_question, name="init_question"),
    path("question/<int:pk>/new", views.create_answer, name="create_answer"),
    path("question/<int:pk>/new_version", views.diff_ver_question, name="new_ver"),
    path('quiz/<int:pk>/created/', views.finish_quiz, name='finish_quiz'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/edit', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:pk>/view', views.view_quiz_content, name='view_quiz_content'),
    path('question/<int:pk>/view', views.question_view, name='question_view'),
    path('question/<int:pk>/edit', views.edit_question, name='edit_question'),

    path('answer/<int:pk>/edit', views.edit_answer, name='edit_answer'),
    path('answer/<int:pk>/add', views.edit_addanswer, name='edit_addanswer'),
    path('answer/<int:pk>/delete', views.delete_answer, name='delete_answer'),
    path('question/<int:pk>/local/delete', views.delete_qux_local, name='delete_qux_local'),
    path('question/<int:pk>/global/delete', views.delete_qux_global, name='delete_qux_global'),

    path('quiz/<int:pk>/delete', views.delete_quiz, name='delete_quiz'),
    path('quiz/<int:pk>/take', views.take_quiz, name='take_quiz'),

    path('attempt/<int:pk>/attempt/<int:num>', views.view_attempt, name='view_attempt'),

    path('module/<int:pk>/assignment/new', views.create_assignment, name='create_assignment'),
    path('assignment/<int:pk>', views.assignment, name='assignment'),
    path('assignment/<int:pk>/edit', views.edit_assignment, name='edit_assignment'),
    path('assignment/<int:pk>/submit', views.submit_assignment, name='submit_assignment'),

    path('submission/<int:pk>/<int:num>', views.submission_detail, name='submission_detail'),

    path('<int:pk>/view_assignments', views.view_assignments, name='view_assignments'),
    path('assignment/<int:pk>/submissions', views.view_submissions, name='view_submissions'),

    path('<int:pk>/view_quizzes', views.view_quizzes, name='view_quizzes'),
    path('quiz/<int:pk>/submissions', views.quiz_submissions, name='quiz_submissions'),

    path('quiz/<int:quiz_pk>/attempter/<int:pk>', views.grader_view_attempts, name='grader_view_attempts'),
    path('attempt/<int:pk>/grade', views.grade_quiz_attempt, name='grade_quiz_attempt'),

    path('<int:pk>/grade', views.view_grades, name='view_grades'),

    
]

