#Signals = Triggers
from ticketing.utils.assignment import get_user_with_lightest_load
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from .utils.tagger import assign_tags_to_ticket  # This works because of __init__.py

@receiver(post_save, sender=Ticket)
def auto_tag_ticket(sender, instance, created, **kwargs):
    if created:
        assign_tags_to_ticket(instance)


@receiver(post_save, sender=Ticket)
def auto_assign_ticket(sender, instance, created, **kwargs):
    if created and not instance.assigned_to:
        from ticketing.utils.assignment import get_user_with_lightest_load
        helper = get_user_with_lightest_load()
        if helper:
            instance.assigned_to = helper
            instance.save()