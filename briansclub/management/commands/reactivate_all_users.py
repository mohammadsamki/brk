from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Reactivate all inactive users'

    def handle(self, *args, **options):
        # Find all inactive users
        inactive_users = User.objects.filter(is_active=False)

        if inactive_users.exists():
            # Reactivate the users
            for user in inactive_users:
                user.is_active = True
                user.save()

            # Print the number of reactivated users
            self.stdout.write(self.style.SUCCESS(f'Reactivated {inactive_users.count()} users'))
        else:
            self.stdout.write(self.style.WARNING('No inactive users found'))