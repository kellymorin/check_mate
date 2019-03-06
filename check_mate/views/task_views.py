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
    """Handles rendering a pre-populated edit form with existing task data and update of task details

    Arguments:
        task_id {int} -- The id of the task we would like to edit

    Returns:
        [render] -- if the request is a GET, will return a render of task_edit.html with pre-populated information in task form
        [HttpResponseRedirect] -- when the POST request to update a task is successful, it will redirect to the ticket detail view with the task details updated
    """

        task = Task.objects.get(pk=task_id)
        ticket_id = task.ticket.id
        ticket = Ticket.objects.get(pk=ticket_id)
    project_id = ticket.project.id
    project = Project.objects.get(pk=project_id)
    form_data = request.POST

    if request.method == "GET":
        task_form = TaskForm(instance=task)
        task_status = TaskStatusForm(instance=task)
        context = {
            "task": task,
            "task_form": task_form,
            "task_status": task_status,
            "ticket": ticket_id,
            "edit": True
        }

        return render(request, "task_form.html", context)

    elif request.method == "POST":

        if task.task_status != form_data["task_status"]:
            __update_task_history(task, request.user, "Status", form_data["task_status"])

        task.task_name = form_data["task_name"]
        task.task_status = form_data["task_status"]
        task.task_description = form_data["task_description"]

        if form_data["task_due"]:
            task.task_due = form_data["task_due"]

        if form_data["task_assigned_user"] != "":
            assigned_user = User.objects.get(pk=form_data["task_assigned_user"])
            if task.task_assigned_user != form_data["task_assigned_user"]:
                __update_task_history(task, request.user, "Assignment", assigned_user)

            task.task_assigned_user = assigned_user

            task.save()

        if form_data["task_status"] == "Active" and ticket.ticket_status == "Not Started":
            ticket.ticket_status = "Active"
            ticket.save()

            __update_ticket_history(ticket, request.user, "Status", "Active")

        if ticket.get_task_status['Complete'] == ticket.get_task_status['Total']:
            ticket.ticket_status = "Complete"
            ticket.save()

            __update_ticket_history(ticket, request.user, "Status", "Complete")

            if project.get_ticket_status['Complete'] == project.get_ticket_status['Total']:
                project.project_status = "Complete"
                project.save()

        if task.task_status != "Complete" and ticket.ticket_status == "Complete":
            ticket.ticket_status = "Active"
            ticket.save()

            __update_ticket_history(ticket, request.user, "Status", "Active")

            if project.project_status == "Complete":
                project.project_status = "Active"
                project.save()

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
