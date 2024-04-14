from django.core.management.base import BaseCommand
from briansclub.models import Billing

class Command(BaseCommand):
    help = 'Clear all billing data'

    def handle(self, *args, **options):
        try:
            Billing.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared all billing data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
