import datetime

from check_mate.models import *

# Non-MVP Notes -------------------------------------------
# V2: Update task history posts to include comments, when functionality is available
# ----------------------------------------------------------

def __update_task_history(task, user, activity_type, activity_details):
    if activity_type == "Status":
        new_task_history = TaskHistory(task=task, task_active_user=user, activity_type="Status", status=activity_details, activity_date=datetime.date.today())

    elif activity_type == "Assignment":
        new_task_history = TaskHistory(task=task, task_active_user=user, task_affected_user =activity_details, activity_type="Assignment", activity_date=datetime.date.today())

    new_task_history.save()


def __update_ticket_history(ticket, user, activity_type, activity_details):
    if activity_type == "Status":
        new_ticket_history = TicketHistory(ticket=ticket, ticket_active_user=user, activity_type="Status", status=activity_details, activity_date=datetime.date.today())

        new_ticket_history.save()

    elif activity_type == "Assignment":
        new_ticket_history = TicketHistory(ticket=ticket, ticket_active_user = user, ticket_affected_user=activity_details, activity_type="Assignment", activity_date=datetime.date.today())

        new_ticket_history.save()

def __get_ticket_detail_history_descriptions(ticket_history, task_history, request):
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
    return all_history

def __filter_ticket_history(user, selected_tickets):
    today = datetime.date.today()
    previous_date = ""

    if today.weekday() == 0:
        previous_date = today + relativedelta(weekday=FR(-1))

    else:
        previous_date = today - datetime.timedelta(1)

    ticket_activity = TicketHistory.objects.filter(activity_date = previous_date).filter(ticket_active_user= user).filter(ticket__in=selected_tickets).order_by('ticket__ticket_name')


    ticket_history = dict()
    for ticket in ticket_activity:
        try:
            ticket_history[ticket.ticket.ticket_name].append(ticket)
        except:
            ticket_history[ticket.ticket.ticket_name] = list()
            ticket_history[ticket.ticket.ticket_name].append(ticket)

    return ticket_history

def __filter_task_history(user, selected_tickets):
    selected_tasks = []

    today = datetime.date.today()
    previous_date = ""

    if today.weekday() == 0:
        previous_date = today + relativedelta(weekday=FR(-1))

    else:
        previous_date = today - datetime.timedelta(1)

    all_tasks = Task.objects.filter(ticket__in=selected_tickets)

    for task in all_tasks:
        selected_tasks.append(task.id)

    task_activity = TaskHistory.objects.filter(activity_date = previous_date).filter(task_active_user=user).filter(task__in=selected_tasks).order_by('task__task_name')

    task_history = dict()
    for task in task_activity:
        try:
            task_history[task.task.task_name].append(task)
        except:
            task_history[task.task.task_name] = list()
            task_history[task.task.task_name].append(task)

    return task_history

def __filter_road_block_ticket(selected_projects):
    road_blocked_tickets = Ticket.objects.filter(ticket_status = "Road Block").filter(project__in=selected_projects)

    return road_blocked_tickets

def __filter_road_block_task(selected_tickets):
    road_blocked_tasks = Task.objects.filter(task_status = "Road Block").filter(ticket__in=selected_tickets)

    return road_blocked_tasks