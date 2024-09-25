from datetime import datetime

from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from utils.work_with_date import get_last_day_of_month, get_count_of_days
from .models import UserRoles
from ..users import models as users
from ..common import models as common


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = users.User.objects.filter(phone=attrs['phone']).first()
        if not user:
            raise serializers.ValidationError({"phone": "Bunday foydalanuvchi topilmadi"})
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError({"password": 'Parol xato kiritildi'})
        return attrs


class StudentSerializer(serializers.ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(
        queryset=common.Floor.objects.filter(parent__isnull=False),
        required=True, write_only=True
    )
    attendance = serializers.SerializerMethodField()
    added_at = serializers.DateField(write_only=True, required=True)

    def get_attendance(self, obj):
        attendance = obj.attendances.filter(date=datetime.today().date()).first()
        return {
            'id': attendance.pk,
            'is_available': attendance.is_available
        } if attendance else False

    class Meta:
        model = users.User
        fields = (
            'id',
            'phone',
            'password',
            'first_name',
            'apartment',
            'group',
            'attendance',
            'added_at',
            'balance'
        )

    def validate(self, attrs):
        apartment_id = attrs['apartment']
        group = attrs.get('group')
        if not group:
            raise serializers.ValidationError({"group": "Guruh tanlash shart"})
        apartment = common.UserApartment.objects.filter(status='active', apartment__id=apartment_id.id).count()
        if apartment >= 6:
            raise serializers.ValidationError({"apartment": "Bu xonada oquvchilar soni 6 ta"})
        return attrs

    def create(self, validated_data):
        apartment = validated_data.pop("apartment")
        added_at = validated_data.pop("added_at")
        validated_data['status'] = 'active'
        validated_data['role'] = 'student'

        instance = super().create(validated_data)
        UserRoles.objects.create(
            user=instance, role='student'
        )
        user_apartment = common.UserApartment.objects.create(
            student=instance, apartment=apartment, added_at=added_at
        )
        common.Attendance.objects.create(
            student=instance, apartment=apartment, date=datetime.today().date(),
            is_available=None
        )
        self.withdraw_payment(user_apartment)
        return instance

    @classmethod
    def withdraw_payment(cls, user_apartment):
        added_at = datetime.strptime(str(user_apartment.added_at), "%Y-%m-%d").date()
        price = 200000
        last_day = get_last_day_of_month(added_at)
        all_days_count = get_count_of_days(added_at.replace(day=1), last_day.date())
        allowed_days = get_count_of_days(added_at, last_day.date())
        amount = -((price / all_days_count) * allowed_days)
        print(amount)
        common.StudentPayments.objects.create(
            student_apartment=user_apartment,
            amount=amount,
            date=datetime.today().date(),
        )

class EmployeeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = users.User
        fields = (
            'id',
            'first_name',
            'phone',
            'first_name'
        )
