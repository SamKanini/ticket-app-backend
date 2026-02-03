from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Event, Ticket
import uuid

@receiver(post_save, sender=Event)
def create_tickets_for_event(sender, instance, created, **kwargs):
    if created:  # Only when event is first created
        print(f"Creating {instance.total_seats} tickets for {instance.name}")
        
        # Create tickets with seat numbers
        tickets_to_create = []
        for i in range(1, instance.total_seats + 1):
            tickets_to_create.append(
                Ticket(
                    event=instance,
                    seat_number=f"{i:03d}",  # 001, 002, 003... 100
                    ticket_number=str(uuid.uuid4())[:8].upper()  # Generate unique ticket number
                )
            )
        
        # Bulk create for efficiency
        Ticket.objects.bulk_create(tickets_to_create)
        print(f"Successfully created {len(tickets_to_create)} tickets")