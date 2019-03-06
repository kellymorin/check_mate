import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from check_mate.models import *
from check_mate.forms import ProjectForm

# Non-MVP Notes--------------------------------------------------------------
# TODO: Add the ability to filter from all projects, current projects, previous projects
# TODO: Consider consolodiating add and edit to run through one view and one template
# ---------------------------------------------------------------------------


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
def project_details(request, project_id):
    """This function loads a specific project's detail page

    Arguments:
        project_id {int} -- the id of the specific project details being requested

    Returns:
        [render] -- returns the project_details.html template with specific project details and all associated tickets passed in
    """

    project_detail = Project.objects.filter(pk=project_id)[0]
    tickets = Ticket.objects.filter(project=project_id)
    context = {
        "project_detail": project_detail,
        "tickets": tickets
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
                    "error_message": "You must complete all fields in the form",
                    "project_name": project_name,
                    "project_description": project_description,
                    "project_form": project_form,
                    "project_due": project_due
                }

            else:
                new_project = Project(project_name=project_name, project_description= project_description, project_due=project_due, project_created=datetime.date.today(),project_status = "Not Started")
                new_project.save()

                return HttpResponseRedirect(reverse("check_mate:projects"))

    else:
        context = {
            "project_form": project_form,
        }
    return render(request, "project_add.html", context)


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
        return HttpResponseRedirect(reverse("check_mate:projects"))
    else:
        project = Project.objects.get(pk=project_id)
        tickets = Ticket.objects.filter(project=project_id)

        if len(tickets) == 0:
            context = {
                "project": project,
                "can_delete": True
            }
        else:
            context = {
                "project": project,
                "can_delete": False
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

        return render(request, "project_edit.html", context)

    elif request.method == "POST":
        project.project_name = form_data["project_name"]
        project.project_description = form_data["project_description"]

        if form_data["project_due"]:
            project.project_due = form_data["project_due"]

        project.save()

        return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id, )))
