import random
import uuid
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from ..common.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField
EMPLOYEE, OWNER, STUDENT = 'employee', 'owner', 'student'
ACTIVE, NEW = 'active', 'new'


PHONE_EXPIRE = 2


class UserConfirmation(models.Model):
    code = models.CharField(max_length=4)
    user = models.OneToOneRel('users.User', models.CASCADE, 'verify_code')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class UserManager(AbstractUserManager):
    def _create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError("The given phone number must be set")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone, password, **extra_fields)

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser, BaseModel):
    REQUIRED_FIELDS = []
    username = None
    email = None

    ROLE_CHOICES = (
        (EMPLOYEE, 'Employee'),
        (OWNER, 'Owner'),
        (STUDENT, 'Student'),

    )

    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (NEW, 'New'),
    )

    phone = PhoneNumberField(unique=True, verbose_name='Phone Number')
    role = models.CharField(max_length=50, verbose_name='Type', choices=ROLE_CHOICES, default=EMPLOYEE)
    status = models.CharField(default=NEW, verbose_name='Status', choices=STATUS_CHOICES, max_length=50)
    USERNAME_FIELD = 'phone'
    wallet = models.PositiveBigIntegerField(default=0, verbose_name='Wallet')
    objects = UserManager()

    def __str__(self):
        return str(self.phone)

    def save(self, *args, **kwargs):
        self.hashing_password()
        super().save(*args, **kwargs)

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def create_verify_code(self):
        code = "".join(str(random.randint(0, 100) % 10) for _ in range(4))
        if UserConfirmation.objects.filter(user=self).exists():
            UserConfirmation.objects.filter(user=self).update(
                code=code,
                is_confirmed=False,
                expiration_time=datetime.now() + timedelta(minutes=PHONE_EXPIRE)
            )
        else:
            UserConfirmation.objects.create(user=self, code=code)
        return code

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
