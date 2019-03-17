import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from check_mate.models import *
from dateutil.relativedelta import relativedelta, FR

# Non-MVP Notes -----------------------------------------
# V2: Update stand up view so that if someone else has already claimed a ticket for the day, that displays on everyone else's view
# -------------------------------------------------------



@login_required
def stand_up_view(request):
    # if no tickets have been claimed for today's stand up, show the option to select tickets
    today = datetime.date.today()
    previous_date = ""

    if today.weekday() == 0:
        previous_date = today + relativedelta(weekday=FR(-1))

    else:
        previous_date = today - datetime.timedelta(1)

    projects = Project.objects.all()
    tasks = Task.objects.filter(task_created=previous_date).order_by('task_name')
    tickets = Ticket.objects.filter(ticket_created=previous_date).order_by('ticket_name')
    road_blocked_tickets = Ticket.objects.filter(ticket_status = "Road Block")
    road_blocked_tasks = Task.objects.filter(task_status = "Road Block")
    claimed_tickets = StandUpTickets.objects.filter(date = today).filter(user = request.user.id)
    claimed_tasks = StandUpTasks.objects.filter(date = today).filter(user = request.user.id)

    ticket_activity = TicketHistory.objects.filter(activity_date = previous_date).filter(ticket_active_user = request.user.id).order_by('ticket__ticket_name')
    task_activity = TaskHistory.objects.filter(activity_date= previous_date).filter(task_active_user = request.user.id).order_by('task__task_name')

    task_history = dict()
    for task in task_activity:
        try:
            task_history[task.task.task_name].append(task)
        except:
            task_history[task.task.task_name] = list()
            task_history[task.task.task_name].append(task)

    ticket_history = dict()
    for ticket in ticket_activity:
        try:
            ticket_history[ticket.ticket.ticket_name].append(ticket)
        except:
            ticket_history[ticket.ticket.ticket_name] = list()
            ticket_history[ticket.ticket.ticket_name].append(ticket)

    context={
        'projects': projects,
        'task_activity': task_history,
        'tasks': tasks,
        'tickets': tickets,
        'ticket_activity': ticket_history,
        'road_blocked_tickets': road_blocked_tickets,
        'road_blocked_tasks': road_blocked_tasks,
        'claimed_tickets': claimed_tickets,
        'claimed_tasks': claimed_tasks
    }

    return render(request, "stand_up.html", context)

@login_required
def filter_stand_up(request):
    today = datetime.date.today()
    previous_date = ""

    if today.weekday() == 0:
        previous_date = today + relativedelta(weekday=FR(-1))

    else:
        previous_date = today - datetime.timedelta(1)

    if request.method == "POST":
        selected_projects = []
        selected_tickets = []
        selected_tasks = []

        # Loop through the projects selected to filter by and append their ID's to the selected_project list
        for item in request.POST:
            if "project" in item:
                selected_projects.append(item.split("-")[1])

        # Find all projects that are part of the filtered projects
        all_projects = Project.objects.filter(pk__in=selected_projects)

        # Find all tickets that are assigned to those projects
        all_tickets = Ticket.objects.filter(project__in=selected_projects)

        # Loop through tickets that have been selected and append their ID's to the selected_tickets list
        for ticket in all_tickets:
            selected_tickets.append(ticket.id)

        all_tasks = Task.objects.filter(ticket__in=selected_tickets)

        # Loop through the tasks that have been selected and append their ID's to the selected_tasks list
        for task in all_tasks:
            selected_tasks.append(task.id)


        # Get all tickets that were created yesterday and are part of selected projects
        tickets = Ticket.objects.filter(ticket_created=previous_date).filter(project__in=selected_projects).order_by('ticket_name')

        # Get all tasks that were created yesterday and are part of selected tickets
        tasks = Task.objects.filter(task_created=previous_date).filter(ticket__in=selected_tickets).order_by('task_name')

        # Get all tickets that are marked as road blocks and are part of the selected projects
        road_blocked_tickets = Ticket.objects.filter(ticket_status = "Road Block").filter(project__in=selected_projects)

        # Get all tasks that are marked as road blocks and are part of the selected tickets
        road_blocked_tasks = Task.objects.filter(task_status = "Road Block").filter(ticket__in=selected_tickets)

        # Get all tickets that have been claimed by the user and are part of the selected projects
        claimed_tickets = StandUpTickets.objects.filter(date = today).filter(user = request.user.id).filter(ticket__in=selected_tickets)

        # Get all tasks that have been claimed by the user and are part of the selected tickets
        claimed_tasks = StandUpTasks.objects.filter(date=today).filter(user=request.user.id).filter(task__in=selected_tasks)

        # Get all activity related to selected tickets
        ticket_activity = TicketHistory.objects.filter(activity_date = previous_date).filter(ticket_active_user = request.user.id).filter(ticket__in=selected_tickets).order_by('ticket__ticket_name')

        # Get all activity related to selected tasks
        task_activity = TaskHistory.objects.filter(activity_date=previous_date).filter(task_active_user=request.user.id).filter(task__in=selected_tasks).order_by('task__task_name')

        task_history = dict()
        for task in task_activity:
            try:
                task_history[task.task.task_name].append(task)
            except:
                task_history[task.task.task_name] = list()
                task_history[task.task.task_name].append(task)

        ticket_history = dict()
        for ticket in ticket_activity:
            try:
                ticket_history[ticket.ticket.ticket_name].append(ticket)
            except:
                ticket_history[ticket.ticket.ticket_name] = list()
                ticket_history[ticket.ticket.ticket_name].append(ticket)

        projects = Project.objects.all()

        context = {
            "projects": projects,
            "selected_projects": all_projects,
            "tickets": tickets,
            "tasks": tasks,
            "road_blocked_tickets": road_blocked_tickets,
            "road_blocked_tasks": road_blocked_tasks,
            "claimed_tickets": claimed_tickets,
            "claimed_tasks": claimed_tasks,
            "ticket_activity": ticket_history,
            "task_activity": task_history,
        }

    return render(request, "stand_up.html", context)


def claim_tickets_tasks(request):

    today = datetime.date.today()

    # When request is POST, claim tickets and redirect to stand up view
    if request.method == "POST":
        for item in request.POST:
            if "task" in item or "ticket" in item:
                if "task" in item:
                    task_id = item.split('-')[1]
                    task = Task.objects.get(pk=task_id)
                    StandUpTasks.objects.create(task=task, user=request.user, date= today)
                    # print("task",task_list)
                else:
                    ticket_id = item.split('-')[1]
                    ticket = Ticket.objects.get(pk=ticket_id)
                    StandUpTickets.objects.create(ticket=ticket, user=request.user, date=today)

        return HttpResponseRedirect(reverse("check_mate:stand-up"))

    elif request.path == "/stand-up/claim/view-all":
        # Find tickets and tasks assigned to user that are not closed
        assigned_tickets = Ticket.objects.filter(ticket_assigned_user = request.user.id).exclude(ticket_status = "Complete")
        assigned_tasks = Task.objects.filter(task_assigned_user = request.user.id).exclude(task_status = "Complete")

        # Find all tickets or tasks that are past due and not assigned to the user
        past_due_tickets = Ticket.objects.filter(ticket_due__lte=today).exclude(ticket_status = "Complete").exclude(ticket_assigned_user = request.user.id)
        past_due_tasks = Task.objects.filter(task_due__lte=today).exclude(task_status = "Complete").exclude(task_assigned_user = request.user.id)

        # Find tickets or tasks currently ready for review that are not assigned to user
        review_tickets = Ticket.objects.filter(ticket_status = "Ready for Review").exclude(ticket_assigned_user = request.user.id)
        review_tasks = Task.objects.filter(task_status = "Ready for Review").exclude(task_assigned_user = request.user.id)

        # Find tickets or tasks not assigned to the user, where the status is not Ready for Review or Complete, and the due date is in the future
        other_tickets = Ticket.objects.all().exclude(ticket_assigned_user = request.user.id).exclude(ticket_status = "Ready for Review").exclude(ticket_status = "Complete").exclude(ticket_due__lte=today)
        other_tasks = Task.objects.all().exclude(task_assigned_user = request.user.id).exclude(task_status = "Ready for Review").exclude(task_status = "Complete").exclude(task_due__lte=today)

        context = {
            "assigned_tickets": assigned_tickets,
            "assigned_tasks": assigned_tasks,
            "past_due_tickets": past_due_tickets,
            "past_due_tasks": past_due_tasks,
            "review_tickets": review_tickets,
            "review_tasks": review_tasks,
            "other_tickets": other_tickets,
            "other_tasks":other_tasks
        }

    else:
        # Find tickets and tasks assigned to user that are not closed
        assigned_tickets = Ticket.objects.filter(ticket_assigned_user = request.user.id).exclude(ticket_status = "Complete")
        assigned_tasks = Task.objects.filter(task_assigned_user = request.user.id).exclude(task_status = "Complete")

        # Find all tickets or tasks that are past due and not assigned to the user
        past_due_tickets = Ticket.objects.filter(ticket_due__lte=today).exclude(ticket_status = "Complete").exclude(ticket_assigned_user = request.user.id)
        past_due_tasks = Task.objects.filter(task_due__lte=today).exclude(task_status = "Complete").exclude(task_assigned_user = request.user.id)

        # Find tickets or tasks currently ready for review that are not assigned to user
        review_tickets = Ticket.objects.filter(ticket_status = "Ready for Review").exclude(ticket_assigned_user = request.user.id)
        review_tasks = Task.objects.filter(task_status = "Ready for Review").exclude(task_assigned_user = request.user.id)

        context = {
            "assigned_tickets": assigned_tickets,
            "assigned_tasks": assigned_tasks,
            "past_due_tickets": past_due_tickets,
            "past_due_tasks": past_due_tasks,
            "review_tickets": review_tickets,
            "review_tasks": review_tasks
        }


    # IDEAL FEATURE: Once a ticket has been claimed for the day, it will not display in other users options to claim (unless it's a review)

    return render(request, "claim.html", context)

def remove_claim(request):
    today = datetime.date.today()

    if request.method == "POST":
        # Check if claimed items were changed. Remove or add as needed
        today_claimed_tasks = StandUpTasks.objects.filter(user=request.user).filter(date=today)
        new_claimed_tasks = list()

        # Check if claimed tickets were changed. Remove or add as needed
        today_claimed_tickets = StandUpTickets.objects.filter(user=request.user).filter(date=today)
        new_claimed_tickets = list()

        for item in request.POST:
            if "task" in item or "ticket" in item:
                if "task" in item:
                    task_id = item.split('-')[1]
                    new_claimed_tasks.append(task_id)
                else:
                    ticket_id = item.split("-")[1]
                    new_claimed_tickets.append(ticket_id)

        # Compare new list with old list
        for stand_up_task in today_claimed_tasks:
            if str(stand_up_task.task.id) not in new_claimed_tasks:
                instance = StandUpTasks.objects.get(pk=stand_up_task.id)
                instance.delete()
            elif str(stand_up_task.task.id) in new_claimed_tasks:
                new_claimed_tasks.remove(str(stand_up_task.task.id))

        # Add the remaining claimed tasks
        for task in new_claimed_tasks:
            StandUpTasks.objects.create(
                task=Task.objects.get(pk=task),
                user=request.user,
                date=today
            )

        # Compare new list with old list
        for stand_up_ticket in today_claimed_tickets:
            if str(stand_up_ticket.ticket.id) not in new_claimed_tickets:
                instance = StandUpTickets.objects.get(pk=stand_up_ticket.id)
                instance.delete()
            elif str(stand_up_ticket.ticket.id) in new_claimed_tickets:
                new_claimed_tickets.remove(str(stand_up_ticket.ticket.id))

        # Add the remaining claimed tickets
        for ticket in new_claimed_tickets:
            StandUpTickets.objects.create(
                ticket= Ticket.objects.get(pk=ticket),
                user=request.user,
                date=today
            )


        return HttpResponseRedirect(reverse("check_mate:stand-up"))

    else:
        # Get all tickets that have been claimed by the user for today
        claimed_tickets = StandUpTickets.objects.filter(date = today).filter(user = request.user.id)

        # Get a list of ticket IDs in the claimed tickets query set
        ticket_id_list = list(StandUpTickets.objects.filter(date=today).filter(user=request.user.id).values_list("ticket", flat=True))

        # Find all tickets that have been assigned to the user, are not complete, and are not currently claimed by the user for today
        assigned_tickets = Ticket.objects.filter(ticket_assigned_user = request.user.id).exclude(ticket_status = "Complete").exclude(id__in=ticket_id_list)

        # Get all tasks that have been claimed by the user for today
        claimed_tasks = StandUpTasks.objects.filter(date = today).filter(user = request.user.id)

        # Get a list of all task IDs in the claimed tasks query set
        id_list = list(StandUpTasks.objects.filter(date=today).filter(user = request.user.id).values_list("task", flat=True))

        # Find all tasks that have been assigned to the user, are not complete, and are not currently claimed by the user for today
        assigned_tasks = Task.objects.filter(task_assigned_user = request.user.id).exclude(task_status = "Complete").exclude(id__in=id_list)

        context ={
            "claimed_tickets": claimed_tickets,
            "claimed_tasks": claimed_tasks,
            "assigned_tasks": assigned_tasks,
            "assigned_tickets": assigned_tickets
        }

        return render(request, "claim_edit.html", context)






