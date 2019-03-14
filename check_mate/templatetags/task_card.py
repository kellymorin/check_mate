from ..models import Task
from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/task_card.html')
def task_card(task_id, claim_status):
    task_instance = Task.objects.get(pk=task_id)
    user_initials = ""
    claim = False
    if task_instance.task_assigned_user:
        first_initial = list(task_instance.task_assigned_user.first_name)[0]
        last_initial = list(task_instance.task_assigned_user.last_name)[0]
        user_initials = f"{first_initial}{last_initial}"
        user_initials.upper()
    if claim_status == True:
        claim = True
    return {'task': task_instance, "user_initials": user_initials, "claim": claim}