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