from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import Lower
from api.models import UserData

class Command(BaseCommand):
    help = 'Deletes all duplicates of UserData records based on username and password, case-insensitively.'

    def handle(self, *args, **kwargs):
        # Annotate each object with a new field that is the lowercase version of the username and password
        annotated_users = UserData.objects.annotate(
            lowercase_username=Lower('username'),
            lowercase_password=Lower('password'),
        )

        # Identify duplicate username and password combinations in lowercase
        duplicates = annotated_users.values('lowercase_username', 'lowercase_password').annotate(
            count=Count('id')
        ).filter(count__gt=1)

        # Loop over the identified duplicates to delete them
        for duplicate in duplicates:
            # Delete all records with this username and password in a case-insensitive manner
            UserData.objects.filter(
                username__iexact=duplicate['lowercase_username'],
                password__iexact=duplicate['lowercase_password']
            ).delete()

        self.stdout.write(self.style.SUCCESS('All duplicates based on username and password have been deleted, disregarding case.'))
