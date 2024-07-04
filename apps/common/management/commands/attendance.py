from datetime import datetime

from django.core.management.base import BaseCommand
from apps.common.models import Floor, Attendance, UserApartment
from apps.users.models import User
import uuid  # Import uuid for generating unique identifiers


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_apartments = UserApartment.objects.filter(status='active').values_list('student__id', flat=True)
        users = User.objects.filter(pk__in=user_apartments)
        for user in users:
            apartment = user.user_apartments.filter(status='active').first()
            if apartment:
                attendance, created = Attendance.objects.get_or_create(
                    student=user,
                    date=str(datetime.today().date()),
                    apartment=apartment.apartment,
                )
        self.stdout.write(msg='SUCCESS')
