from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create sample users for testing'

    def handle(self, *args, **options):
        users_to_create = [
            {'username': 'admin', 'password': 'admin123', 'email': 'admin@example.com'},
            {'username': 'testuser', 'password': 'testpass123', 'email': 'test@example.com'},
            {'username': 'demo', 'password': 'demo123', 'email': 'demo@example.com'},
        ]

        for user_data in users_to_create:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    password=user_data['password'],
                    email=user_data['email']
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user: {username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User {username} already exists')
                )

        self.stdout.write(
            self.style.SUCCESS('\nSample users created successfully!')
        )
        self.stdout.write('Available test credentials:')
        self.stdout.write('- admin / admin123')
        self.stdout.write('- testuser / testpass123')
        self.stdout.write('- demo / demo123')
