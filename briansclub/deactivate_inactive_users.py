from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Deactivate users who have not logged in for more than a week'

    def handle(self, *args, **options):
        # Calculate the date one week ago
        one_week_ago = timezone.now() - timedelta(weeks=1)

        # Find users who haven't logged in for more than a week
        inactive_users = User.objects.filter(last_login__lt=one_week_ago)

        # Deactivate the users
        for user in inactive_users:
            user.is_active = False
            user.save()

        # Print the number of deactivated users
        self.stdout.write(self.style.SUCCESS(f'Deactivated {inactive_users.count()} users'))