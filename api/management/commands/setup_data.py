from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Event
from django.utils import timezone
from datetime import timedelta
from decouple import config

class Command(BaseCommand):
    help = 'Create initial data'

    def handle(self, *args, **kwargs):
        # Create superuser from environment variables
        username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
        email = config('DJANGO_SUPERUSER_EMAIL', default='sam.kanini18@gmail.com')
        password = config('DJANGO_SUPERUSER_PASSWORD', default='12345')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(f'Superuser {username} created!')
        else:
            self.stdout.write('Superuser already exists')

        # Create events if none exist
        if Event.objects.count() == 0:
            Event.objects.create(
                name='Rock Concert',
                description='Amazing rock music',
                date=timezone.now() + timedelta(days=30),
                venue='City Arena',
                ticket_price=50.00,
                total_seats=20
            )
            self.stdout.write('Sample event created!')
        else:
            self.stdout.write('Events already exist')