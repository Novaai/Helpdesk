from django.contrib.auth.models import Group
from ticketing.models import Ticket

def get_user_with_lightest_load():
    try:
        helpdesk_admins = Group.objects.get(name="Helpdesk Admins").user_set.all()
    except Group.DoesNotExist:
        return None

    if not helpdesk_admins.exists():
        return None

    ticket_counts = {
        user: Ticket.objects.filter(assigned_to=user, status='pending').count()
        for user in helpdesk_admins
    }

    return min(ticket_counts, key=ticket_counts.get)