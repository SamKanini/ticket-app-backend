
from django.contrib import admin
from .models import Customer, Event, Ticket

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'venue', 'total_seats', 'available_tickets', 'sold_tickets']
    readonly_fields = ['available_tickets', 'sold_tickets']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['event', 'seat_number', 'is_sold', 'customer', 'purchased_at']
    list_filter = ['is_sold', 'event']
    search_fields = ['seat_number', 'ticket_number']