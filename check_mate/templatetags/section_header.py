from ..models import Project
from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/section_header.html')
def section_header(item_type, item):
    delete_status = item.delete_status
    item_id = item.id
    user_initials = ""
    if item_type == "Project":
        title = item.project_name
        description = item.project_description
        date_description = "Project Due"
        due_date = item.project_due
        status_description = "Project Status"
        status = item.project_status
        progress = item.get_ticket_status
        sub_items = item.ticket_set.all
        edit_link = 'check_mate:project_edit'
        delete_link = 'check_mate:project_delete'
        parent_item_link = ""
        parent_item_id = ""
        parent_item = ""
    elif item_type == "Ticket":
        title = item.ticket_name
        description = item.ticket_description
        date_description = "Ticket Due"
        due_date = item.ticket_due
        status_description = "Ticket Status"
        status = item.ticket_status
        progress = item.get_task_status
        sub_items = item.task_set.all
        edit_link = 'check_mate:ticket_edit'
        delete_link = 'check_mate:ticket_delete'
        parent_item_link = 'check_mate:project_details'
        parent_item_id = item.project.id
        parent_item = item.project.project_name
        if item.ticket_assigned_user:
            first_initial = list(item.ticket_assigned_user.first_name)[0]
            last_initial = list(item.ticket_assigned_user.last_name)[0]
            user_initials = f"{first_initial}{last_initial}"
            user_initials.upper()

    return{"title": title, "description": description, "date_description": date_description, "due_date": due_date, "status_description": status_description, "status": status, "progress": progress, "sub_items": sub_items, "edit_link": edit_link, "item_id": item_id, "delete_status": delete_status, "delete_link": delete_link, "parent_item_link": parent_item_link, "parent_item_id": parent_item_id, "parent_item": parent_item, "user_initials": user_initials}