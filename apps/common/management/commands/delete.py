from django.core.management.base import BaseCommand
from apps.common.models import Floor
import uuid  # Import uuid for generating unique identifiers


class Command(BaseCommand):

    def handle(self, *args, **options):
        floors = Floor.objects.filter(parent__isnull=True)
        for floor in floors:
            floor.delete()
        self.stdout.write(msg='SUCCESS')
