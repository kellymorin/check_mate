import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from check_mate.models import *
from check_mate.forms import TicketForm, TicketStatusForm
from ..utils import __update_ticket_history

# Automation Notes --------------------
# when the first ticket is added to a project, set the project status to not started, set ticket status to not started
# When task is added to a ticket keep status as not started, until a task is set to active, or the ticket settings are manually overwritten
# While tasks are active in ticket, keep ticket status set to active, and project status to active
# Once all tasks are marked as complete, update ticket status to complete
# Once all tickets are marked as complete, update project status to complete
# -------------------------------------------

# Style Notes ----------------------------------------------------------
# V2: On ticket edit form, see if I can set limitations on when a due date can be set for, based on when the parent items due date is
# -----------------------------------------------------------------------



@login_required
def ticket_detail(request, ticket_id):
    """Loads a specific ticket's detail page

    Arguments:
        ticket_id {int} -- the id of the specific ticket details being requested

    Returns:
        [render] -- returns the ticket_details.html template with specific ticket details and all associated tasks passed in
    """
    # Then they should be able to see the assigned team member, activity history

    ticket_detail = Ticket.objects.get(pk=ticket_id)

    ticket_history = TicketHistory.objects.filter(ticket=ticket_id).order_by('activity_date')
    tasks = Task.objects.filter(ticket=ticket_id)
    task_history = []

    for task in tasks:
        task_history.append(TaskHistory.objects.filter(task=task.id))

    all_history = []

    for item in ticket_history:
        ticket = {}
        ticket["activity_date"] = item.activity_date
        if item.activity_type == "Status":
            if item.ticket_active_user == request.user:
                ticket["description"] = f"You updated the status of {item.ticket.ticket_name} to {item.status}"
            else:
                ticket["description"] = f"{item.ticket_active_user.first_name} {item.ticket_active_user.last_name} updated the status of {item.ticket.ticket_name} to {item.status}"
        elif item.activity_type == "Assignment":
            if item.ticket_active_user == request.user:
                if item.ticket_affected_user == request.user:
                    ticket["description"] = f"You self-assigned {item.ticket.ticket_name} ticket"
                else:
                    ticket["description"] = f"You assigned {item.ticket.ticket_name} ticket to {item.ticket_affected_user.first_name} {item.ticket_affected_user.last_name}"
            else:
                if item.ticket_affected_user == request.user:
                    ticket["description"] = f"{item.ticket_active_user.first_name} {item.ticket_active_user.last_name} assigned {item.ticket.ticket_name} ticket to you"
                elif item.ticket_affected_user == item.ticket_active_user:
                    ticket["description"] = f"{item.ticket_active_user.first_name} {item.ticket_active_user.last_name}  self-assigned {item.ticket.ticket_name} ticket"
                else:
                    ticket["description"] = f"{item.ticket_active_user.first_name} {item.ticket_active_user.last_name}  assigned {item.ticket.ticket_name} ticket to {item.ticket_affected_user.first_name} {item.ticket_affected_user.last_name}"
        all_history.append(ticket)

    for query_set in task_history:
        for item in query_set:
            task = {}
            task["activity_date"] = item.activity_date
            if item.activity_type == "Status":
                if item.task_active_user == request.user:
                    task["description"] = f"You updated the status of {item.task.task_name} to {item.status}"
                else:
                    task["description"] = f"{item.task_active_user.first_name} {item.task_active_user.last_name} updated the status of {item.task.task_name} to {item.status}"
            elif item.activity_type == "Assignment":
                if item.task_active_user == request.user:
                    if item.task_affected_user == request.user:
                        task["description"] = f"You self-assigned {item.task.task_name} task"
                    else:
                        task["description"] = f"You assigned {item.task.task_name} task to {item.task_affected_user.first_name} {item.task_affected_user.last_name}"
                else:
                    if item.task_affected_user == request.user:
                        task["description"] = f"{item.task_active_user.first_name} {item.task_active_user.last_name} assigned {item.task.task_name} task to you"
                    elif item.task_affected_user == item.task_active_user:
                        task["description"] = f"{item.task_active_user.first_name} {item.task_active_user.last_name} self-assigned {item.task.task_name} task"
                    else:
                        task["description"] = f"{item.task_active_user.first_name} {item.task_active_user.last_name} assigned {item.task.task_name} task to {item.task_affected_user.first_name} {item.task_affected_user.last_name}"
            all_history.append(task)

    context={
        "ticket_detail": ticket_detail,
        "all_history": all_history
    }
    return render(request, "ticket_details.html", context)


@login_required
def ticket_add(request):
    """Handles the addition of new tickets from the project detail view

    Returns:
        [render] -- if the request is a GET, or there is an error with the form data, will return a render of ticket_form.html with an error message (when applicable)
        [HttpResponseRedirect] -- when the request to POST a new ticket is successful, it will redirect to the project detail view with the new ticket added
    """

    ticket_form = TicketForm(user=request.user)
    form_data = request.POST

    if "first_request" not in form_data:
        completed_ticket_form = TicketForm(form_data)

        # if completed_ticket_form.is_valid():
        print(request.POST)
        ticket_name = form_data["ticket_name"]
        ticket_description = form_data["ticket_description"]
        ticket_due = form_data["ticket_due"]
        project_id = form_data["project"]
        project = Project.objects.get(pk=project_id)

        if ticket_name == "" or ticket_description == "":
            context={
                "ticket_form": completed_ticket_form,
                "project": project_id
            }

            messages.error(request, "You must complete all fields in the form")

        else:
            new_ticket = Ticket.objects.create(
                ticket_name=ticket_name, ticket_description=ticket_description,
                ticket_due= ticket_due,
                ticket_created = datetime.date.today(), ticket_status="Not Started",
                project=project
            )

            # Loop through submitted tags and add existing or create a new one
            tags = form_data.getlist("tags")
            print(tags)
            for tag in tags:
                print(tag)
                try:
                    new_ticket.tags.add(Tag.objects.get(pk=tag))
                except ValueError:
                    new_ticket.tags.add(Tag.objects.create(name=tag, user=request.user))


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

            messages.success(request, "Ticket successfully saved")

            return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id,)))

    else:
        project = form_data["project"]
        context = {
            "ticket_form": ticket_form,
            "project": project
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
        messages.success(request, "Ticket successfully deleted")
        return HttpResponseRedirect(reverse("check_mate:project_details", args=(project_id,)))
    else:
        ticket = Ticket.objects.get(pk=ticket_id)

        context = {
            "ticket": ticket,
        }
        return render(request, "ticket_delete.html", context)


@login_required
def ticket_edit(request, ticket_id):
    """Handles rendering a pre-populated edit form with existing ticket data and update of ticket details

    Arguments:
        ticket_id {int} -- The id of the ticket we would like to edit

    Returns:
        [render] -- if the request is a GET, will return a render of ticket_form.html with pre-populated information in ticket form
        [HttpResponseRedirect] -- when the POST request to update a ticket is successful, it will redirect to the ticket detail view with the ticket details updated
    """
    ticket = Ticket.objects.get(pk=ticket_id)
    project_id = ticket.project.id
    project = Project.objects.get(pk=project_id)
    form_data = request.POST

    if request.method == "GET":
        ticket_form = TicketForm(instance=ticket, user=request.user)
        ticket_status = TicketStatusForm(instance=ticket)
        context = {
            "ticket": ticket,
            "ticket_form": ticket_form,
            "ticket_status": ticket_status
        }

        return render(request, "ticket_form.html", context)

    elif request.method == "POST":

        if ticket.ticket_status != form_data["ticket_status"]:
            __update_ticket_history(ticket, request.user, "Status", form_data["ticket_status"])

        ticket.ticket_name = form_data["ticket_name"]
        ticket.ticket_description = form_data["ticket_description"]
        ticket.ticket_status = form_data["ticket_status"]

        if form_data["ticket_due"]:
            ticket.ticket_due = form_data["ticket_due"]

        if form_data["ticket_assigned_user"] != "":
            assigned_user = User.objects.get(pk=form_data["ticket_assigned_user"])
            if ticket.ticket_assigned_user != form_data["ticket_assigned_user"]:
                __update_ticket_history(ticket, request.user, "Assignment", assigned_user)

            ticket.ticket_assigned_user = assigned_user

        ticket.save()

        # Check if tags were changed. removew or add as needed
        new_tags = form_data.getlist("tags")
        old_tags = ticket.tags.all()

        # Compare new list with old list
        # If old tag is not in new list, remove the relation
        # If old tag is in new list, remove it from the list, to be left with only new tags to add
        for old_tag in old_tags:


        if form_data["ticket_status"] == "Active" and project.project_status == "Not Started":
            project.project_status = "Active"
            project.save()

        if project.get_ticket_status['Complete'] == project.get_ticket_status['Total']:
            project.project_status = "Complete"
            project.save()

        if ticket.ticket_status != "Complete" and project.project_status == "Complete":
            project.project_status = "Active"
            project.save()

        messages.success(request, "Ticket updates successfully saved")
        return HttpResponseRedirect(reverse("check_mate:ticket_details", args=(ticket_id,)))