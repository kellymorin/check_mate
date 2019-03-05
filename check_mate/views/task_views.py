import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from check_mate.models import *
from check_mate.forms import TaskForm, TaskStatusForm

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
            ticket = request.POST["ticket"]
            template_name = "task_add.html"
            context = {
                "task_form": task_form,
                "ticket": ticket
            }
            return render(request, template_name, context)
        else:
            try:
                task_name = request.POST["task_name"]
                task_description = request.POST["task_description"]
                task_due = request.POST["task_due"]
                ticket_id = request.POST["ticket"]
                ticket = Ticket.objects.filter(pk=ticket_id)[0]
                if task_name == "" or task_description == "":
                    return render(request, "task_add.html", {
                        "error_message": "You must complete all fields in the form",
                        "task_name": task_name,
                        "task_description": task_description,
                        "task_due": task_due,
                        "task_form" : TaskForm()
                    })
                else:
                    new_task = Task(task_name= task_name, task_description = task_description, task_due = task_due, task_created = datetime.date.today(), task_status = "Not Started", ticket=ticket)
                    new_task.save()

                    return HttpResponseRedirect(reverse("check_mate:ticket_details", args=(ticket_id,)))
            except KeyError:
                return render(request, "task_add.html", {
                    "error_message": "You must complete all fields in the form"
                })


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
            "ticket": ticket
        }
        return render(request, template_name, context)
    elif request.method == "POST":
        task = Task.objects.get(pk=task_id)
        ticket_id = task.ticket.id
        ticket = Ticket.objects.get(pk=ticket_id)

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
        if request.POST["task_status"] == "Active" and ticket.ticket_status == "Not Started":
            ticket.ticket_status = "Active"
            ticket.save()
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
