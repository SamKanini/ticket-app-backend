from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer, CustomerSerializer, EventSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Customer, Event, Ticket
from rest_framework import generics

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        # Create the user
        user = serializer.save()
        # Automatically create a Customer profile for this user
        Customer.objects.create(user=user)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Customer.objects.filter(user=self.request.user)
        return Customer.objects.none()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            serializer = self.get_serializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    
    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        """Get all tickets for a specific event"""
        event = self.get_object()
        tickets = event.tickets.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # For list/retrieve, only show user's own tickets
        if self.action in ['list', 'retrieve']:
            return Ticket.objects.filter(customer__user=self.request.user)
        # For purchase action/ everything else, allow access to all tickets
        return Ticket.objects.all()
    
    @action(detail=True, methods=['post'])
    # creates a custom endpoint 
    def purchase(self, request, pk=None):
        """Purchase a specific ticket by ID"""
        ticket = self.get_object()
        
        # Check if ticket is already sold
        if ticket.is_sold:
            return Response(
                {'error': 'This ticket has already been sold'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get customer
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Mark ticket as sold
        ticket.is_sold = True
        ticket.customer = customer
        ticket.purchased_at = timezone.now()
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

        