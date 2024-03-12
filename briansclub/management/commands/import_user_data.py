from django.core.management.base import BaseCommand
from api.models import UserData
import csv
from datetime import datetime
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Import user data from a text file'

    def add_arguments(self, parser):
        parser.add_argument('txt_file', type=str, help='The txt file with user data')

    def handle(self, *args, **options):
        txt_file = options['txt_file']
        with open(txt_file, 'r') as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)  # Skip the header row
            for row in reader:
                _, created = UserData.objects.get_or_create(
                    username=row[1],
                    password=row[2],
                    created_at=make_aware(datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S.%f+00')),
                    balance=row[4]
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"User {row[1]} added successfully"))
                else:
                    self.stdout.write(self.style.WARNING(f"User {row[1]} already exists"))
