
# Then they will be presented with a detailed view of their activity from yesterday, the option to select their priorities for today, and a place to note any road blocks they're facing

# When reviewing the activity from yesterday
# Then the user will be shown all tasks they commented on, edited, added, completed, etc
# And any other activity they had on the project board from the last 24 hours
# If the stand-up view is being accessed on a Monday, then the yesterday tab will refer to all activity from the previous friday

# When reviewing the priorities for today
# Then the user will be able to select any tasks they have been assigned, comments they have been mentioned in, or incomplete tasks/tickets that were started the previous day as their priorities for the day

import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from check_mate.models import *
from dateutil.relativedelta import relativedelta, FR

@login_required
def stand_up_view(request):
    # if no tickets have been claimed for today's stand up, show the option to select tickets
    today = datetime.date.today()
    previous_date = ""

    if today.weekday() == 0:
        previous_date = today + relativedelta(weekday=FR(-1))

    else:
        previous_date = today - datetime.timedelta(1)

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

    # Find tickets or tasks the user has interacted with in the last 24 hours that are not closed
    # Have an affordance to see all open tickets or tasks


    # IDEAL FEATURE: Once a ticket has been claimed for the day, it will not display in other users options to claim (unless it's a review)

        return render(request, "claim.html", context)

def remove_claim(request):
    # Create affordance to delete claimed tasks

    today = datetime.date.today()

    if request.method == "POST":
        for item in request.POST:
            if "task" in item or "ticket" in item:
                if "task" in item:
                    task_id = item.split('-')[1]
                    task = Task.objects.get(pk=task_id)
                    claimed_task = StandUpTasks.objects.filter(task=task).filter(user = request.user).filter(date=today)
                    claimed_task.delete()
                    # print("task", claimed_task)
                else:
                    ticket_id = item.split("-")[1]
                    ticket = Ticket.objects.get(pk=ticket_id)
                    claimed_ticket = StandUpTickets.objects.filter(ticket=ticket).filter(user = request.user).filter(date=today)
                    claimed_ticket.delete()

        return HttpResponseRedirect(reverse("check_mate:stand-up"))

    else:
        claimed_tickets = StandUpTickets.objects.filter(date = today).filter(user = request.user.id)
        claimed_tasks = StandUpTasks.objects.filter(date = today).filter(user = request.user.id)

        context ={
            "claimed_tickets": claimed_tickets,
            "claimed_tasks": claimed_tasks
        }

        return render(request, "claim_edit.html", context)






