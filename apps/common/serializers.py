from datetime import datetime
from rest_framework.serializers import ModelSerializer
from ..common import models
from rest_framework import serializers


class FloorListSerializer(ModelSerializer):

    class Meta:
        model = models.Floor
        fields = (
            "id",
            "name",
            'parent',
            'order',
        )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class AttendanceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attendance
        fields = (
            'id', 'is_available',
            'student', 'date', 'apartment', 'is_late',
            'student_name', 'room_name'
        )

        extra_kwargs = {
            "student": {"read_only": True},
            "apartment": {"read_only": True},
            "is_late": {"read_only": True},
            "date ": {"read_only": True},

        }


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = (
            'id', 'teacher',
            'name', 'edu_form'
        )

    def validate(self, attrs):
        return attrs


class ApplicationDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ApplicationDate
        fields = (
            'date',
        )

    def validate(self, attrs):
        if attrs['date'] < datetime.today().date():
            raise serializers.ValidationError({"date": "O\'tib ketgan sanani tanlash mumkin emas"})
        return attrs


class ApplicationCreateSerializer(serializers.ModelSerializer):
    dates = serializers.ListSerializer(
        required=True, write_only=True,
        child=ApplicationDatesSerializer(required=True)
    )

    class Meta:
        model = models.Application
        fields = (
            'id',
            'reason',
            'dates',
        )

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        user_apartment = models.UserApartment.objects.filter(student=user).first()
        if len(attrs['dates']) == 0:
            raise serializers.ValidationError({"dates": "Sana kiritish majburiy"})
        if not user_apartment:
            raise serializers.ValidationError({"reason": "Yotoqhona bilan shartnoma mavjud emas"})
        attrs['user_apartment'] = user_apartment

        for date_obj in attrs['dates']:
            date = date_obj.get('date')
            for application in models.Application.objects.filter(user_apartment=user_apartment):
                if models.ApplicationDate.objects.filter(date=date, application=application).exists():
                    raise serializers.ValidationError({"date": "Bu sanada ariza yuborilgan"})
        return attrs

    def create(self, validated_data):
        dates_data = validated_data.pop('dates')
        application = models.Application.objects.create(**validated_data)

        for date_data in dates_data:
            models.ApplicationDate.objects.create(application=application, **date_data)

        return application


class StudentApplicationsSerializer(serializers.ModelSerializer):
    dates = ApplicationDatesSerializer(many=True)

    class Meta:
        model = models.Application
        fields = (
            'id',
            'reason',
            'user_apartment',
            'admin',
            'address',
            'status',
            'student_data',
            'admin_data',
            'dates',
        )


class ApplicationUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Application
        fields = (
            'id',
            'status',
        )


class StudentPaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StudentPayments
        fields = (
            'id',
            'student_apartment',
            'amount',
            'date',
            'admin_data',
        )