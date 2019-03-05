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
# When the user selects the option to add a new related task
# Then they should be presented with a form, where they can provide information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken back to the ticket detail page with the related task added
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data


# @login_required
# def task_edit(request, task_id):
# When the user selects the option to edit task details
# Then they should be presented with a form, that is pre-populated with existing task data, where they can update information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken back to the ticket detail page with the related task updated completed
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data

# @login_required
# def task_delete(request, task_id):
# And an option to delete the entire task

# When the user selects the options to delete
# Then they will be presented with an option to confirm that they would like to delete the task

# If the user confirms deletion
# Then they will be taken back to the ticket detail page, with the related task removed from the list

# If the user cancels deletion
# Then they will be taken back to the ticket detail page, with no changes made to the related task
