from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from ..common import models
from rest_framework import serializers


class FloorListSerializer(ModelSerializer):

    class Meta:
        model = models.Floor
        fields = (
            "id",
            "name",
            'parent'
        )

    def validate(self, attrs):
        parent_id = attrs.get("parent")
        if parent_id:
            parent = models.Floor.objects.filter(parent__isnull=False, pk=parent_id.pk)
            if parent.exists():
                raise serializers.ValidationError({'parent': "Bunday qavat mavjud emas"})
        return attrs


class AttendanceUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attendance
        fields = (
            'id', 'is_available',
            'student', 'date', 'apartment', 'is_late',
            'student_name', 'room_name'
        )

        extra_kwargs = {
            "student": {"required": True},
            "apartment": {"required": True},
            "is_late": {"required": True},
            "date ": {"required": True},

        }

