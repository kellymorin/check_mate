import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from check_mate.models import *
from check_mate.forms import ProjectForm

# Non-MVP Notes--------------------------------------------
# V2: Make sure every project has a status in fixtures
# ----------------------------------------------------------



@login_required
def projects(request):
    """This view collects all projects and renders them using the projects.html template

    Returns:
        [render] -- returns the projects.html template with all projects passed in
    """

    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, 'projects.html', context)

@login_required
def projects_filter(request):

    if request.method == "POST":
        status = []

        for item in request.POST:
            if "status" in item:
                if "_" in item.split("-")[1]:
                    new_item = item.split("-")[1]
                    status.append(" ".join(new_item.split("_")))
                else:
                    status.append(item.split("-")[1])

        projects = Project.objects.filter(project_status__in=status)

        context = {
            "projects": projects,
            "selected_status": status
        }

    return render(request, 'projects.html', context)

@login_required
def project_details(request, project_id):
    """This function loads a specific project's detail page

    Arguments:
        project_id {int} -- the id of the specific project details being requested

    Returns:
        [render] -- returns the project_details.html template with specific project details and all associated tickets passed in
    """
    user_list = []

    project_detail = Project.objects.get(pk=project_id)
    tickets = Ticket.objects.filter(project=project_id)
    ticket_tags = Ticket.objects.filter(project=project_id)
    tasks = Task.objects.filter(ticket__in=tickets)

    for ticket in tickets:
        if ticket.ticket_assigned_user is not None:
            if ticket.ticket_assigned_user not in user_list:
                user_list.append(ticket.ticket_assigned_user)

    for task in tasks:
        if task.task_assigned_user is not None:
            if task.task_assigned_user not in user_list:
                user_list.append(task.task_assigned_user)

    context = {
        "project_detail": project_detail,
        "tickets": tickets,
        "ticket_tags": ticket_tags,
        "user_list": user_list
    }
    return render(request, "project_details.html", context)

@login_required
def project_detail_filter(request, project_id):

    if request.method == "POST":
        project_detail = Project.objects.get(pk=project_id)
        ticket_tags = Ticket.objects.filter(project=project_id)
        tasks = Task.objects.filter(ticket__in=ticket_tags)
        tag_list = []
        users = []
        user_list = []

        for ticket in ticket_tags:
            if ticket.ticket_assigned_user is not None:
                if ticket.ticket_assigned_user not in user_list:
                    user_list.append(ticket.ticket_assigned_user)

        for task in tasks:
            if task.task_assigned_user is not None:
                if task.task_assigned_user not in user_list:
                    user_list.append(task.task_assigned_user)

        for item in request.POST:
            if "tag" in item:
                tag_list.append(item.split("-")[1])
            if "user" in item:
                users.append(item.split("-")[1])

        if user_list and tag_list:
            selected_tags = Tag.objects.filter(pk__in=tag_list)
            selected_users = User.objects.filter(pk__in=users)
            tickets = Ticket.objects.filter(project=project_id).filter(Q(tags__in=selected_tags)| Q(ticket_assigned_user__in=selected_users)).distinct()
        elif tag_list:
            selected_tags = Tag.objects.filter(pk__in=tag_list)
            tickets = Ticket.objects.filter(project=project_id).filter(tags__in=selected_tags).distinct()
            selected_users = []
        elif user_list:
            selected_users = User.objects.filter(pk__in=users)
            tickets = Ticket.objects.filter(project=project_id).filter(ticket_assigned_user__in=selected_users).distinct()
            selected_tags = []

        context={
            "project_detail": project_detail,
            "tickets": tickets,
            "ticket_tags": ticket_tags,
            "selected_tags": selected_tags,
            "selected_users": selected_users,
            "user_list": user_list
        }

    return render(request, "project_details.html", context)


@login_required
def project_add(request):
    """Handles the addition of new projects from the main project board

    Returns:
        [render] -- if the request is a GET, or there is an error with the form data, will return a render of project_add.html with an error message (when applicable)
        [HttpResponseRedirect] -- when the request to POST a new project is successful, it will redirect to the main projects view with the new project added
    """
    project_form = ProjectForm()
    form_data = request.POST

    if request.method == "POST":
        completed_project_form = ProjectForm(form_data)

        if completed_project_form.is_valid():
            project_name = form_data["project_name"]
            project_description = form_data["project_description"]
            project_due = form_data["project_due"]

            if project_name == "" or project_description == "":
                context = {
                    "project_form": completed_project_form
                }

                messages.error(request, "You must complete all fields in the form")

            else:
                new_project = Project(project_name=project_name, project_description= project_description, project_due=project_due, project_created=datetime.date.today(),project_status = "Not Started")
                new_project.save()

                messages.success(request, "Project successfully saved")

                return HttpResponseRedirect(reverse("check_mate:projects"))

    else:
        context = {
            "project_form": project_form
        }
    return render(request, "project_form.html", context)


@login_required
def project_delete(request, project_id):
    """Handles checking if a project can be deleted and the deletion of appropriate projects. Projects can only be deleted if they do not have any tickets associated with them.

    Arguments:
        project_id {int} -- the id of the project we would like to delete

    Returns:
        [render] -- if the request is a GET, will return a render of project_delete.html with permissions to delete a project
        [HttpResponseRedirect] -- when the POST request to remove a project is successful, it will redirect to the main projects view with the requested project removed
    """

    if request.method == "POST":
        project= Project.objects.get(pk=project_id)
        project.delete()
        messages.success(request, "Project successfully deleted")
        return HttpResponseRedirect(reverse("check_mate:projects"))
    else:
        project = Project.objects.get(pk=project_id)

        context = {
            "project": project,
        }
        return render(request, "project_delete.html", context)


@login_required
def project_edit(request, project_id):
    """Handles rendering a pre-populated edit form with existing project data and update of project details

    Arguments:
        project_id {int} -- The id of the project we would like to edit

    Returns:
        [render] -- if the request is a GET, will return a render of project_edit.html with pre-populated information in project form
        [HttpResponseRedirect] -- when the POST request to update a project is successful, it will redirect to the project detail view with the project details updated
    """
    project = Project.objects.get(pk=project_id)
    form_data = request.POST

    if request.method == "GET":
        project_form = ProjectForm(instance=project)
        context = {
            "project": project,
            "project_form": project_form
        }

        return render(request, "project_form.html", context)

    elif request.method == "POST":
        project.project_name = form_data["project_name"]
        project.project_description = form_data["project_description"]

        if form_data["project_due"]:
            project.project_due = form_data["project_due"]

        project.save()

        messages.success(request, "Changes successfully saved")

        return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id, )))
