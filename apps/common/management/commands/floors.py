from django.core.management.base import BaseCommand
from apps.common.models import Floor
import uuid  # Import uuid for generating unique identifiers


class Command(BaseCommand):

    def handle(self, *args, **options):
        for floor in range(1, 6):
            parent_name = f'{floor}-Qavat'
            parent, _ = Floor.objects.get_or_create(name=parent_name, order=floor)
            for room in range(1, 12):
                child_name = f'{room}-xona'
                children, _ = Floor.objects.get_or_create(name=child_name, parent=parent, order=room)
        self.stdout.write(msg='SUCCESS')
