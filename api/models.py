from django.db import models
from django.contrib.auth.models import User
import uuid

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.IntegerField(default=100)  # Total number of seats
    
    def __str__(self):
        return self.name
    
    @property
    def available_tickets(self):
        """Count how many tickets are not sold"""
        return self.tickets.filter(is_sold=False).count()
    
    @property
    def sold_tickets(self):
        """Count how many tickets are sold"""
        return self.tickets.filter(is_sold=True).count()

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=10)
    is_sold = models.BooleanField(default=False)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    purchased_at = models.DateTimeField(null=True, blank=True)
    ticket_number = models.CharField(max_length=8, unique=True, blank=True)
    
    class Meta:
        unique_together = ['event', 'seat_number']
        ordering = ['seat_number']
    
    def __str__(self):
        return f"{self.event.name} - Seat {self.seat_number}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)