from ..models import Task
from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/task_card_claim.html')
def task_card_claim(task_id):
    task_instance = Task.objects.get(pk=task_id)
    return {'task': task_instance}