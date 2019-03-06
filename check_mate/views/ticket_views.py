import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from check_mate.models import *
from check_mate.forms import TicketForm, TicketStatusForm
from ..utils import __update_ticket_history

# Automation Notes --------------------
# when the first ticket is added to a project, set the project status to active, set ticket status to not started
# When task is added to a ticket keep status as not started, until a task is set to active, or the ticket settings are manually overwritten
# While tasks are active in ticket, keep ticket status set to active
# Once all tasks are marked as complete, update ticket status to complete
# -------------------------------------------

# TODO: Have not added ability to update assigned team member
# TODO: Update edit functionality to first post to the ticket history section, then to the ticket


@login_required
def ticket_detail(request, ticket_id):
    """Loads a specific ticket's detail page

    Arguments:
        ticket_id {int} -- the id of the specific ticket details being requested

    Returns:
        [render] -- returns the ticket_details.html template with specific ticket details and all associated tasks passed in
    """
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
    """Handles the addition of new tickets from the project detail view

    Returns:
        [render] -- if the request is a GET, or there is an error with the form data, will return a render of ticket_add.html with an error message (when applicable)
        [HttpResponseRedirect] -- when the request to POST a new ticket is successful, it will redirect to the project detail view with the new ticket added
    """
    # Then they should be presented with a form, where they can provide information about the task such as assigned team member

    if request.method == "POST":
        if "first_request" in request.POST:
            ticket_form = TicketForm()
    form_data = request.POST

    if "first_request" not in form_data:
        completed_ticket_form = TicketForm(form_data)

        if completed_ticket_form.is_valid():
            print(form_data)
            ticket_name = form_data["ticket_name"]
            ticket_description = form_data["ticket_description"]
            ticket_due = form_data["ticket_due"]
            project_id = form_data["project"]
                project = Project.objects.filter(pk=project_id)[0]

                if ticket_name == "" or ticket_description == "":
                context={
                        "error_message": "You must complete all fields in the form",
                        "ticket_name": ticket_name,
                        "ticket_description": ticket_description,
                    "ticket_due": ticket_due,
                    "ticket_form": ticket_form,
                    "project": project_id
                }

                else:
                    new_ticket = Ticket(ticket_name=ticket_name, ticket_description=ticket_description, ticket_due= ticket_due, ticket_created = datetime.date.today(), ticket_status="Not Started", project=project)
                    new_ticket.save()

                __update_ticket_history(new_ticket, request.user, "Status", "Not Started")

                if form_data["ticket_assigned_user"] != "":
                    assigned_user = User.objects.get(pk=form_data["ticket_assigned_user"])

                    __update_ticket_history(new_ticket, request.user, "Assignment", assigned_user)

                    new_ticket.ticket_assigned_user = assigned_user

                    new_ticket.save()

                if project.project_status == "Complete":
                    project.project_status = "Active"
                    project.save()

                    return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id,)))

    else:
        project = form_data["project"]
        context = {
            "ticket_form": ticket_form,
            "project": project,
            "add": True
        }
    return render(request, "ticket_form.html", context)


@login_required
def ticket_delete(request, ticket_id):
    """Handles checking if a ticket can be deleted and the deletion of appropriate tickets. Tickets can only be deleted if they do not have any tasks associated with them

    Arguments:
        ticket_id {int} -- the id of the ticket we are trying to delete

    Returns:
        [render] -- if the reuqest is a GET, will return a render of ticket_delete.html with permissions to delete a ticket
        [HttpResponseRedirect] -- when the POST request to remove a ticket is successful, it will redirect to the project detail view with the requested ticket removed
    """

    if request.method == "POST":
        ticket = Ticket.objects.get(pk=ticket_id)
        project_id = ticket.project.id
        ticket.delete()
        return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id,)))
    else:
        ticket = Ticket.objects.get(pk=ticket_id)
        tasks = Task.objects.filter(ticket=ticket_id)

        if len(tasks) == 0:
            context = {
                "ticket": ticket,
                "can_delete": True
            }
        else:
            context={
                "ticket": ticket,
                "can_delete": False
            }
        return render(request, "ticket_delete.html", context)


# TODO: UPDATE TO INCLUDE SUMMARY
@login_required
def ticket_edit(request, ticket_id):
    """[summary]

    Arguments:
        ticket_id {int} -- The id of the ticket we would like to edit

    Returns:
        [render] -- if the request is a GET, will return a render of ticket_edit.html with pre-populated information in ticket form
        [HttpResponseRedirect] -- when the POST request to update a ticket is successful, it will redirect to the ticket detail view with the ticket details updated
    """

    if request.method == "GET":
        ticket = Ticket.objects.get(pk=ticket_id)
        ticket_form = TicketForm(instance=ticket)
        ticket_status = TicketStatusForm(instance=ticket)
        template_name = "ticket_edit.html"
        context = {
            "ticket": ticket,
            "ticket_form": ticket_form,
            "ticket_status": ticket_status,
        }
        return render(request, "ticket_form.html", context)
    elif request.method == "POST":
        if ticket.ticket_status != form_data["ticket_status"]:
            __update_ticket_history(ticket, request.user, "Status", form_data["ticket_status"])
        if form_data["ticket_assigned_user"] != "":
            assigned_user = User.objects.get(pk=form_data["ticket_assigned_user"])
            if ticket.ticket_assigned_user != form_data["ticket_assigned_user"]:
                __update_ticket_history(ticket, request.user, "Assignment", assigned_user)

            ticket.ticket_assigned_user = assigned_user

        if request.POST["ticket_due"]:
            ticket.ticket_name = request.POST["ticket_name"]
            ticket.ticket_description = request.POST["ticket_description"]
            ticket.ticket_status = request.POST["ticket_status"]
            ticket.ticket_due = request.POST["ticket_due"]
            ticket.save()
        else:
            ticket.ticket_name = request.POST["ticket_name"]
            ticket.ticket_description = request.POST["ticket_description"]
            ticket.ticket_status = request.POST["ticket_status"]
            ticket.save()
        if request.POST["ticket_status"] == "Active" and project.project_status == "Not Started":
            project.project_status = "Active"
            project.save()
        return HttpResponseRedirect(reverse("check_mate:ticket_details", args=(ticket_id,)))