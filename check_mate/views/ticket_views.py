import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from check_mate.models import *
from check_mate.forms import TicketForm

# Automation Notes --------------------
# when the first ticket is added to a project, set the project status to active, set ticket status to not started
# When task is added to a ticket keep status as not started, until a task is set to active, or the ticket settings are manually overwritten
# While tasks are active in ticket, keep ticket status set to active
# Once all tasks are marked as complete, update ticket status to complete
# -------------------------------------------


@login_required
def ticket_detail(request, ticket_id):
# When the user selects the ticket detail view
# Then they should be able to see the assigned team member, activity history

    ticket_detail = Ticket.objects.filter(pk=ticket_id)[0]
    tasks = Task.objects.filter(ticket=ticket_id)
    context={
        "ticket_detail": ticket_detail,
        "tasks": tasks
    }
    return render(request, "ticket_details.html", context)


@login_required
def ticket_add(request):

# When the user selects the option to add a new issue ticket
# Then they should be presented with a form, where they can provide information about the task such as name, description, status and assigned team member

    if request.method == "POST":
        if "first_request" in request.POST:
            ticket_form = TicketForm()
            project = request.POST["project"]
            template_name = "ticket_add.html"
            context = {
                "ticket_form": ticket_form,
                "project": project
            }
            return render(request, template_name, context)
        else:
            try:
                ticket_name = request.POST["ticket_name"]
                ticket_description = request.POST["ticket_description"]
                ticket_due = request.POST["ticket_due"]
                project_id = request.POST["project"]
                project = Project.objects.filter(pk=project_id)[0]
                if ticket_name == "" or ticket_description == "":
                    return render(request, "ticket_add.html", {
                        "error_message": "You must complete all fields in the form",
                        "ticket_name": ticket_name,
                        "ticket_description": ticket_description,
                        "ticket_due": ticket_due
                    })
                else:
                    new_ticket = Ticket(ticket_name=ticket_name, ticket_description=ticket_description, ticket_due= ticket_due, ticket_created = datetime.date.today(), ticket_status="Not Started", project=project)
                    new_ticket.save()

                    return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id,)))
            except KeyError:
                return render(request, "ticket_add.html", {
                    "error_message": "You must complete all fields in the form"
                })


# login_required
# def ticket_edit(request, ticket_id):
# Given a user is authenticated
# When the user is viewing a issue ticket detail view
# Then the user should be able to view all details of the ticket, including name, description, ticket status, completion status bar, ticket history and all related tasks
# And they should be given an affordance to edit the details of the issue ticket

# When the user selects the option to edit ticket details
# Then they should be presented with a form, that is pre-populated with existing ticket data, where they can update information about the task such as name, description, status and assigned team member

# When the user submits the form
# If the data is valid, they will be taken back to the updated ticket detail page
# If the data is not valid, they will be shown an error message on the form and asked to supply valid data