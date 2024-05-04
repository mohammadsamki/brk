# fix_duplicate_content_types.py

from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models import Count


class Command(BaseCommand):
    help = 'Fix duplicate content type records in the database'

    def handle(self, *args, **options):
        # Find content types with duplicate IDs
        duplicate_content_types = ContentType.objects.values('id').annotate(count=Count('id')).filter(count__gt=1)

        # Iterate over duplicate content types
        for duplicate in duplicate_content_types:
            # Retrieve all duplicate instances of the content type
            duplicate_instances = ContentType.objects.filter(id=duplicate['id']).order_by('id')

            # Keep the first instance and delete the rest
            for idx, instance in enumerate(duplicate_instances):
                if idx == 0:
                    # Skip the first instance
                    continue
                try:
                    # Delete duplicate content type instance
                    instance.delete()
                    self.stdout.write(self.style.SUCCESS(f"Duplicate content type with ID {instance.id} has been deleted."))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"Failed to delete duplicate content type with ID {instance.id}."))
