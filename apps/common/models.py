import datetime
from datetime import timezone
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True


class Floor(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name")
    is_active = models.BooleanField(default=True, verbose_name='Active')
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, verbose_name="Qavat", related_name='children', null=True, blank=True)
    order = models.PositiveIntegerField(default=999)

    def __str__(self):
        return f"{self.pk}-{self.name}"


class UserApartment(BaseModel):

    class GroupStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'

    student = models.ForeignKey(
        "users.User", related_name="user_apartments", on_delete=models.CASCADE, verbose_name='Student',
    )
    apartment = models.ForeignKey(
        Floor, related_name="user_apartments", on_delete=models.PROTECT, verbose_name='Apartment'
    )
    status = models.CharField(
        max_length=50, verbose_name='Group status',
        choices=GroupStatus.choices, default=GroupStatus.ACTIVE
    )


class LateReason(BaseModel):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Attendance(BaseModel):
    student = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='attendances', verbose_name='Student'
    )
    date = models.DateField(verbose_name='Date', default=datetime.datetime.now())
    apartment = models.ForeignKey(
        Floor, on_delete=models.CASCADE, related_name='attendances', limit_choices_to={'parent__isnull': False}
    )
    is_available = models.BooleanField(verbose_name='Is available', null=True, blank=True)
    admin = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='admin_attendances', null=True
    )
    is_late = models.BooleanField(default=False)
    reason = models.TextField()

    @property
    def student_name(self):
        return self.student.first_name

    @property
    def room_name(self):
        return self.apartment.name


class Group(BaseModel):
    class GroupGroupEduForm(models.TextChoices):
        DAYTIME = 'daytime', 'Daytime'
        EVENING = 'evening', 'Evening'
        REMOTE = 'remote', 'Remote'
        CORRESPONDENCE = 'correspondence', 'Correspondence'

    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        'users.User', related_name='teacher_groups', on_delete=models.PROTECT,
        limit_choices_to={"role": 'employee'}
    )
    edu_form = models.CharField(max_length=255, choices=GroupGroupEduForm.choices, default=GroupGroupEduForm.DAYTIME)


class Application(BaseModel):

    class StatusChoices(models.TextChoices):
        MODERATION = 'moderation', 'Moderation'
        APPROVED = 'approved', 'Approved'
        CANCELLED = 'cancelled', 'Cancelled'

    user_apartment = models.ForeignKey(
        UserApartment, related_name='applications', on_delete=models.CASCADE,
    )
    reason = models.TextField()
    admin = models.ForeignKey(
        'users.User', related_name='applications', on_delete=models.PROTECT,
    )
    status = models.CharField(max_length=255, choices=StatusChoices.choices, default=StatusChoices.MODERATION)


class ApplicationDate(BaseModel):
    application = models.ForeignKey(
        Application, related_name='dates', on_delete=models.CASCADE
    )
    date = models.DateField()

