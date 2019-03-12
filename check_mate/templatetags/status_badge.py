from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/status_badge.html')
def status_badge(status):
    return{'status': status}