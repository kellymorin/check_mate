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
    # ex. /projects/filter
    path("projects/filter", views.projects_filter, name="projects_filter"),
    # ex. /projects/5
    path("projects/<int:project_id>", views.project_details, name="project_details"),
    # ex. /projects/5/filter
    path("projects/<int:project_id>/filter", views.project_filter_tags, name="project_filter_tags"),
    # ex. /projects/add
    path("projects/add", views.project_add, name="project_add"),
    # ex. /projects/5/delete
    path("projects/<int:project_id>/delete", views.project_delete, name="project_delete"),
    # ex. /projects/5/edit
    path("projects/<int:project_id>/edit", views.project_edit, name="project_edit"),
    # ex. /ticket/1
    path("ticket/<int:ticket_id>", views.ticket_detail, name="ticket_details"),
    # ex. /ticket/1/filter
    # path("ticket/<int:ticket_id>/filter", views.ticket_filter_tags, name="ticket_filter_tags"),
    # ex. /ticket/1/history
    path("ticket/<int:ticket_id>/history", views.ticket_detail, name="ticket_history"),
    # ex. /ticket/add
    path("ticket/add", views.ticket_add, name="ticket_add"),
    # ex. /ticket/1/delete
    path("ticket/<int:ticket_id>/delete", views.ticket_delete, name="ticket_delete"),
    # ex. /ticket/1/edit
    path("ticket/<int:ticket_id>/edit", views.ticket_edit, name="ticket_edit"),
    # ex. /task/add
    path("task/add", views.task_add, name="task_add"),
    # ex. /task/1/edit
    path("task/<int:task_id>/edit", views.task_edit, name="task_edit"),
    # ex. /task/1/delete
    path("task/<int:task_id>/delete", views.task_delete, name="task_delete"),
    # ex. /stand-up
    path("stand-up", views.stand_up_view, name="stand-up"),
    # ex /stand-up/claim
    path("stand-up/claim", views.claim_tickets_tasks, name="claim"),
    # ex /stand-up/claim/edit
    path("claim/edit", views.remove_claim, name="remove-claim"),
    # ex /stand-up/claim/view-all
    path("stand-up/claim/view-all", views.claim_tickets_tasks, name="claim-all"),
]