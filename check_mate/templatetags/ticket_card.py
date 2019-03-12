from ..models import Ticket
from django import template

register = template.Library()

@register.inclusion_tag('reusable_components/ticket_card.html')
def ticket_card(ticket_id, claim_status):
    ticket_instance = Ticket.objects.get(pk=ticket_id)
    user_initials = ""
    claim = False
    if ticket_instance.ticket_assigned_user:
        first_initial = list(ticket_instance.ticket_assigned_user.first_name)[0]
        last_initial = list(ticket_instance.ticket_assigned_user.last_name)[0]
        user_initials = f"{first_initial}{last_initial}"
        user_initials.upper()
    if claim_status == True:
        claim = True
    return{'ticket': ticket_instance, "user_initials": user_initials, "claim": claim}