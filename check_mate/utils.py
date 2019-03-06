import datetime

from check_mate.models import *

# TODO: Update task history posts to include comments, when functionality is available

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