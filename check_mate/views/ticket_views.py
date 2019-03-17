import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from check_mate.models import *
from check_mate.forms import TicketForm, TicketStatusForm
from ..utils import __update_ticket_history, __get_ticket_detail_history_descriptions

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

# TODO: Need to be able to delete tags that are no longer being used
# TODO: Ticket History should be updated with tag changes
# TODO: Task History should be updated with tag changes



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

    all_history = __get_ticket_detail_history_descriptions(ticket_history, task_history, request)

    context={
        "ticket_detail": ticket_detail,
        "all_history": all_history,
        "tasks": tasks,
        "all_tasks":tasks
    }
    return render(request, "ticket_details.html", context)

@login_required
def ticket_filter_tags(request, ticket_id):

    ticket_detail = Ticket.objects.get(pk=ticket_id)
    ticket_history = TicketHistory.objects.filter(ticket=ticket_id).order_by('activity_date')
    tasks = Task.objects.filter(ticket = ticket_id)
    task_history = []
    for task in tasks:
        task_history.append(TaskHistory.objects.filter(task=task.id))

    all_history = __get_ticket_detail_history_descriptions(ticket_history, task_history, request)

    if request.method == "POST":
        tags = []
        for item in request.POST:
            if "tag" in item:
                tags.append(item.split("-")[1])

        filtered_tasks = Task.objects.filter(ticket=ticket_id).filter(tags__in=tags).distinct()
        selected_tags = Tag.objects.filter(pk__in=tags)

        context = {
            "ticket_detail": ticket_detail,
            "all_history": all_history,
            "tasks": filtered_tasks,
            "selected_tags": selected_tags,
            "all_tasks": tasks
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
        completed_ticket_form = TicketForm(data=form_data, user=request.user)

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
            for tag in tags:
                try:
                    new_ticket.tags.add(Tag.objects.get(pk=tag))
                except ValueError:
                    new_ticket.tags.add(Tag.objects.create(tag_name=tag, user=request.user))


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
            if str(old_tag.id) not in new_tags:
                instance = Tag.objects.get(pk=old_tag.id)
                ticket.tags.remove(instance)
            elif str(old_tag.id) in new_tags:
                new_tags.remove(str(old_tag.id))

        # Add the remaining tags
        for tag in new_tags:
            try:
                ticket.tags.add(Tag.objects.get(pk=tag))
            except ValueError:
                ticket.tags.add(Tag.objects.create(tag_name=tag, user=request.user))


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