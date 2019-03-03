from django.shortcuts import render
from check_mate.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from check_mate.forms import ProjectForm

# TODO: Implement edit functionality
# TODO: Update project details to include due date
# TODO: Add the ability to filter from all projects, current projects, previous projects

@login_required
def projects(request):
    projects = Project.objects.all()
    context = {
        "projects": projects
    }
    return render(request, 'projects.html', context)

@login_required
def project_details(request, project_id):
    project_detail = Project.objects.filter(pk=project_id)[0]
    tickets = Ticket.objects.filter(project=project_id)
    print(project_detail)
    context = {
        "project_detail": project_detail,
        "tickets": tickets
    }
    return render(request, "project_details.html", context)

@login_required
def project_add(request):
    if request.method == "GET":
        project_form = ProjectForm()
        template_name = "project_add.html"
        context={
            "project_form": project_form
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        try:
            project_name = request.POST["project_name"]
            project_description = request.POST["project_description"]
            if project_name == "" or project_description == "":
                return render(request, "project_add.html", {
                    "error_message": "You must complete all fields in the form",
                    "project_name": project_name,
                    "project_description": project_description
                })
            else:
                new_project = Project(project_name=project_name, project_description= project_description)
                new_project.save()

                return HttpResponseRedirect(reverse("check_mate:projects"))
        except KeyError:
            return render(request, "project_add.html", {
                "error_message": "You must complete all fields in the form"
            })

@login_required
def project_delete(request, project_id):
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