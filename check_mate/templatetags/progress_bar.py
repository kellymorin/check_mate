from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/progress_bar.html')
def progress_bar(total, complete, active):
    return{'total': total, 'complete': complete, 'active': active}