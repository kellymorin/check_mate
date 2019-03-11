from ..models import Ticket
from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/ticket_card_claim.html')
def ticket_card_claim(ticket_id):
    ticket_instance = Ticket.objects.get(pk=ticket_id)
    return{'ticket': ticket_instance}