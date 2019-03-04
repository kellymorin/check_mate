from django.urls import path

from . import views

app_name = "check_mate"

urlpatterns=[
    path("", views.index, name='index'),
    # ex. /login
    path("login", views.login_user, name="login"),
    # ex. /logout
    path("logout", views.user_logout, name="logout"),
    # ex. /register
    path("register", views.register, name="register"),
    # ex. /projects
    path("projects", views.projects, name="projects"),
    # ex. /projects/5
    path("projects/<int:project_id>", views.project_details, name="project_details"),
    # ex. /projects/add
    path("projects/add", views.project_add, name="project_add"),
    # ex. /projects/5/delete
    path("projects/<int:project_id>/delete", views.project_delete, name="project_delete"),
    # ex. /projects/5/edit
    path("projects/<int:project_id>/edit", views.project_edit, name="project_edit"),
    # ex. /ticket/add
    path("ticket/add", views.ticket_add, name="ticket_add")
]