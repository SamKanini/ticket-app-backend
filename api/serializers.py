from rest_framework import serializers
from .models import User, Customer, Event, Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone']

class TicketSerializer(serializers.ModelSerializer):
    #explain Here
    event_name = serializers.CharField(source='event.name', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'event_name', 'seat_number', 'is_sold', 'ticket_number', 'purchased_at']

class EventSerializer(serializers.ModelSerializer):
    available_tickets = serializers.ReadOnlyField()
    sold_tickets = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'venue', 'ticket_price', 
                  'total_seats', 'available_tickets', 'sold_tickets']