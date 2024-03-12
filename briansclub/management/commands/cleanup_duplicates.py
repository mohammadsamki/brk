from django.core.management.base import BaseCommand
from django.db import models
from api.models import UserData

class Command(BaseCommand):
    help = 'Deletes duplicate UserData records based on username and password.'

    def handle(self, *args, **kwargs):
        # Find duplicate records based on username and password
        duplicates = UserData.objects.values('username', 'password').annotate(
            count=models.Count('id')
        ).filter(count__gt=1)

        for duplicate in duplicates:
            # Keep the most recent record and delete all others
            latest_record = UserData.objects.filter(username=duplicate['username'], password=duplicate['password']).latest('created_at')
            UserData.objects.filter(username=duplicate['username'], password=duplicate['password']).exclude(pk=latest_record.pk).delete()

        self.stdout.write(self.style.SUCCESS('Duplicate records have been removed successfully.'))
