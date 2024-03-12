from django.core.management.base import BaseCommand
from api.models import UserData

class Command(BaseCommand):
    help = 'Removes all users with a balance of 0.00'

    def handle(self, *args, **options):
        # The delete() method returns a dictionary describing the number of deleted objects.
        deleted_info = UserData.objects.filter(balance=0.00).delete()
        num_deleted = deleted_info[0]  # The number of deleted objects is the first item in the dictionary.
        self.stdout.write(self.style.SUCCESS(f'Successfully removed {num_deleted} users with zero balance'))
