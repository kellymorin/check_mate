import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from check_mate.models import *
from check_mate.forms import TaskForm, TaskStatusForm
from ..utils import __update_task_history, __update_ticket_history

# Automation Notes --------------------
# When task is added to a ticket keep status as not started, until a task is set to active, or the ticket settings are manually overwritten
# While tasks are active in ticket, keep ticket status set to active
# Once all tasks are marked as complete, update ticket status to complete
# -------------------------------------------


@login_required
def task_add(request):
    # Then they should be presented with a form, where they can provide information about the task such as assigned team member

    if request.method == "POST":
        if "first_request" in request.POST:
            task_form = TaskForm()
    form_data = request.POST

    if "first_request" not in form_data:
        completed_task_form = TaskForm(form_data)

        if completed_task_form.is_valid():
            task_name = form_data["task_name"]
            task_description = form_data["task_description"]
            task_due = form_data["task_due"]
            ticket_id = form_data["ticket"]
                ticket = Ticket.objects.filter(pk=ticket_id)[0]
            project_id = ticket.project.id
            project = Project.objects.filter(pk=project_id)[0]

                if task_name == "" or task_description == "":
                # TODO: NEED TO UPDATE THIS SO IT AUTOPOPULATES FORM
                context = {
                        "error_message": "You must complete all fields in the form",
                        "task_name": task_name,
                        "task_description": task_description,
                        "task_due": task_due,
                    "task_form": task_form,
                    "ticket": ticket_id
                }

                else:
                new_task = Task(task_name=task_name, task_description=task_description, task_due=task_due, task_created=datetime.date.today(), task_status="Not Started", ticket=ticket)
                    new_task.save()

                __update_task_history(new_task, request.user, "Status", "Not Started")

                if form_data["task_assigned_user"] != "":
                    assigned_user = User.objects.get(pk=form_data["task_assigned_user"])

                    __update_task_history(new_task, request.user, "Assignment", assigned_user)

                    new_task.task_assigned_user = assigned_user

                    new_task.save()

                if ticket.ticket_status == "Complete":
                    ticket.ticket_status = "Active"
                    ticket.save()

                    __update_ticket_history(ticket, request.user, "Status", "Active")

                    if project.project_status == "Complete":
                        project.project_status = "Active"
                        project.save()

                    return HttpResponseRedirect(reverse("check_mate:ticket_details", args=(ticket_id,)))
    else:
        ticket = form_data["ticket"]
        context = {
            "task_form": task_form,
            "ticket": ticket,
            "add": True
        }
    return render(request, "task_form.html", context)


@login_required
def task_edit(request, task_id):
    # Then they should be presented with a form, that is pre-populated with existing task data, where they can update information about the task such as assigned team member

    # Automation Notes:
    # Currently set up to update ticket if task is updated, but does not currently flow through to projects

    # TODO: Need to add automation to post to task history before saving changes

    if request.method == "GET":
        task = Task.objects.get(pk=task_id)
        task_form = TaskForm(instance=task)
        task_status = TaskStatusForm(instance=task)
        ticket_id = task.ticket.id
        ticket = Ticket.objects.get(pk=ticket_id)
        template_name = "task_edit.html"
        context = {
            "task": task,
            "task_form": task_form,
            "task_status": task_status,
            "edit": True
        }
        return render(request, "task_form.html", context)
    elif request.method == "POST":
        if task.task_status != form_data["task_status"]:
            __update_task_history(task, request.user, "Status", form_data["task_status"])
        if form_data["task_assigned_user"] != "":
            assigned_user = User.objects.get(pk=form_data["task_assigned_user"])
            if task.task_assigned_user != form_data["task_assigned_user"]:
                __update_task_history(task, request.user, "Assignment", assigned_user)

            task.task_assigned_user = assigned_user

        if request.POST["task_due"]:
            task.task_name = request.POST["task_name"]
            task.task_description = request.POST["task_description"]
            task.task_status = request.POST["task_status"]
            task.task_due = request.POST["task_due"]
            task.save()
        else:
            task.task_name = request.POST["task_name"]
            task.task_description = request.POST["task_description"]
            task.task_status = request.POST["task_status"]
            task.save()
            __update_ticket_history(ticket, request.user, "Status", "Active")
            __update_ticket_history(ticket, request.user, "Status", "Complete")

            if project.get_ticket_status['Complete'] == project.get_ticket_status['Total']:
                project.project_status = "Complete"
                project.save()
            ticket.ticket_status = "Active"
            ticket.save()
            __update_ticket_history(ticket, request.user, "Status", "Active")
        return HttpResponseRedirect(reverse("check_mate:ticket_details", args=(ticket_id,)))


@login_required
def task_delete(request, task_id):

    if request.method == "POST":
        task = Task.objects.get(pk=task_id)
        ticket_id = task.ticket.id
        task.delete()
        return HttpResponseRedirect(reverse("check_mate:ticket_details", args=(ticket_id,)))
    else:
        task = Task.objects.get(pk=task_id)
        ticket_id = task.ticket.id

        if task.task_status == "Not Started":
            context = {
                "task": task,
                "can_delete": True
            }
        else:
            context={
                "task": task,
                "can_delete": False
            }
        return render(request, "task_delete.html", context)
