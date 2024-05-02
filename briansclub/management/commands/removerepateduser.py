from django.core.management.base import BaseCommand
from briansclub.models import User
from django.db.models import Count

class Command(BaseCommand):
    help = 'Removes duplicate users from the database'

    def handle(self, *args, **options):
        # Identify duplicates based on the 'username' field
        duplicates = User.objects.values('username').annotate(username_count=Count('id')).filter(username_count__gt=1)

        for entry in duplicates:
            # Get IDs of all users with the same username, except for the first one
            users_to_delete_ids = User.objects.filter(username=entry['username']).order_by('id').values_list('id', flat=True)[1:]

            # Delete users by ID
            users_to_delete_count = User.objects.filter(id__in=list(users_to_delete_ids)).delete()[0]

            self.stdout.write(self.style.SUCCESS(f'Removed {users_to_delete_count} duplicate users for username {entry["username"]}'))
