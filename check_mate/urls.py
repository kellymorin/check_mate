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
    # ex. /ticket/1
    path("ticket/<int:ticket_id>", views.ticket_detail, name="ticket_details"),
    # ex. /ticket/add
    # ex. /ticket/1/delete
    path("ticket/<int:ticket_id>/delete", views.ticket_delete, name="ticket_delete"),
    # ex. /ticket/1/edit
    path("ticket/<int:ticket_id>/edit", views.ticket_edit, name="ticket_edit"),
]