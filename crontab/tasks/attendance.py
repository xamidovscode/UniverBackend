from datetime import datetime
from celery import shared_task
from apps.common.models import UserApartment, Attendance
from apps.users.models import User


@shared_task()
def open_attendance():
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